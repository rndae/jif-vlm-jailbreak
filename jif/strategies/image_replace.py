from PIL import Image, ImageDraw, ImageFont
import numpy as np
from .base import NoiseStrategy
from ..core.types import JamConfig
from ..utils.text_image import get_random_image
from ..utils.image import get_default_font

class ImageReplaceNoise(NoiseStrategy):
    def apply(self, text: str, config: JamConfig) -> Image.Image:
        char_size = 60
        spacing = 10
        padding = 20
        
        # Calculate dimensions
        text_width = (char_size + spacing) * len(text) - spacing + 2 * padding
        text_height = char_size + 2 * padding
        
        # Create base image
        img = Image.new('RGB', (text_width, text_height), 'white')
        x = padding
        
        # Process each character
        for char in text:
            if (char.lower() in 'aeiou' and np.random.random() < config.syntactic_noise) or \
               (char.isalnum() and np.random.random() < config.syntactic_noise * 0.5):
                # Replace with random image
                char_img = get_random_image((char_size, char_size))
            else:
                # Draw character
                char_img = Image.new('RGB', (char_size, char_size), 'white')
                draw = ImageDraw.Draw(char_img)
                font = get_default_font(size=char_size-10)
                # Center character
                bbox = font.getbbox(char)
                char_x = (char_size - (bbox[2] - bbox[0])) // 2
                char_y = (char_size - (bbox[3] - bbox[1])) // 2
                draw.text((char_x, char_y), char, font=font, fill='black')
            
            img.paste(char_img, (x, padding))
            x += char_size + spacing
            
        return img
