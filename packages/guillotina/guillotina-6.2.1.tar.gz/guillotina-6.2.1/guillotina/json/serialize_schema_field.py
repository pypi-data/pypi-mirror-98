from guillotina import configure
from guillotina.component import get_multi_adapter
from guillotina.fields.interfaces import IPatchField
from guillotina.interfaces import ICloudFileField
from guillotina.interfaces import IFileField
from guillotina.interfaces import ISchemaFieldSerializeToJson
from guillotina.interfaces import ISchemaSerializeToJson
from guillotina.json.serialize_value import json_compatible
from guillotina.profile import profilable
from guillotina.schema import get_fields
from guillotina.schema.interfaces import IBool
from guillotina.schema.interfaces import IChoice
from guillotina.schema.interfaces import ICollection
from guillotina.schema.interfaces import IDate
from guillotina.schema.interfaces import IDatetime
from guillotina.schema.interfaces import IDecimal
from guillotina.schema.interfaces import IDict
from guillotina.schema.interfaces import IField
from guillotina.schema.interfaces import IFloat
from guillotina.schema.interfaces import IInt
from guillotina.schema.interfaces import IJSONField
from guillotina.schema.interfaces import IObject
from guillotina.schema.interfaces import IText
from guillotina.schema.interfaces import ITextLine
from guillotina.schema.interfaces import ITime
from zope.interface import implementedBy
from zope.interface import Interface


FIELDS_CACHE: dict = {}


@configure.adapter(for_=(IField, Interface, Interface), provides=ISchemaFieldSerializeToJson)
class DefaultSchemaFieldSerializer(object):

    # Elements we won't write
    filtered_attributes = ["order", "unique", "defaultFactory", "required"]

    # Elements that are of the same type as the field itself
    field_type_attributes = ("min", "max", "default", "title")

    # Elements that are of the same type as the field itself, but are
    # otherwise not validated
    non_validated_field_type_attributes = ("missing_value",)

    # Attributes that contain another field. Unfortunately,
    field_instance_attributes = ("key_type", "value_type")

    # Fields that are always written
    forced_fields = frozenset(["default", "missing_value", "title"])

    def __init__(self, field, schema, request):
        self.field = field
        self.schema = schema
        self.request = request

    def get_field(self):
        return self.field

    @profilable
    async def __call__(self):
        return self.serialize()

    def serialize(self):
        field = self.get_field()
        result = {"type": self.field_type}
        if self.widget is not None:
            result["widget"] = self.widget
        # caching the field_attributes here improves performance dramatically
        if field.__class__ in FIELDS_CACHE:
            field_attributes = FIELDS_CACHE[field.__class__].copy()
        else:
            field_attributes = {}
            for schema in implementedBy(field.__class__).flattened():
                field_attributes.update(get_fields(schema))
            FIELDS_CACHE[field.__class__] = field_attributes
        for attribute_name in sorted(field_attributes.keys()):
            attribute_field = field_attributes[attribute_name]
            if attribute_name in self.filtered_attributes:
                continue

            element_name = attribute_field.__name__
            attribute_field = attribute_field.bind(field)
            force = element_name in self.forced_fields

            value = attribute_field.get(field)

            # For 'default', 'missing_value' etc, we want to validate against
            # the imported field type itself, not the field type of the
            # attribute
            if (
                element_name in self.field_type_attributes
                or element_name in self.non_validated_field_type_attributes
            ):
                attribute_field = field

            text = None
            if isinstance(value, bytes):
                text = value.decode("utf-8")
            elif isinstance(value, str):
                text = value
            elif IField.providedBy(value):
                serializer = get_multi_adapter((value, field, self.request), ISchemaFieldSerializeToJson)
                text = serializer.serialize()
                if "properties" in text:
                    text = text["properties"]
            elif value is not None and (force or value != field.missing_value):
                text = json_compatible(value)

            if text:
                if attribute_name == "value_type":
                    attribute_name = "items"
                result[attribute_name] = text
        if result["type"] == "object":
            if IJSONField.providedBy(field):
                result.update(field.json_schema)
            if IDict.providedBy(field):
                if "properties" not in result:
                    result["properties"] = {}
                if field.value_type:
                    field_serializer = get_multi_adapter(
                        (field.value_type, self.schema, self.request), ISchemaFieldSerializeToJson
                    )
                    result["additionalProperties"] = field_serializer.serialize()
                else:
                    result["additionalProperties"] = True
            elif IObject.providedBy(field):
                schema_serializer = get_multi_adapter((field.schema, self.request), ISchemaSerializeToJson)
                result["properties"] = schema_serializer.serialize()
        if field.extra_values is not None:
            result.update(field.extra_values)
        return result

    @property
    def field_type(self):
        # Needs to be implemented on specific type
        return None

    @property
    def widget(self):
        # Needs to be implemented on specific type
        return None


@configure.adapter(for_=(IText, Interface, Interface), provides=ISchemaFieldSerializeToJson)
class DefaultTextSchemaFieldSerializer(DefaultSchemaFieldSerializer):
    @property
    def field_type(self):
        return "string"

    @property
    def widget(self):
        return "textarea"


@configure.adapter(for_=(IFileField, Interface, Interface), provides=ISchemaFieldSerializeToJson)
class DefaultFileSchemaFieldSerializer(DefaultSchemaFieldSerializer):
    @property
    def field_type(self):
        return "object"

    @property
    def widget(self):
        return "file"


@configure.adapter(for_=(IPatchField, Interface, Interface), provides=ISchemaFieldSerializeToJson)
class DefaultPatchFieldSchemaFieldSerializer(DefaultSchemaFieldSerializer):
    def get_field(self):
        return self.field.field

    @property
    def field_type(self):
        if ICollection.providedBy(self.field.field):
            return "array"
        return "object"


@configure.adapter(for_=(ICloudFileField, Interface, Interface), provides=ISchemaFieldSerializeToJson)
class DefaultCloudFileSchemaFieldSerializer(DefaultSchemaFieldSerializer):
    @property
    def field_type(self):
        return "object"

    @property
    def widget(self):
        return "file"


@configure.adapter(for_=(IJSONField, Interface, Interface), provides=ISchemaFieldSerializeToJson)
class DefaultJSONFieldSerializer(DefaultSchemaFieldSerializer):
    @property
    def field_type(self):
        return "object"


@configure.adapter(for_=(ITextLine, Interface, Interface), provides=ISchemaFieldSerializeToJson)
class DefaultTextLineSchemaFieldSerializer(DefaultSchemaFieldSerializer):
    @property
    def field_type(self):
        return "string"

    @property
    def widget(self):
        return "input"


@configure.adapter(for_=(IFloat, Interface, Interface), provides=ISchemaFieldSerializeToJson)
class DefaultFloatSchemaFieldSerializer(DefaultSchemaFieldSerializer):
    @property
    def field_type(self):
        return "number"


@configure.adapter(for_=(IInt, Interface, Interface), provides=ISchemaFieldSerializeToJson)
class DefaultIntSchemaFieldSerializer(DefaultSchemaFieldSerializer):
    @property
    def field_type(self):
        return "integer"


@configure.adapter(for_=(IBool, Interface, Interface), provides=ISchemaFieldSerializeToJson)
class DefaultBoolSchemaFieldSerializer(DefaultSchemaFieldSerializer):
    @property
    def field_type(self):
        return "boolean"


@configure.adapter(for_=(ICollection, Interface, Interface), provides=ISchemaFieldSerializeToJson)
class DefaultCollectionSchemaFieldSerializer(DefaultSchemaFieldSerializer):
    @property
    def field_type(self):
        return "array"


@configure.adapter(for_=(IChoice, Interface, Interface), provides=ISchemaFieldSerializeToJson)
class DefaultChoiceSchemaFieldSerializer(DefaultSchemaFieldSerializer):
    @property
    def field_type(self):
        return "string"

    @property
    def widget(self):
        return "select"


@configure.adapter(for_=(IObject, Interface, Interface), provides=ISchemaFieldSerializeToJson)
class DefaultObjectSchemaFieldSerializer(DefaultSchemaFieldSerializer):
    @property
    def field_type(self):
        return "object"


@configure.adapter(for_=(IDatetime, Interface, Interface), provides=ISchemaFieldSerializeToJson)
class DefaultDateTimeSchemaFieldSerializer(DefaultSchemaFieldSerializer):
    @property
    def field_type(self):
        return "datetime"


@configure.adapter(for_=(IDate, Interface, Interface), provides=ISchemaFieldSerializeToJson)
class DefaultDateSchemaFieldSerializer(DefaultSchemaFieldSerializer):
    @property
    def field_type(self):
        return "date"


@configure.adapter(for_=(ITime, Interface, Interface), provides=ISchemaFieldSerializeToJson)
class DefaultTimeSchemaFieldSerializer(DefaultSchemaFieldSerializer):
    @property
    def field_type(self):
        return "time"


@configure.adapter(for_=(IDict, Interface, Interface), provides=ISchemaFieldSerializeToJson)
class DefaultDictSchemaFieldSerializer(DefaultSchemaFieldSerializer):
    @property
    def field_type(self):
        return "object"


@configure.adapter(for_=(IDecimal, Interface, Interface), provides=ISchemaFieldSerializeToJson)
class DefaultDecimalSchemaFieldSerializer(DefaultSchemaFieldSerializer):
    @property
    def field_type(self):
        return "decimal"
