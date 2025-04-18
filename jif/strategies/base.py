from abc import ABC, abstractmethod
from PIL import Image
from ..core.types import JamConfig

class NoiseStrategy(ABC):
    @abstractmethod
    def apply(self, text: str, config: JamConfig) -> Image.Image:
        """apply noise strategy to text and return image"""
        pass
