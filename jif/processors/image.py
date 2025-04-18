import numpy as np
from PIL import Image
from ..core.processors import ImageProcessor
from ..core.types import JamConfig
from ..strategies.speckle import SpeckleNoise
from ..strategies.point_cloud import PointCloudNoise
from ..utils.image import create_text_image

class SpeckleProcessor(ImageProcessor):
    """Delegates to SpeckleNoise strategy"""
    def __init__(self):
        self.strategy = SpeckleNoise()
    
    def process(self, text: str, config: JamConfig) -> Image.Image:
        return self.strategy.apply(text, config)

class PointCloudProcessor(ImageProcessor):
    """Delegates to PointCloudNoise strategy"""
    def __init__(self):
        self.strategy = PointCloudNoise()
    
    def process(self, text: str, config: JamConfig) -> Image.Image:
        return self.strategy.apply(text, config)

class NoneImageProcessor(ImageProcessor):
    """Creates basic text image without noise"""
    def process(self, text: str, config: JamConfig) -> Image.Image:
        return create_text_image(
            text=text,
            font_size=100,
            bg_color='white',
            text_color='black',
            padding=12
        )
