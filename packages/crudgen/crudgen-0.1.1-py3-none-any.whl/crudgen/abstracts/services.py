from collections import defaultdict

from .abc import AbstractBaseService, AbstractBaseApp, ABC
from .apps import BaseApp


class BaseSimpleRestService(AbstractBaseService, ABC):
    # TODO: indicate type of this dictionary should be App at 2020-10-25 by pooria
    _app_choices = {
        "default": None
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.relation_targets = defaultdict(list)

    def register_app(self, app):
        super().register_app(app)
        if isinstance(app, BaseApp):
            for target, fields in app.relation_targets.items():
                self.relation_targets[target].extend(fields)

    def resolve_relation_targets(self):
        for target, fields in self.relation_targets.items():
            app_name, model_name = target.split('.')
            target_app = self.get_app(app_name)
            target_model = target_app.get_model(model_name)
            for field in fields:
                field.target_app = target_app
                field.target_model = target_model

                related_field_class = type(target_model).get_field_type("related_field")
                related_field = related_field_class(name=field.related_name, field_type='related_field',
                                                    target_app=field.model.app, target_model=field.model)
                target_model.register_field(related_field)


    @classmethod
    def from_dict(cls, data: dict):
        apps = data.get('apps')
        deploy_strategy = data.get('deploy_strategy')
        name = data.get('name')
        service = cls(name=name, deploy_strategy=deploy_strategy)

        for app in apps:
            app_class = cls._app_choices.get(app.get('app_type', 'default'))
            if app_class is None:
                raise Exception("app_type not supported")
            assert issubclass(app_class, AbstractBaseApp), "app class should be subclass of AbstractBaseApp"
            service.register_app(app_class.from_dict(app))
        service.resolve_relation_targets()
        return service
