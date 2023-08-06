from typing import Type

from dirty_models import BaseModel
from dirty_models.utils import ModelFormatterIter
from dirty_validators.complex import ModelValidateMixin

from .builder import Builder

__version__ = '0.2.3'


def create_schema_from_validator(validator: Type[ModelValidateMixin], *,
                                 def_read_only: bool = False,
                                 def_writable_only_on_creation: bool = True,
                                 builder_cls: Type[Builder] = Builder):
    builder = builder_cls(def_read_only=def_read_only, def_writable_only_on_creation=def_writable_only_on_creation)

    return ModelFormatterIter(builder.generate_from_model_validator(validator=validator)).format()


def create_schema_from_model(model: Type[BaseModel], *,
                             def_read_only: bool = True,
                             def_writable_only_on_creation: bool = True,
                             builder_cls: Type[Builder] = Builder):
    builder = builder_cls(def_read_only=def_read_only, def_writable_only_on_creation=def_writable_only_on_creation)

    return ModelFormatterIter(builder.generate_from_model(model_class=model)).format()
