import os
import sys
from dotenv import load_dotenv
from philosopher_chat import PhilosopherChat


def main():
    """Entry point for the philosopher-chat console script."""

    load_dotenv()
    base_url = os.getenv("BASE_URL")
    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("MODEL_NAME")

    if not all([base_url, api_key, model_name]):
        print("Missing environment variables. Create a .env file with:")
        print("BASE_URL=your_url")
        print("OPENAI_API_KEY=your_key")
        print("MODEL_NAME=your_model")
        sys.exit(1)

    # Run the app
    pc = PhilosopherChat(base_url, api_key, model_name)
    pc.run()


if __name__ == "__main__":
    main()
