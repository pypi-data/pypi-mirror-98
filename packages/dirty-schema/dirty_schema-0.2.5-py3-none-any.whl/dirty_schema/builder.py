import re
from typing import Type

from dirty_models import AccessMode, ArrayField, BaseField, BaseModel, BooleanField, BytesField, DateField, \
    DateTimeField, EnumField, FloatField, HashMapField, IntegerField, ModelField, MultiTypeField, StringField, \
    StringIdField, TimeField, TimedeltaField
from dirty_validators.basic import AnyOf, BaseValidator, EqualTo, IPAddress, IsEmpty, IsNone, Length, MacAddress, \
    NoneOf, NotEmpty, \
    NotEmptyString, \
    NotEqualTo, NotNone, NumberRange, Regexp, StringNotContaining, URL, UUID
from dirty_validators.complex import BaseSpecMixin, BaseValueIterableMixin, ChainMixin, ListLike, ListValidatorMixin, \
    ModelValidateMixin, \
    Required, SomeMixin

from dirty_schema.models import JsonSchemaObject, SimpleTypes


class Context:

    def __init__(self):
        self._definitions = {}

    def get_reference_from_definition(self, definition: JsonSchemaObject):
        for ref, d in self._definitions.items():
            pass


def get_access_mode(model_class: Type[BaseModel], field: BaseField):
    if field.metadata is not None and field.metadata.get('hidden', False):
        return AccessMode.HIDDEN
    try:
        return model_class.__override_field_access_modes__[field.name]
    except KeyError:
        return field.access_mode


class Builder:

    def __init__(self, context: Context = None, *,
                 def_read_only: bool = True,
                 def_writable_only_on_creation=True):
        self._def_read_only = def_read_only
        self._def_writable_only_on_creation = def_writable_only_on_creation
        self._context = context or Context()

    def _iterate_validator_fields(self, validator: Type[ModelValidateMixin]):
        for name, field_validator in validator.spec.items():
            yield name, field_validator

    def generate_from_model_validator(self, validator: Type[ModelValidateMixin], schema: JsonSchemaObject = None):
        schema = schema or JsonSchemaObject(type=SimpleTypes.OBJECT)

        self.generate_from_model(validator.__modelclass__, schema)

        required = []
        for name, field_validator in self._iterate_validator_fields(validator):

            field_obj = validator.__modelclass__.get_field_obj(name)

            if field_obj is None:
                continue

            am = get_access_mode(validator.__modelclass__, field_obj)

            if am == AccessMode.HIDDEN \
                    or (am == AccessMode.READ_ONLY and not self._def_read_only) \
                    or (am == AccessMode.WRITABLE_ONLY_ON_CREATION and not self._def_writable_only_on_creation):
                continue

            name = field_obj.name

            try:
                property_schema = schema.get_property_schema(name)
            except KeyError:
                continue

            if isinstance(field_validator, Required):
                required.append(name)

            property_schema = self.map_validate_field(property_schema, field_validator, field_obj)
            schema.set_property_schema(name, property_schema)

        if len(required):
            schema.required = required

        return schema

    def map_validate_field(self, property_schema, validator, field_obj):
        if isinstance(validator, EqualTo):
            property_schema.const = validator.comp_value
        elif isinstance(validator, NotEqualTo):
            property_schema.not_ = {'const': validator.comp_value}
        elif isinstance(validator, StringNotContaining):
            property_schema.not_ = {'pattern': re.escape(validator.token)}
        elif isinstance(validator, Length):
            if property_schema.type_ == SimpleTypes.STRING:
                if validator.max is not None:
                    property_schema.maxLength = validator.max
                if validator.min is not None:
                    property_schema.minLength = validator.min
            elif property_schema.type_ == SimpleTypes.ARRAY:
                if validator.max is not None:
                    property_schema.maxItems = validator.max
                if validator.min is not None:
                    property_schema.minItems = validator.min
            elif property_schema.type_ == SimpleTypes.OBJECT:
                if validator.max is not None:
                    property_schema.maxProperties = validator.max
                if validator.min is not None:
                    property_schema.minProperties = validator.min
        elif isinstance(validator, NumberRange):
            if validator.max is not None:
                property_schema.maximum = validator.max
            if validator.min is not None:
                property_schema.minimum = validator.min
        elif isinstance(validator, Regexp):
            property_schema.pattern = validator.regex.pattern
        elif isinstance(validator, AnyOf):
            property_schema.enum = validator.values
        elif isinstance(validator, NoneOf):
            property_schema.not_ = {'enum': validator.values}
        elif isinstance(validator, IsEmpty):
            property_schema.anyOf = [SimpleTypes.NULL,
                                     {'type': SimpleTypes.STRING, 'maxLength': 0},
                                     {'type': SimpleTypes.ARRAY, 'maxItems': 0},
                                     {'type': SimpleTypes.OBJECT, 'maxProperties': 0}]
        elif isinstance(validator, NotEmptyString):
            property_schema.minLength = 1
        elif isinstance(validator, NotEmpty):
            property_schema.not_ = {'const': SimpleTypes.NULL}
            if property_schema.type_ == SimpleTypes.STRING:
                property_schema.minLength = 1
            elif property_schema.type_ == SimpleTypes.ARRAY:
                property_schema.minItems = 1
            elif property_schema.type_ == SimpleTypes.OBJECT:
                property_schema.minProperties = 1
        elif isinstance(validator, IsNone):
            property_schema.const = SimpleTypes.NULL
        elif isinstance(validator, NotNone):
            property_schema.not_ = {'const': SimpleTypes.NULL}
        elif isinstance(validator, ChainMixin):
            for child_validator in validator.validators:
                property_schema = self.map_validate_field(property_schema, child_validator, field_obj)
        elif isinstance(validator, ModelValidateMixin):
            property_schema = self.generate_from_model_validator(validator.__class__, property_schema)
        elif isinstance(validator, SomeMixin):
            if isinstance(field_obj, MultiTypeField):
                property_schema = self.map_multitype_with_multivalidator(field_obj, validator)
            else:
                property_schema.anyOf = [self.map_validate_field(property_schema.copy(), child_validator, field_obj)
                                         for child_validator in validator.validators]
        elif isinstance(validator, ListValidatorMixin) and isinstance(field_obj, (ArrayField, ListLike)):
            property_schema.items = self.map_validate_field(property_schema.items,
                                                            validator.validator,
                                                            field_obj.field_type)
        return property_schema

    def _iterate_model_fields(self, model_class: Type[BaseModel]):
        for name, field in model_class.get_structure().items():
            if field.metadata is not None and field.metadata.get('hidden', False):
                continue
            try:
                am = model_class.__override_field_access_modes__[name]
            except KeyError:
                am = field.access_mode

            if am == AccessMode.HIDDEN:
                continue

            yield name, field

    def generate_from_model(self, model_class: Type[BaseModel], schema: JsonSchemaObject = None):
        schema = schema or JsonSchemaObject(type=SimpleTypes.OBJECT)

        schema.properties = {
            name: self.map_field_type(field)
            for name, field in self._iterate_model_fields(model_class)
            if field.access_mode == AccessMode.READ_AND_WRITE or
               (self._def_writable_only_on_creation and
                get_access_mode(model_class, field) == AccessMode.WRITABLE_ONLY_ON_CREATION) or
               (self._def_read_only and get_access_mode(model_class, field) == AccessMode.READ_ONLY)
        }

        try:
            schema.additionalProperties = self.map_field_type(model_class.__field_type__, metadata=False)
        except AttributeError:
            pass

        return schema

    def map_field_type(self, field: BaseField, metadata=True) -> JsonSchemaObject:
        if metadata:
            schema = JsonSchemaObject(default=field.default if not callable(field.default) else field.default(),
                                      title=field.name,
                                      description=field.__doc__)
        else:
            schema = JsonSchemaObject()

        if isinstance(field, StringField):
            schema.type = SimpleTypes.STRING
            if isinstance(field, StringIdField):
                schema.minLength = 1
        elif isinstance(field, BooleanField):
            schema.type = SimpleTypes.BOOLEAN
        elif isinstance(field, IntegerField):
            schema.type = SimpleTypes.INTEGER
        elif isinstance(field, FloatField):
            schema.type = SimpleTypes.NUMBER
        elif isinstance(field, TimeField):
            schema.type = SimpleTypes.STRING
            schema.format = 'time'
        elif isinstance(field, DateField):
            schema.type = SimpleTypes.STRING
            schema.format = 'date'
        elif isinstance(field, DateTimeField):
            schema.type = SimpleTypes.STRING
            schema.format = 'date-time'
        elif isinstance(field, TimedeltaField):
            schema.type = SimpleTypes.NUMBER
        elif isinstance(field, EnumField):
            values = [v for v in field.enum_class.__members__.values()]
            if all([isinstance(v, (int, float)) for v in values]):
                schema.type = SimpleTypes.NUMBER
            else:
                schema.type = SimpleTypes.STRING

            schema.enum = values
        elif isinstance(field, ArrayField):
            schema.type = SimpleTypes.ARRAY

            schema.items = self.map_field_type(field.field_type, metadata=False)
        elif isinstance(field, MultiTypeField):
            schema.anyOf = [self.map_field_type(f, metadata=False)
                            for f in field.field_types]
        elif isinstance(field, ModelField):
            schema.type = SimpleTypes.OBJECT

            self.generate_from_model(field.model_class, schema=schema)

            if isinstance(field, HashMapField):
                schema.additionalProperties = self.map_field_type(field.field_type, metadata=False)
        elif isinstance(field, BytesField):
            schema.type = SimpleTypes.STRING
            schema.contentEncoding = 'base64'

        if field.json_schema:
            schema.import_data(field.json_schema)
        return schema

    def map_multitype_with_multivalidator(self,
                                          field_obj: MultiTypeField,
                                          field_validator: SomeMixin) -> JsonSchemaObject:
        schemas = []
        for f in field_obj.field_types:
            f_schema = self.map_field_type(f, metadata=False)

            for v in field_validator.validators:
                if not self.is_compatible_validator(f, v):
                    continue
                f_schema = self.map_validate_field(f_schema, v, f)

            schemas.append(f_schema)

        schema = JsonSchemaObject(default=field_obj.default if not callable(field_obj.default) else field_obj.default(),
                                  title=field_obj.name,
                                  description=field_obj.__doc__)

        schema.anyOf = schemas
        return schema

    def is_compatible_validator(self, field_obj: BaseField, field_validator: BaseValidator) -> bool:
        if isinstance(field_validator, ModelValidateMixin):
            return isinstance(field_obj, ModelField) and issubclass(field_obj.model_class,
                                                                    field_validator.__modelclass__)
        if isinstance(field_validator,
                      (Regexp, IPAddress,
                       MacAddress, URL, UUID,
                       NotEmptyString, StringNotContaining)):
            return isinstance(field_obj, StringField)
        if isinstance(field_validator, Length):
            return isinstance(field_obj, (StringField, ArrayField, HashMapField, ModelField))
        if isinstance(field_validator, BaseValueIterableMixin):
            return isinstance(field_obj, (ArrayField, HashMapField, ModelField))
        if isinstance(field_validator, BaseSpecMixin):
            return isinstance(field_obj, (HashMapField, ModelField))
        return True
