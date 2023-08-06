from abc import ABC, abstractmethod


class AbstractBaseCommon(ABC):

    @property
    @abstractmethod
    def code(self):
        pass

    @abstractmethod
    def transform(self, **kwargs):
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        pass

    # @abstractmethod
    # def to_json(self):
    #     pass


class AbstractBaseField(AbstractBaseCommon, ABC):

    def __init__(self, name, field_type, model=None):
        super().__init__()
        self.name = name
        self.field_type = field_type
        self.model = model

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, model):
        self.__model = model

    def transform(self):
        return self.code


class AbstractBaseSerializer(AbstractBaseCommon, ABC):

    def __init__(self, name, field_names, extras=None, model=None, fields=None):
        super().__init__()
        self.name = name
        self.field_names = field_names
        self.extras = extras or {}
        self.__fields = []
        self.model = model

    @property
    def fields(self):

        if not self.__fields:
            for field_name in self.field_names:
                extra = self.extras.get('field_name')
                if extra:
                    field_name = extra.get('source') or field_name
                self.__fields.append(self.model.get_field(field_name))
        return self.__fields

    @property
    def model(self):
        return self.__model

    @model.setter
    def model(self, model):
        self.__model = model
        # TODO: check fields against model at 2020-10-25 by pooria

    def transform(self, **kwargs):
        return self.code


class AbstractBaseModel(AbstractBaseCommon, ABC):

    def __init__(self, name, fields=None, app=None, serializers=None):
        super().__init__()
        self.name = name
        if fields is None:
            self.__fields = {}
        else:
            for field in fields:
                self.register_field(field)
        if serializers is None:
            self.__serializers = {}
        else:
            for serializer in serializers:
                self.register_serializer(serializer)
        self.app = app

    @property
    def fields(self):
        return list(self.__fields.values())

    def get_field(self, name):
        return self.__fields[name]

    def register_field(self, field):
        field.model = self
        self.__fields[field.name] = field

    @property
    def serializers(self):
        return list(self.__serializers.values())

    def get_serializer(self, name):
        return self.__serializers[name]

    def register_serializer(self, serializer):
        # TODO: check serializer fields against self serializer at 2020-10-25 by pooria
        serializer.model = self
        self.__serializers[serializer.name] = serializer

    @property
    def app(self):
        return self.__app

    @app.setter
    def app(self, app):
        self.__app = app

    def transform(self):
        return self.code


# TODO: abstract base endpoint should complete at 2020-10-10 by pooria
class AbstractBaseEndpoint(AbstractBaseCommon, ABC):

    def __init__(self, path, model, serializer, app=None):
        super().__init__()
        self.path = path
        self.__model = model
        self.__serializer = serializer
        self.parent = None
        self.__actions = []
        self.app = app

    @property
    def model(self):
        if not isinstance(self.__model, AbstractBaseModel):
            self.__model = self.app.get_model(self.__model)
        return self.__model

    @property
    def serializer(self):
        if not isinstance(self.__serializer, AbstractBaseSerializer):
            self.__serializer = self.model.get_serializer(self.__serializer)
        return self.__serializer

    @staticmethod
    def needs_router():
        return True

    @abstractmethod
    def assign_app(self, app):
        pass

    @property
    def actions(self):
        return self.__actions

    def register_action(self, action):
        action.parent = self
        self.__actions.append(action)

    @property
    def app(self):
        return self.__app

    @app.setter
    def app(self, app):
        self.__app = app

    def transform(self):
        return self.code


class AbstractBaseApp(AbstractBaseCommon, ABC):

    def __init__(self, name, namespace, service=None, models=None, endpoints=None):
        super().__init__()
        self.name = name
        self.namespace = namespace
        if models is None:
            self.__models = {}
        else:
            for model in models:
                self.register_model(model)
        if endpoints is None:
            self.__endpoints = {}
        else:
            for endpoint in endpoints:
                self.register_endpoint(endpoint)
        self.service = service

    @property
    def models(self):
        return list(self.__models.values())

    def get_model(self, name) -> AbstractBaseModel:
        return self.__models[name]

    def register_model(self, model):
        if model.name in self.__models.keys():
            raise ValueError(f"duplicate model in app: {self.name}, model: {model.name}")
        model.app = self
        self.__models[model.name] = model

    @property
    def endpoints(self):
        return list(self.__endpoints.values())

    def get_endpoint(self, path):
        return self.__endpoints[path]

    def register_endpoint(self, endpoint: AbstractBaseEndpoint):
        endpoint.assign_app(self)
        if endpoint.needs_router():
            self.__endpoints[endpoint.path] = endpoint

        for action in endpoint.actions:
            self.register_endpoint(action)


    @property
    def service(self):
        return self.__service

    @service.setter
    def service(self, service):
        self.__service = service


    @property
    def code(self):
        return "this type of object does not necessarily have a code representation"


class AbstractBaseService(AbstractBaseCommon, ABC):

    def __init__(self, name, deploy_strategy, apps=None):
        super().__init__()
        self.name = name
        self.deploy_strategy = deploy_strategy
        if apps is None:
            self.__apps = {}
        else:
            for app in apps:
                self.register_app(app)

    def register_app(self, app):
        if app.name in self.__apps.keys():
            raise KeyError(f"duplicate app name: {app.name}")
        app.service = self
        self.__apps[app.name] = app

    @property
    def apps(self):
        return list(self.__apps.values())

    def get_app(self, name):
        return self.__apps[name]

    @property
    def code(self):
        return "this type of object does not necessarily have a code representation"

