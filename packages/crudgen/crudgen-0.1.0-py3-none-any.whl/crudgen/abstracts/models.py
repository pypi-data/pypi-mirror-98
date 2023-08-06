import logging
from collections import defaultdict

from .abc import AbstractBaseModel, AbstractBaseSerializer, AbstractBaseField, ABC

from .fields import BaseForeignKey, BaseManyToMany

logger = logging.getLogger(__name__)


class DBModel(AbstractBaseModel, ABC):

    _field_choices = {
        "CharField": None,
        "ForeignKey": None,
        "ManyToMany": None
    }

    _serializer_choices = {
        "default": None
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.relation_targets = defaultdict(list)

    @classmethod
    def get_field_type(cls, field_type):
        return cls._field_choices.get(field_type)

    def register_field(self, field):
        super().register_field(field)
        if isinstance(field, (BaseForeignKey, BaseManyToMany)):
            self.relation_targets[field.target].append(field)

    @classmethod
    def validate_data(cls, data, raise_exception):
        # TODO: do some validations here too at 2020-10-16 by pooria
        pass

    @classmethod
    def from_dict(cls, data: dict):
        cls.validate_data(data, raise_exception=True)
        name = data['name']
        model = cls(name=name)

        for field in data['fields']:
            field_class = cls._field_choices.get(field['field_type'])
            if field_class is None:
                raise Exception(f"field_type: {field['field_type']} is not supported")
            assert issubclass(field_class, AbstractBaseField)
            model.register_field(field_class.from_dict(field))
            logger.debug(field)

        for serializer in data['serializers']:
            # TODO: serializer classes default and stuff at 2020-10-17 by pooria
            serializer_class = cls._serializer_choices.get(serializer.get("serializer_type", "default"))
            if serializer_class is None:
                raise Exception(f"serializer_type: {serializer.get('serializer_type')} is not supported")
            assert issubclass(serializer_class, AbstractBaseSerializer)
            model.register_serializer(serializer_class.from_dict(serializer))

        return model
