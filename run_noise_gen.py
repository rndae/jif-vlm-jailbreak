import argparse
import os
from datetime import datetime
from PIL import Image
from jif.core.generator import NoiseGenerator
from jif.core.types import JamConfig, NoiseType

def create_comparison_image(images, texts, title="Noise Comparison"):
    """Create a single image showing all variations side by side with labels"""
    n_images = len(images)
    if n_images == 0:
        return None
        
    # Calculate grid layout
    cols = min(3, n_images)
    rows = (n_images + cols - 1) // cols
    
    # Get max dimensions
    max_width = max(img.width for img in images)
    max_height = max(img.height for img in images)
    
    # Create canvas
    canvas_width = cols * (max_width + 20)  # Add padding
    canvas_height = rows * (max_height + 40)  # Add space for text
    canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
    
    # Paste images and add labels
    for idx, (img, text) in enumerate(zip(images, texts)):
        row = idx // cols
        col = idx % cols
        x = col * (max_width + 20)
        y = row * (max_height + 40)
        
        # Paste image
        canvas.paste(img, (x, y))
        
        # Add text label using PIL's ImageDraw
        from PIL import ImageDraw
        draw = ImageDraw.Draw(canvas)
        draw.text((x, y + max_height + 5), text, fill='black')
    
    return canvas

def main():
    parser = argparse.ArgumentParser(description='Generate noisy text images')
    parser.add_argument('text', help='Text to render')
    
    # Method selection arguments
    parser.add_argument('--semantic', 
                       choices=['REGEX', 'LATENT', 'NONE'],
                       default='NONE', 
                       help='Semantic noise method')
    parser.add_argument('--syntactic', choices=['KOLMOGOROV', 'SHUFFLE', 'NONE'],
                      default='NONE', help='Syntactic noise method')
    parser.add_argument('--image-noise', choices=['SPECKLE', 'POINT_CLOUD', 'NONE'],
                      default='NONE', help='Image noise method')
    
    # Separate noise levels
    parser.add_argument('--semantic-noise-lvl', type=float, default=0.5,
                      help='Semantic noise level (0.0-1.0)')
    parser.add_argument('--syntactic-noise-lvl', type=float, default=0.5,
                      help='Syntactic noise level (0.0-1.0)')
    parser.add_argument('--image-noise-lvl', type=float, default=0.5,
                      help='Image noise level (0.0-1.0)')
    
    # Legacy support
    parser.add_argument('--noise-level', type=float, default=None,
                      help='Global noise level (deprecated, use specific levels instead)')
    
    parser.add_argument('--image-replace', action='store_true',
                      help='Use image replacement mode')
    
    parser.add_argument('--output-dir', default='outputs',
                      help='Output directory')
    parser.add_argument('--compare-levels', action='store_true',
                      help='Generate comparison across noise levels')
    parser.add_argument('--compare-methods', action='store_true',
                      help='Generate comparison across different methods')
    
    args = parser.parse_args()
    
    # Handle noise levels with precedence
    semantic_level = args.semantic_noise_lvl if args.semantic_noise_lvl is not None else args.noise_level or 0.5
    syntactic_level = args.syntactic_noise_lvl if args.syntactic_noise_lvl is not None else args.noise_level or 0.5
    image_level = args.image_noise_lvl if args.image_noise_lvl is not None else args.noise_level or 0.5
    
    os.makedirs(args.output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if args.compare_levels:
        # Generate variations with different noise levels
        noise_levels = [0.0, 0.25, 0.5, 0.75, 1.0]
        images = []
        labels = []
        
        for level in noise_levels:
            config = JamConfig(
                syntactic_noise=level,
                semantic_method=args.semantic,
                syntactic_method=args.syntactic,
                image_method=args.image_noise,
                use_image_replace=args.image_replace
            )
            generator = NoiseGenerator(config)
            img = generator.generate(args.text)
            images.append(img)
            labels.append(f"Noise Level: {level:.2f}")
        
        comparison = create_comparison_image(images, labels, "Noise Level Comparison")
        output_path = os.path.join(args.output_dir, f"noise_levels_{timestamp}.png")
        comparison.save(output_path)
        print(f"Noise level comparison saved to: {output_path}")
        
    elif args.compare_methods:
        # Generate variations with different noise types
        images = []
        labels = []
        
        config = JamConfig(
            syntactic_noise=args.noise_level,
            semantic_method=args.semantic,
            syntactic_method=args.syntactic,
            image_method=args.image_noise,
            use_image_replace=args.image_replace
        )
        
        for noise_type in NoiseType:
            config.noise_type = noise_type
            generator = NoiseGenerator(config)
            try:
                img = generator.generate(args.text)
                images.append(img)
                labels.append(f"Method: {noise_type.name}")
            except Exception as e:
                print(f"Failed to generate {noise_type.name}: {e}")
        
        comparison = create_comparison_image(images, labels, "Method Comparison")
        output_path = os.path.join(args.output_dir, f"methods_{timestamp}.png")
        comparison.save(output_path)
        print(f"Method comparison saved to: {output_path}")
        
    else:
        # Generate single image with specified settings
        config = JamConfig(
            semantic_noise_level=semantic_level,
            syntactic_noise_level=syntactic_level,
            image_noise_level=image_level,
            semantic_method=args.semantic,
            syntactic_method=args.syntactic,
            image_method=args.image_noise,
            use_image_replace=args.image_replace
        )
        generator = NoiseGenerator(config)
        img = generator.generate(args.text)
        output_path = os.path.join(args.output_dir, f"noisy_{timestamp}.png")
        img.save(output_path)
        print(f"Generated image saved to: {output_path}")

if __name__ == "__main__":
    main()
