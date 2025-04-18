import numpy as np
from PIL import Image, ImageDraw
from scipy import signal
from .base import NoiseStrategy
from ..core.types import JamConfig
from ..utils.image import create_text_image, add_noise_efficient

class SpeckleNoise(NoiseStrategy):
    def _generate_pink_noise(self, shape: tuple) -> np.ndarray:
        """Generate 2D pink noise with proper broadcasting"""
        rows, cols = shape[:2]
        
        # Create 2D frequency coordinates
        fx = np.fft.fftfreq(cols)
        fy = np.fft.fftfreq(rows)
        
        # Create 2D frequency grid
        fx, fy = np.meshgrid(fx, fy)
        
        # Calculate frequency distances from center
        distances = np.sqrt(fx*fx + fy*fy)
        
        # Avoid division by zero at DC component
        distances[0,0] = 1.0
        
        # Create pink noise spectrum
        spectrum = 1.0 / distances
        spectrum[0,0] = 0.0  # Remove DC component
        
        # Generate random phase
        phase = np.random.uniform(0, 2*np.pi, (rows, cols))
        
        # Combine magnitude and phase
        freq_data = spectrum * (np.cos(phase) + 1j * np.sin(phase))
        
        # Inverse FFT and take real part
        noise = np.real(np.fft.ifft2(freq_data))
        
        # Normalize
        noise = (noise - noise.min()) / (noise.max() - noise.min())
        return noise

    def apply(self, text: str, config: JamConfig) -> Image.Image:
        # Create dark gray background with black text
        bg_color = (10, 10, 10)  # Very dark gray
        text_color = (0, 0, 0)   # Black
        
        img = create_text_image(
            text, 
            width=800, 
            height=800,
            font_size=100,
            bg_color=bg_color,
            text_color=text_color,
            padding=12
        )
        img_array = np.array(img)
        
        # Generate base noise
        if config.distribution == 'pink':
            noise_2d = self._generate_pink_noise(img_array.shape[:2])
            noise = np.stack([noise_2d] * 3, axis=-1)
        else:
            noise = np.random.normal(0, 0.5, img_array.shape)  # Reduced base intensity
        
        # Apply uniform noise across the image
        noisy_img = np.clip(
            img_array + noise * config.syntactic_noise * 127,  # Scale factor reduced for subtler effect
            0, 255
        ).astype(np.uint8)
        
        return Image.fromarray(noisy_img)
