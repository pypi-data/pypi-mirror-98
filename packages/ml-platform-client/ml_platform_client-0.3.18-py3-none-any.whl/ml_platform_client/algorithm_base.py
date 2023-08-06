from .util import generate_uuid
from .train_manager import train_manager


class PredictorBase:
    def __init__(self, model):
        self.model = model

    def predict(self, features: dict, params: dict):
        raise NotImplemented


class AlgorithmBase:
    def train(self, model_id: str, model_path: str, data_config: dict, parameters: dict, extend: dict):
        raise NotImplemented

    def load(self, model_id: str, model_path: str) -> PredictorBase:
        raise NotImplemented

    def unload(self, model_id):
        pass

    def status(self, model_id):
        return train_manager.check(model_id)

    def delete(self, model_id):
        raise NotImplemented

    def generate_model_id(self, extend: dict):
        return generate_uuid()
