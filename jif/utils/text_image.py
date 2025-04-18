import os 
import requests
from io import BytesIO
import random
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def get_random_image(size=(40, 40)):
    """fetch random image or use local fallback"""
    try:
        response = requests.get(f"https://picsum.photos/{size[0]}")
        img = Image.open(BytesIO(response.content))
        return img.resize(size)
    except:
        # fallback to local images
        fallback_dir = os.path.join(os.path.dirname(__file__), "..", "random-images")
        if os.path.exists(fallback_dir):
            files = [f for f in os.listdir(fallback_dir) if f.endswith(('.jpg', '.png'))]
            if files:
                img_path = os.path.join(fallback_dir, random.choice(files))
                return Image.open(img_path).resize(size)
        
        # create random noise image as last resort
        return Image.fromarray(
            np.random.randint(0, 255, (*size, 3), dtype=np.uint8)
        )

def replace_chars_with_images(text: str, noise_level: float = 0.5) -> Image.Image:
    """replace characters with small random images based on noise level"""
    char_height = 40
    char_width = 40
    spacing = 5
    
    # Clean text - remove special tokens
    text = text.replace('[CLS]', '').replace('[SEP]', '').strip()
    
    # calculate total width needed
    total_width = len(text) * (char_width + spacing)
    img = Image.new('RGB', (total_width, char_height), 'white')
    
    x = 0
    for char in text:
        if char.lower() in 'aeiou' and random.random() < noise_level:
            # replace vowels with random images
            char_img = get_random_image((char_width, char_height))
        elif random.random() < noise_level * 0.5:
            # replace other chars with probability proportional to noise
            char_img = get_random_image((char_width, char_height))
        else:
            # create image with character
            char_img = Image.new('RGB', (char_width, char_height), 'white')
            draw = ImageDraw.Draw(char_img)
            font = ImageFont.load_default()
            bbox = font.getbbox(char)
            w = bbox[2] - bbox[0]
            h = bbox[3] - bbox[1]
            x_pos = (char_width - w) // 2
            y_pos = (char_height - h) // 2
            draw.text((x_pos, y_pos), char, fill='black', font=font)
            
        img.paste(char_img, (x, 0))
        x += char_width + spacing
        
    return img
