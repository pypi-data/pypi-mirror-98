from abc import ABC
from .abc import AbstractBaseField


class BaseCharField(AbstractBaseField, ABC):

    def __init__(self, max_length, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_length = max_length

    @classmethod
    def validate_data(cls, data, raise_exception=True):
        assert data.get("field_type", None) == "CharField"
        # TODO: do some validation here at 2020-10-16 by pooria
        pass

    @classmethod
    def from_dict(cls, data: dict):
        cls.validate_data(data, raise_exception=True)
        return cls(**data)


class BaseBooleanField(AbstractBaseField, ABC):

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class BaseForeignKey(AbstractBaseField, ABC):

    def __init__(self, target, related_name=None, related_query_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target = target
        self.related_name = related_name
        self.related_query_name = related_query_name
        self.target_app = None
        self.target_model = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class BaseManyToMany(AbstractBaseField, ABC):

    def __init__(self, target, related_name=None, related_query_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target = target
        self.related_name = related_name
        self.related_query_name = related_query_name
        self.target_app = None
        self.target_model = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


class BaseRelatedField(AbstractBaseField, ABC):

    def __init__(self, target_app, target_model, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_app = target_app
        self.target_model = target_model
