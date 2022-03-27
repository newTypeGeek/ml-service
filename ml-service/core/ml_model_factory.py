from schema import ModelType
from . import model


class MLModelFactory:
    def __init__(self):
        self._models = {}
        self.register_model(ModelType.linear_regressor, model.Linear)
        self.register_model(ModelType.random_forest, model.RandomForest)

    def register_model(self, model_name: ModelType, model_class):
        self._models[model_name] = model_class

    def create_model(self, model_name: ModelType, **kwargs):
        return self._models[model_name](**kwargs)

