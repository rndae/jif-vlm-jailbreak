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
    try:
        # Try to get system Arial font first
        font_path = os.path.join(os.environ.get('SystemRoot', 'C:\\Windows'), 'Fonts', 'Arial.ttf')
        return ImageFont.truetype(font_path, size)
    except:
        # Fallback to default, but scale up the size since default font is small
        return ImageFont.load_default().font_variant(size=size * 3)

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
    height: int = 800,
    font_size: int = 200,  # Much larger default font size
    bg_color: str = 'white',
    text_color: str = 'black',
    padding: int = 12
) -> Image.Image:
    """Create square image with text in a textbox format"""
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Start with large font size and adjust if needed
    current_font_size = font_size
    while current_font_size > 40:  # Don't go smaller than 40
        font = get_default_font(current_font_size)
        
        # Split on explicit line breaks first
        paragraphs = text.split('\n')
        lines = []
        max_width = width - (2 * padding)
        
        for paragraph in paragraphs:
            if not paragraph:  # Empty line
                lines.append('')
                continue
                
            # Word wrap within each paragraph
            words = paragraph.split()
            current_line = []
            
            for word in words:
                test_line = ' '.join(current_line + [word])
                bbox = font.getbbox(test_line)
                if bbox[2] <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]
        
            if current_line:
                lines.append(' '.join(current_line))
        
        # Calculate line spacing with extra room for empty lines
        line_height = int(current_font_size * 1.5)  # Increased from 1.2
        total_height = line_height * len(lines)
        
        # If text fits, draw it; otherwise try smaller font
        if total_height <= height - (2 * padding):
            y = padding
            for line in lines:
                bbox = font.getbbox(line)
                x = padding
                draw.text((x, y), line, font=font, fill=text_color)
                y += line_height
            break
        
        current_font_size = int(current_font_size * 0.8)
    
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
