from .dbfile import DBFile
from .exceptions import RangeNotFound
from .exceptions import RangeNotSupported
from guillotina import configure
from guillotina.blob import Blob
from guillotina.event import notify
from guillotina.events import FileBeforeUploadFinishedEvent
from guillotina.events import FileUploadFinishedEvent
from guillotina.events import FileUploadStartedEvent
from guillotina.exceptions import BlobChunkNotFound
from guillotina.exceptions import FileNotFoundException
from guillotina.files.utils import generate_key
from guillotina.files.utils import guess_content_type
from guillotina.interfaces import IDBFileField
from guillotina.interfaces import IFileCleanup
from guillotina.interfaces import IFileField
from guillotina.interfaces import IFileNameGenerator
from guillotina.interfaces import IFileStorageManager
from guillotina.interfaces import IRequest
from guillotina.interfaces import IResource
from guillotina.interfaces import IUploadDataManager
from guillotina.response import HTTPPreconditionFailed
from typing import AsyncIterator

import time


@configure.adapter(for_=(IResource, IFileField), provides=IFileNameGenerator)
class FileNameGenerator:
    def __init__(self, context, field):
        self.context = context
        self.field = field

    def __call__(self):
        return generate_key(self.context)


@configure.adapter(for_=IFileStorageManager, provides=IUploadDataManager, name="db")
class DBDataManager:

    _data = None
    _file = None
    _timeout = 15  # how long before a tus upload becomes stale

    def __init__(self, file_storage_manager):
        self.file_storage_manager = file_storage_manager
        self.context = file_storage_manager.context
        self.request = file_storage_manager.request
        self.field = file_storage_manager.field

    @property
    def real_context(self):
        return self.field.context or self.context

    async def load(self):
        if not hasattr(self.context, "__uploads__"):
            self.context.__uploads__ = {}
        if self.field.__name__ not in self.context.__uploads__:
            self.context.__uploads__[self.field.__name__] = {}
        self._data = self.context.__uploads__[self.field.__name__]

    def protect(self):
        if "last_activity" in self._data:
            # check for another active upload, fail if we're screwing with
            # someone else
            if (time.time() - self._data["last_activity"]) < self._timeout:
                if self.request.headers.get("TUS-OVERRIDE-UPLOAD", "0") != "1":
                    raise HTTPPreconditionFailed(content={"reason": "There is already an active tusupload"})

    async def start(self):
        self.protect()

        if "_blob" in self._data:
            # clean it
            blob = self._data["_blob"]
            bfile = blob.open("r")
            await bfile.async_del()

        self._data.clear()
        self.context.register()
        self._data["last_activity"] = time.time()

        await notify(FileUploadStartedEvent(self.context, field=self.field, dm=self))

    async def update(self, **kwargs):
        kwargs["last_activity"] = time.time()
        self._data.update(kwargs)
        self.context.register()

    async def save(self, **kwargs):
        pass

    async def finish(self, values=None):
        # create file object with new data from finished upload
        try:
            file = self.field.get(self.real_context)
        except AttributeError:
            file = None

        if file is None:
            file = self.file_storage_manager.file_class()
        else:
            # save previous data on file.
            # we do this instead of creating a new file object on every
            # save just in case other implementations want to use the file
            # object to store different data
            file._old_uri = file.uri
            file._old_size = file.size
            file._old_filename = file.filename
            file._old_md5 = file.md5
            file._old_content_type = file.guess_content_type()

            if getattr(file, "_blob", None):
                cleanup = IFileCleanup(self.context, None)
                if cleanup is None or cleanup.should_clean(file=file):
                    bfile = file._blob.open("r")
                    await bfile.async_del()
                else:
                    file._previous_blob = getattr(file, "_blob", None)

        await notify(FileBeforeUploadFinishedEvent(self.context, field=self.field, file=file, dm=self))

        if values is None:
            values = self._data
        self.field.set(self.real_context, file)
        for key, value in values.items():
            setattr(file, key, value)

        if self.field.__name__ in getattr(self.context, "__uploads__", {}):
            del self.context.__uploads__[self.field.__name__]
            self.context.register()

        try:
            self.field.context.data.register()
        except AttributeError:
            self.field.context.register()

        await notify(FileUploadFinishedEvent(self.context, field=self.field, file=file, dm=self))
        return file

    @property
    def content_type(self):
        return guess_content_type(self._data.get("content_type"), self._data.get("filename"))

    @property
    def size(self):
        return self._data.get("size", 0)

    def get_offset(self):
        return self._data.get("offset", 0)

    def get(self, name, default=None):
        if self._data is None:
            return default
        return self._data.get(name, default)


@configure.adapter(for_=IResource, provides=IFileCleanup)
class DefaultFileCleanup:
    def __init__(self, context):
        pass

    def should_clean(self, **kwargs):
        return True


@configure.adapter(for_=(IResource, IRequest, IDBFileField), provides=IFileStorageManager)
class DBFileStorageManagerAdapter:

    file_class = DBFile

    def __init__(self, context, request, field):
        self.context = context
        self.request = request
        self.field = field

    def exists(self):
        try:
            file = self.field.get(self.field.context or self.context)
        except AttributeError:  # pragma: no cover
            file = None
        return file is not None and file.size > 0

    async def start(self, dm):
        blob = Blob(self.context)
        await dm.update(_blob=blob)

    async def iter_data(self) -> AsyncIterator[bytes]:
        file = self.field.get(self.field.context or self.context)
        if not getattr(file, "_blob", None):
            raise FileNotFoundException()
        blob = file._blob
        bfile = blob.open()
        async for chunk in bfile.iter_async_read():
            yield chunk

    async def range_supported(self) -> bool:
        file = self.field.get(self.field.context or self.context)
        blob = file._blob
        return blob.chunk_sizes is not None

    async def read_range(self, start: int, end: int) -> AsyncIterator[bytes]:
        file = self.field.get(self.field.context or self.context)
        if file is None or file._blob.chunk_sizes is None:
            raise RangeNotSupported(field=self.field)

        blob = file._blob
        bfile = blob.open()
        total = 0
        start_bytes_idx = start
        # find first blob
        search_total = 0
        for chunk_idx, chunk_size in sorted(blob.chunk_sizes.items(), key=lambda vv: vv[0]):
            if start_bytes_idx >= search_total and start_bytes_idx < (search_total + chunk_size):
                start_bytes_idx = start - search_total
                end_bytes_idx = start_bytes_idx + ((end - start) - total)

                while total < (end - start):
                    # now, just read from here until end
                    try:
                        chunk = (await bfile.async_read_chunk(chunk_idx))[start_bytes_idx:end_bytes_idx]
                    except BlobChunkNotFound:
                        raise RangeNotFound(field=self.field, blob=blob, start=start, end=end)
                    if len(chunk) == 0:  # pragma: no cover
                        raise RangeNotFound(field=self.field, blob=blob, start=start, end=end)
                    total += len(chunk)
                    yield chunk
                    chunk_idx += 1
                    start_bytes_idx = 0
                    end_bytes_idx = (end - start) - total

                if total != (end - start):  # pragma: no cover
                    raise RangeNotFound(field=self.field, blob=blob, start=start, end=end)
            else:
                search_total += chunk_size

    async def append(self, dm, iterable, offset) -> int:
        blob = dm.get("_blob")
        mode = "a"
        if blob.chunks == 0:
            mode = "w"
        bfile = blob.open(mode)
        size = 0
        async for chunk in iterable:
            size += len(chunk)
            await bfile.async_write_chunk(chunk)
        return size

    async def finish(self, dm):
        pass

    async def copy(self, to_storage_manager, dm):
        # too much storage manager logic here? only way to give file manager
        # more control for plugins
        await to_storage_manager.start(dm)
        await to_storage_manager.append(dm, to_storage_manager.iter_data(), 0)
        await to_storage_manager.finish(dm)
        await dm.finish()

    async def delete(self):
        obj = self.field.context or self.context
        file = self.field.get(obj)
        blobfile = file._blob.open("w")
        await blobfile.async_del()
        delattr(file, "_blob")
        self.field.context.register()
        return True
