from utils.singleton import FalconSingleton

def main():
    # Initialize the singleton instance of the Falcon 3 model
    falcon_model = FalconSingleton()

    while True:
        user_input = input("Enter your prompt (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        
        # Generate a response using the Falcon model
        response = falcon_model.generate_response(user_input)
        print("Response:", response)

if __name__ == "__main__":
    main()