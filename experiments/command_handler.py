import os
from datetime import datetime
from typing import Optional
from PIL import Image
from abc import ABC, abstractmethod
from .model_manager import ModelManager
import sys

print("\nInitializing experiment environment...")

# Add FigStep to Python path 
figstep_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'FigStep'))
if figstep_path not in sys.path:
    sys.path.append(figstep_path)
    print(f"Added FigStep to Python path: {figstep_path}")

try:
    from FigStep.src.generate_prompts import gen_query, QueryType, text_to_image
    print("✓ FigStep module loaded successfully")
except Exception as e: 
    print(f"✗ Error loading FigStep module: {e}")
    raise

class Command(ABC):
    @abstractmethod
    def execute(self, *args, **kwargs):
        pass

class PromptCommand(Command):
    def __init__(self, model_manager: ModelManager):
        self.model_manager = model_manager
        self.output_dir = os.path.join("experiments", "outputs")
        os.makedirs(self.output_dir, exist_ok=True)

    def execute(self, text: str, image_path: Optional[str] = None, use_figstep: bool = False):
        image = None
        if image_path:
            try:
                image = Image.open(image_path)
            except Exception as e:
                print(f"Error loading image: {e}")
                return

        print("Sending prompt to model...")
        response = self.model_manager.get_model().ask(text, image=image, is_figstep=use_figstep)
        
        # Save output
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(self.output_dir, f"response_{timestamp}.txt")
        
        with open(output_file, "w") as f:
            f.write(f"Prompt: {text}\n")
            f.write(f"Image: {image_path if image_path else 'None'}\n")
            f.write(f"FigStep: {use_figstep}\n")
            f.write("-" * 80 + "\n")
            f.write(response)
            
        print(f"\nResponse saved to: {output_file}")
        print("\nResponse:")
        print("-" * 80)
        print(response)
        print("-" * 80)

class FigStepCommand(Command):
    def __init__(self):
        self.output_dir = os.path.join("experiments", "outputs", "figstep_images")
        os.makedirs(self.output_dir, exist_ok=True)

    def execute(self, instruction: str):
        try:
            _, image = gen_query(QueryType.figstep, "", instruction)
            
            # Save generated image
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = os.path.join(self.output_dir, f"figstep_{timestamp}.png")
            image.save(image_path)
            
            print(f"\nFigStep prompt image generated and saved to: {image_path}")
            return image_path
            
        except Exception as e:
            print(f"Error generating FigStep prompt: {e}")

class CommandParser:
    def __init__(self, model_manager: ModelManager):
        self.prompt_command = PromptCommand(model_manager)
        self.figstep_command = FigStepCommand()

    def parse_and_execute(self, command_str: str):
        try:
            parts = command_str.strip().split()
            if not parts:
                return True

            command = parts[0].lower()

            if command == "exit":
                return False
                
            elif command == "prompt":
                text = " ".join(parts[1:])
                image_path = None
                use_figstep = False
                
                # Parse options
                if "-image:" in text:
                    idx = text.find("-image:")
                    image_path = text[idx+7:].split()[0].strip('"')
                    text = text[:idx].strip()
                
                if "-figstep" in text:
                    use_figstep = True
                    text = text.replace("-figstep", "").strip()
                
                self.prompt_command.execute(text, image_path, use_figstep)
                
            elif command == "figstep" and len(parts) >= 3 and parts[1] == "generate":
                instruction = " ".join(parts[2:])
                self.figstep_command.execute(instruction)
                
            else:
                print("Unknown command. Type 'exit' to quit.")
                
        except Exception as e:
            print(f"Error executing command: {e}")
            
        return True
