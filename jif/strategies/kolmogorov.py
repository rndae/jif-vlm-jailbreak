import numpy as np
from PIL import Image, ImageDraw
from .base import NoiseStrategy
from ..core.types import JamConfig
from ..utils.image import get_default_font, create_text_image

class KolmogorovNoise(NoiseStrategy):
    def _generate_code(self, text: str) -> str:
        """Generate Python code that prints the text"""
        encodings = [
            f'print("".join(chr(ord(c)^{np.random.randint(1,10)}) for c in "{text}"))',
            f'import re; print(re.sub(r"[a-z]", lambda m: chr((ord(m.group())-97+{np.random.randint(1,26)})%26+97), "{text}"))',
            f'print("".join(map(lambda x: chr((ord(x)-32+{np.random.randint(1,95)})%95+32), "{text}")))'
        ]
        return np.random.choice(encodings)

    def apply(self, text: str, config: JamConfig) -> Image.Image:
        # Generate noisy code version of text
        code = self._generate_code(text)
        print(f"Kolmogorov transformation:\n{code}")
        
        # Create image with code
        return create_text_image(code, width=800, height=400)
