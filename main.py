import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types


def main():
    print("Hello from ai-agent-project!")

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("GEMINI_API_KEY is not set in the environment variables. Please set it in the .env file.")
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-2.5-flash", contents=messages)

    if response.usage_metadata == None:
        raise RuntimeError("Usage metadata is not available in the response. Please check the API response for details.")
    if args.verbose == True:
        print("Prompt tokens: " + str(response.usage_metadata.prompt_token_count))
        print("Response tokens: " + str(response.usage_metadata.candidates_token_count))
        print(f"User prompt: {args.user_prompt}")
    print(response.text)


if __name__ == "__main__":
    main()
