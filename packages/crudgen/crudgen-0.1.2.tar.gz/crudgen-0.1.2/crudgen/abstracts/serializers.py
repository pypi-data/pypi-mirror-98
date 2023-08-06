from .abc import AbstractBaseSerializer, ABC


class BaseSerializer(AbstractBaseSerializer, ABC):

    @classmethod
    def from_dict(cls, data: dict):
        name = data.get('name')
        fields = data.get('fields')
        extras = data.get('extras')
        return cls(name=name, field_names=fields, extras=extras)
