import numpy as np
from PIL import Image, ImageDraw, ImageFont
from .base import NoiseStrategy
from ..core.types import JamConfig
from ..utils.image import get_default_font

class PointCloudNoise(NoiseStrategy):
    def _get_text_points(self, text: str, font: ImageFont.ImageFont) -> np.ndarray:
        """Get points that form the text"""
        img = Image.new('L', (800, 800), color='white')  # Square dimensions
        draw = ImageDraw.Draw(img)
        
        # Draw text with consistent padding
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        x = 12 if text_width > 776 else (800 - text_width) // 2  # 776 = 800 - 2*12
        y = 12
        draw.text((x, y), text, font=font, fill='black')
        
        # Convert to points
        pixels = np.array(img)
        points = np.column_stack(np.where(pixels < 128))
        
        return points

    def apply(self, text: str, config: JamConfig) -> Image.Image:
        font = get_default_font(size=60)
        points = self._get_text_points(text, font)
        
        if len(points) == 0:
            return Image.new('RGB', (800, 400), 'white')
            
        # Add 3D coordinates
        num_points = len(points)
        z = np.sin(points[:, 0] / 100) * 20 * config.image_noise_level  # Use image noise
        points_3d = np.column_stack([points, z])
        
        # Generate colors based on 3D position
        colors = np.zeros((num_points, 3), dtype=np.uint8)
        colors[:, 0] = np.interp(points_3d[:, 0], (0, 800), (50, 255))  # R
        colors[:, 1] = np.interp(points_3d[:, 1], (0, 400), (50, 255))  # G
        colors[:, 2] = np.interp(points_3d[:, 2], (z.min(), z.max()), (50, 255))  # B
        
        # Sort by Z for proper depth
        z_order = points_3d[:, 2].argsort()
        points = points[z_order]
        colors = colors[z_order]
        
        # Create image
        img = Image.new('RGB', (800, 400), 'white')
        for (x, y), color in zip(points, colors):
            x = int(x)
            y = int(y)
            img.putpixel((x, y), tuple(color))
            
        return img
