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

def get_model_selection():
    while True:
        print("\nSelect model to load:")
        print("1. Falcon")
        print("2. Granite")
        choice = input("Enter choice (1/2): ").strip()
        if choice == "1":
            return "falcon"
        elif choice == "2":
            return "granite"
        print("Invalid choice, please try again")

def main():
    print_welcome()
    
    model_type = get_model_selection()
    
    model_manager = ModelManager()
    model_manager.initialize(model_type)
    parser = CommandParser(model_manager)
    
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
