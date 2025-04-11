import os
import sys
from datetime import datetime
from PIL import Image

# Add FigStep to path and print for debugging
figstep_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'FigStep'))
print(f"Looking for FigStep at: {figstep_path}")
if figstep_path not in sys.path:
    sys.path.append(figstep_path)
    print("Added to sys.path")

from FigStep.src.generate_prompts import gen_query, QueryType, text_to_image

def is_valid_image(image):
    """Validate that an image was properly generated"""
    if not isinstance(image, Image.Image):
        print("Not a PIL Image")
        return False
    if image.size != (760, 760):
        print(f"Wrong size: {image.size}")
        return False
    return True

def setup_output_dir():
    """Setup output directory for test artifacts"""
    output_dir = os.path.join("experiments", "outputs", "test_figstep")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def test_prompt_generation():
    output_dir = setup_output_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    print("\nTesting FigStep prompt generation...")
    
    try:
        test_text = "Test\n1. \n2. \n3. "
        print(f"Testing basic image generation with text: {test_text}")
        test_image = text_to_image(test_text)
        
        if is_valid_image(test_image):
            test_image.save(os.path.join(output_dir, f"test_basic_{timestamp}.png"))
            print("✓ Basic image generation works")
        else:
            raise Exception("Invalid image generated")
    except Exception as e:
        print(f"✗ Basic image test failed: {str(e)}")
        return False

    test_cases = [
        ("Write code documentation", QueryType.figstep),
        ("Steps to make a sandwich", QueryType.figstep),
        ("How to write a blog post", QueryType.figstep),
        ("Basic programming tutorial", QueryType.prompt_6),
        ("What is machine learning?", QueryType.question_image_and_text),
        ("Simple baseline query", QueryType.baseline),
        ("Five step process", QueryType.prompt_5),
        # Edge cases
        ("", QueryType.figstep),  # Empty string
        ("A" * 1000, QueryType.figstep),  # Very long text
        ("Special chars !@#$%^&*()", QueryType.prompt_6),
        ("Multi\nline\ntext", QueryType.question_image_and_text),
    ]
    
    success_count = 0
    
    for instruction, query_type in test_cases:
        try:
            print(f"\nTesting: {instruction[:50]}...")
            print(f"Query type: {query_type}")
            
            if query_type == QueryType.question_image_and_text:
                prompt, image = gen_query(query_type, instruction, "")
            else:
                prompt, image = gen_query(query_type, "", instruction)
            
            if not prompt and query_type != QueryType.figstep:
                raise Exception("Expected prompt but got None")
                
            if query_type in [QueryType.figstep, QueryType.question_image_and_text]:
                if not is_valid_image(image):
                    raise Exception("Expected valid image but got None or invalid image")
            
            output_file = os.path.join(output_dir, f"test_{timestamp}.txt")
            with open(output_file, "a") as f:
                f.write(f"\nTest Case: {instruction}\n")
                f.write(f"Query Type: {query_type}\n")
                f.write(f"Generated Prompt: {prompt}\n")
                f.write("-" * 80 + "\n")
            
            if image and is_valid_image(image):
                image_path = os.path.join(output_dir, 
                    f"test_{timestamp}_{query_type.name}_{success_count}.png")
                image.save(image_path)
                print(f"✓ Image saved to: {image_path}")
            
            success_count += 1
            print("✓ Test passed")
            
        except Exception as e:
            print(f"✗ Test failed: {str(e)}")
            continue
    
    print(f"\nTests completed: {success_count}/{len(test_cases)} successful")
    return success_count == len(test_cases)

if __name__ == "__main__":
    print("Starting FigStep integration tests...")
    success = test_prompt_generation()
    print(f"\nTests {'all passed!' if success else 'had failures.'}")
