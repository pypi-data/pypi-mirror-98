from typing import Any
from typing import Dict
from typing import Optional


class LRU(Dict[str, Any]):
    def __init__(self, size: int): ...
    def set(self, key: str, value: Any, size: Optional[int] = None) -> None: ...
