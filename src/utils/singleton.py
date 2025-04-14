from PIL import Image
from typing import Optional, Union
from ..models.falcon import FalconModel
from ..models.granite import GraniteModel
from ..models.domain import Question

class SingletonMeta(type):
    """
    A singleton metaclass that ensures only one instance of a class is created.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Falcon(metaclass=SingletonMeta):
    def __init__(self, model_type="falcon"):
        self._falcon_model = None
        self._granite_model = None
        self._current_model_type = model_type.lower()
        self._initialize_selected_model()

    def _initialize_selected_model(self):
        if self._current_model_type == "granite" and not self._granite_model:
            from ..models.granite import GraniteModel
            self._granite_model = GraniteModel()
            self._current_model = self._granite_model
        else:  # default to falcon
            from ..models.falcon import FalconModel
            self._falcon_model = FalconModel()
            self._current_model = self._falcon_model

    def switch_model(self, model_name: str):
        """Switch between available models"""
        model_name = model_name.lower()
        if model_name != self._current_model_type:
            self._current_model_type = model_name
            self._initialize_selected_model()

    def ask(self, text: str, image: Optional[Image.Image] = None, is_figstep: bool = False) -> str:
        question = Question(text=text, image=image, is_figstep=is_figstep)
        return self._current_model.generate_response(question).text