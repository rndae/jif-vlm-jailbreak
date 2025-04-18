import numpy as np
from PIL import Image, ImageDraw
from scipy import signal
from .base import NoiseStrategy
from ..core.types import JamConfig
from ..utils.image import create_text_image, add_noise_efficient

class SpeckleNoise(NoiseStrategy):
    def apply(self, text: str, config: JamConfig) -> Image.Image:
        # Create text image with black background and white text for better noise visibility
        img = create_text_image(text, font_size=60, bg_color='black', text_color='white')
        img_array = np.array(img)
        
        # Generate and apply noise
        if config.distribution == 'pink':
            rows, cols = img_array.shape[:2]
            f = np.fft.fftfreq(rows)
            S = 1 / np.where(f == 0, float('inf'), np.abs(f))
            noise = np.real(np.fft.ifft(np.random.randn(rows, cols) * np.sqrt(S)))
            noise = np.repeat(noise[:, :, np.newaxis], 3, axis=2)
        else:
            noise = np.random.normal(0, 1, img_array.shape)
            
        # Scale noise based on intensity
        scaled_noise = noise * (config.syntactic_noise * 255)
        
        # Apply noise differently to text and background
        text_mask = (img_array == 255).all(axis=2)  # Find white text pixels
        noisy_img = img_array.copy()
        
        # Add noise to text pixels (white)
        noisy_img[text_mask] = np.clip(
            img_array[text_mask] + scaled_noise[text_mask], 
            0, 255
        ).astype(np.uint8)
        
        # Add noise to background pixels (black)
        noisy_img[~text_mask] = np.clip(
            img_array[~text_mask] + scaled_noise[~text_mask] * 0.5,  # Less noise on background
            0, 255
        ).astype(np.uint8)
        
        return Image.fromarray(noisy_img)
