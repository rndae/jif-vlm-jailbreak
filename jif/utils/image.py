import numpy as np
from PIL import Image, ImageFont, ImageDraw
import sys
import os

def check_environment():
    """check current environment and dependencies"""
    print(f"Python executable: {sys.executable}")
    print(f"Python version: {sys.version}")
    
    try:
        from PIL import __version__ as pil_version
        print("PIL version:", pil_version)
    except:
        print("PIL version: installed (version unknown)")
    
    print("\nPYTHONPATH:")
    for p in sys.path:
        print(f"  {p}")

import numpy as np
from PIL import Image, ImageFont

def get_default_font(size: int = 40) -> ImageFont:
    """get default font for text rendering"""
    return ImageFont.load_default()

def add_noise_to_image(img: np.ndarray, noise: np.ndarray, intensity: float) -> np.ndarray:
    """add noise to image with given intensity"""
    scaled_noise = noise * intensity * 255
    noisy_img = np.clip(img + scaled_noise[..., None], 0, 255).astype(np.uint8)
    return noisy_img

def text_to_points(text: str, density: float = 0.5) -> np.ndarray:
    """convert text to point cloud representation"""
    img = Image.new('L', (800, 400), color='white')
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), text, font=get_default_font(), fill='black')
    
    # convert to numpy array and find text pixels
    img_array = np.array(img)
    text_pixels = np.column_stack(np.where(img_array < 128))
    
    # sample points based on density
    num_points = int(len(text_pixels) * density)
    if num_points > 0:
        indices = np.random.choice(len(text_pixels), num_points)
        return text_pixels[indices]
    return np.array([[0, 0]])  # fallback

def create_text_image(
    text: str,
    width: int = 800,
    height: int = 400,
    font_size: int = 40,
    bg_color: str = 'white',
    text_color: str = 'black'
) -> Image.Image:
    """Create image with text centered and scaled to fit"""
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    font = get_default_font(font_size)
    
    # Calculate text size and position
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Scale font size if text is too wide
    if text_width > width * 0.9:
        font_size = int(font_size * (width * 0.9) / text_width)
        font = get_default_font(font_size)
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    
    # Center text
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    draw.text((x, y), text, font=font, fill=text_color)
    return img

def add_noise_efficient(img: np.ndarray, noise_type: str = 'gaussian', intensity: float = 0.5) -> np.ndarray:
    """Add noise efficiently using vectorized operations"""
    if noise_type == 'pink':
        # Generate pink noise using 1/f spectrum
        rows, cols = img.shape[:2]
        f_rows = np.fft.fftfreq(rows)
        f_cols = np.fft.fftfreq(cols)
        f_2d = np.sqrt(np.outer(f_rows**2, f_cols**2))
        S = 1 / np.where(f_2d == 0, float('inf'), np.abs(f_2d))
        noise_2d = np.fft.ifft2(np.random.randn(rows, cols) * np.sqrt(S))
        noise = np.real(noise_2d)
        noise = np.repeat(noise[:, :, np.newaxis], 3, axis=2)
        noisy = np.clip(img + noise * intensity * 127, 0, 255).astype(np.uint8)
    elif noise_type == 'speckle':
        noise = np.random.normal(0, intensity, img.shape)
        noisy = np.clip(img * (1 + noise), 0, 255).astype(np.uint8)
    else:  # gaussian
        noise = np.random.normal(0, intensity * 50, img.shape)
        noisy = np.clip(img + noise, 0, 255).astype(np.uint8)
    return noisy
