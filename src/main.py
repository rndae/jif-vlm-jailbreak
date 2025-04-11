from utils.singleton import Falcon

def main():
    falcon = Falcon()

    while True:
        user_input = input("Enter your question (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        
        response = falcon.ask(user_input)
        print("Answer:", response)

if __name__ == "__main__":
    main()