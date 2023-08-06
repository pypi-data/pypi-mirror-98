import logging
from collections import defaultdict

from .abc import AbstractBaseApp, AbstractBaseEndpoint, AbstractBaseModel, ABC
from .models import DBModel


logger = logging.getLogger(__name__)


class BaseApp(AbstractBaseApp, ABC):

    _model_choices = {
        "DBModel": None
    }

    _endpoint_choices = {
        "simple_data_access": None
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.relation_targets = defaultdict(list)

    def register_model(self, model):
        super().register_model(model)
        if isinstance(model, DBModel):
            for target, fields in model.relation_targets.items():
                self.relation_targets[target].extend(fields)

    @classmethod
    def validate_data(cls, data, raise_exception):
        # TODO: do some validations here too at 2020-10-16 by pooria
        pass

    @classmethod
    def find_serializer_by_name(cls, serializer_name, models):
        for model in models:
            for serializer in model.serializers:
                if serializer.name == serializer_name:
                    return serializer
        # TODO: raise exception for model not found at 2020-10-16 by pooria

    @classmethod
    def from_dict(cls, data: dict):
        # TODO: make a decision about path at 2020-10-16 by pooria
        cls.validate_data(data, raise_exception=True)
        name = data['name']
        namespace = data['namespace']
        app = cls(name=name, namespace=namespace)
        for model in data['models']:
            logger.info(model)
            model_class = cls._model_choices.get(model.get('model_type', 'default'))
            if model_class is None:
                raise Exception(f"model_type: {model.get('model_type')} is not supported")
            assert issubclass(model_class, AbstractBaseModel)
            app.register_model(model_class.from_dict(model))

        for endpoint in data['endpoints']:
            logger.info(endpoint)
            endpoint_class = cls._endpoint_choices.get(endpoint.get('endpoint_type', 'simple_data_access'))
            if endpoint_class is None:
                raise Exception(f"endpoint_type: {endpoint.get('endpoint_type')} is not supported")
            assert issubclass(endpoint_class, AbstractBaseEndpoint)
            app.register_endpoint(endpoint_class.from_dict(endpoint))

        return app
