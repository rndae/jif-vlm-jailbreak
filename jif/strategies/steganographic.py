import numpy as np
from PIL import Image, ImageDraw, ImageFont
from .base import NoiseStrategy
from ..core.types import JamConfig

class SteganographicNoise(NoiseStrategy):
    def apply(self, text: str, config: JamConfig) -> Image.Image:
        # create base image
        img = Image.new('RGB', (800, 400), color='white')
        draw = ImageDraw.Draw(img)
        
        # inject steganographic noise
        np.random.seed(42)
        pixels = np.array(img)
        noise_mask = np.random.rand(*pixels.shape[:2]) < config.syntactic_noise
        
        # encode text with bit manipulation
        encoded_text = ''.join(chr(ord(c) ^ 0x33) for c in text)
        
        # draw encoded text
        font = ImageFont.load_default()
        draw.text((10, 10), encoded_text, font=font, fill='black')
        
        return img
