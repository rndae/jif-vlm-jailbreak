import os
from PIL import Image
import argparse
from typing import Tuple, Optional
import sys

def optimize_image(image: Image.Image, size: Tuple[int, int] = (128, 128)) -> Image.Image:
    """Optimize image by resizing and converting to grayscale"""
    if image.mode != 'L':
        image = image.convert('L')
    
    image.thumbnail(size, Image.Resampling.LANCZOS)
    
    return image

def process_directory(input_dir: str, output_dir: Optional[str] = None, size: Tuple[int, int] = (128, 128)):
    """Process all PNG images in a directory"""
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(input_dir), "optimized")
    
    os.makedirs(output_dir, exist_ok=True)
    
    total_files = 0
    processed_files = 0
    total_size_before = 0
    total_size_after = 0

    print(f"Processing images in {input_dir}...")
    print(f"Saving optimized images to {output_dir}")
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.png'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.jpg')
            
            total_files += 1
            total_size_before += os.path.getsize(input_path)
            
            try:
                with Image.open(input_path) as img:
                    optimized = optimize_image(img, size)
                    optimized.save(output_path, 'JPEG', quality=75, optimize=True)
                    
                total_size_after += os.path.getsize(output_path)
                processed_files += 1
                print(f"Processed: {filename} -> {os.path.basename(output_path)}")
                
            except Exception as e:
                print(f"Error processing {filename}: {e}")
    
    if total_files > 0:
        print("\nSummary:")
        print(f"Files processed: {processed_files}/{total_files}")
        print(f"Total size before: {total_size_before / 1024:.2f}KB")
        print(f"Total size after: {total_size_after / 1024:.2f}KB")
        print(f"Size reduction: {((total_size_before - total_size_after) / total_size_before) * 100:.1f}%")

def main():
    parser = argparse.ArgumentParser(description='Batch optimize images: resize and convert PNG to JPG')
    parser.add_argument('input_dir', help='Input directory containing PNG images')
    parser.add_argument('--output_dir', help='Output directory for optimized images')
    parser.add_argument('--size', type=int, nargs=2, default=[128, 128],
                      help='Output size (width height), default: 128 128')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_dir):
        print(f"Error: Directory not found: {args.input_dir}")
        sys.exit(1)
        
    process_directory(args.input_dir, args.output_dir, tuple(args.size))

if __name__ == "__main__":
    main()
