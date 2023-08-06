from .abc import AbstractBaseEndpoint, ABC


class SimpleDataAccessEndpoint(AbstractBaseEndpoint, ABC):
    nested_endpoints = {
        "nested_many_simple_data_access": None,
        "nested_foreign_simple_data_access": None
    }

    def assign_app(self, app):
        self.app = app

    @classmethod
    def validate_data(cls, data):
        # TODO: do some validation here at 2020-10-16 by pooria
        pass

    @classmethod
    def from_dict(cls, data: dict):
        cls.validate_data(data)
        path = data.get('path')
        model = data.get('model')
        serializer = data.get('serializer')
        endpoint = cls(model=model, serializer=serializer, path=path)
        actions = data.get('actions', [])
        for action in actions:
            nested_endpoint_type = action['endpoint_type']
            nested_endpoint_class = cls.nested_endpoints[nested_endpoint_type]
            endpoint.register_action(nested_endpoint_class.from_dict(action))
        return endpoint


class NestedManySimpleDataAccessEndpoint(SimpleDataAccessEndpoint, ABC):

    def __init__(self, parent_field, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__parent_field = parent_field

    @property
    def parent_field(self):
        return self.model.get_field(self.__parent_field)

    @classmethod
    def validate_data(cls, data):
        # TODO: do some validation here at 2020-10-16 by pooria
        pass

    @classmethod
    def from_dict(cls, data: dict):
        cls.validate_data(data)
        path = data.get('path')
        model = data.get('model')
        serializer = data.get('serializer')
        parent_field = data['parent_field']
        endpoint = cls(model=model, parent_field=parent_field, serializer=serializer, path=path)
        return endpoint


class NestedForeignSimpleDataAccessEndpoint(SimpleDataAccessEndpoint, ABC):
    pass


class BaseAddToManyRelationEndpoint(AbstractBaseEndpoint, ABC):

    def __init__(self, parent_field, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__parent_field = parent_field

    @property
    def parent_field(self):
        return self.parent.model.get_field(self.__parent_field)

    @staticmethod
    def needs_router():
        return False

    def assign_app(self, app):
        self.app = app

    @classmethod
    def validate_data(cls, data: dict):
        return

    @classmethod
    def from_dict(cls, data: dict):
        cls.validate_data(data)
        path = data.get('path')
        model = data.get('model')
        parent_field = data['parent_field']
        endpoint = cls(model=model, parent_field=parent_field, serializer=None, path=path)
        return endpoint


class BaseRemoveFromManyRelationEndpoint(BaseAddToManyRelationEndpoint, ABC):
    pass
