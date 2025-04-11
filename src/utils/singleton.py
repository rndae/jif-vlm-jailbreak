from PIL import Image
from typing import Optional, Union
from ..models.falcon import FalconModel
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
    def __init__(self):
        self._model = FalconModel()

    def ask(self, text: str, image: Optional[Image.Image] = None, is_figstep: bool = False) -> str:
        question = Question(text=text, image=image, is_figstep=is_figstep)
        answer = self._model.generate_response(question)
        return answer.text