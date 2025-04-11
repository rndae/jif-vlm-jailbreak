import os
from experiments.model_manager import ModelManager 
from experiments.command_handler import CommandParser

def print_welcome():
    print("\nFalcon-3 Experiment Console")
    print("=" * 30)
    print("Loading command reference...")
    
    commands_path = os.path.join(os.path.dirname(__file__), "commands.txt")
    try:
        with open(commands_path, "r") as f:
            print(f.read())
    except:
        print("Could not load commands reference file.")
    print("=" * 30)

def main():
    print_welcome()
    
    # Initialize model manager and command parser
    model_manager = ModelManager()
    model_manager.initialize()  # Load model once at startup
    parser = CommandParser(model_manager)
    
    # Main command loop
    running = True
    while running:
        try:
            command = input("\nEnter command > ")
            running = parser.parse_and_execute(command)
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
