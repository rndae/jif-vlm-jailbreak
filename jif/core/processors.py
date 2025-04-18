from abc import ABC, abstractmethod
from typing import Optional, Tuple
from PIL import Image
from .types import JamConfig

class TextProcessor(ABC):
    @abstractmethod
    def process(self, text: str, config: JamConfig) -> str:
        """Process text and return modified text"""
        pass

class SemanticProcessor(TextProcessor):
    """Base class for semantic noise processors"""
    pass

class SyntacticProcessor(TextProcessor):
    """Base class for syntactic noise processors"""
    pass

class ImageProcessor(ABC):
    @abstractmethod
    def process(self, text: str, config: JamConfig) -> Image.Image:
        """Convert text to image with optional noise"""
        pass

class DefaultImageProcessor(ImageProcessor):
    """Default processor that creates basic text image"""
    def process(self, text: str, config: JamConfig) -> Image.Image:
        from ..utils.image import create_text_image
        return create_text_image(
            text=text,
            font_size=100,
            bg_color='white',
            text_color='black',
            padding=12
        )
