import os
import json
from dotenv import load_dotenv
from google import genai
import argparse
from openai import OpenAI
from call_function import available_functions

def main():
    print("Hello from ai-agent-project!")

    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if api_key == None:
        raise RuntimeError("OPENROUTER_API_KEY is not set in the environment variables. Please set it in the .env file.")
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    system_prompt = """
    You are a helpful AI coding agent.
    When a user asks a question or makes a request, make a function call plan. 
    You can perform the following operations via these functions:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. 
    You do not need to specify the working directory in your function calls. 
    It is automatically injected for security reasons.
    """

    messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
    ]

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key,)
    response = client.chat.completions.create(
        model="openrouter/free", 
        messages=messages, 
        tools=available_functions
        )

    if response.usage == None:
        raise RuntimeError("Usage metadata is not available in the response. Please check the API response for details.")
    if args.verbose == True:
        print("Prompt tokens: " + str(response.usage.prompt_token_count))
        print("Response tokens: " + str(response.usage.candidates_token_count))
        print(f"User prompt: {args.user_prompt}")

    text = response.choices[0].message

    if text.tool_calls != None: 
        for tool_call in text.tool_calls:
            print(f"Calling function: {tool_call.function.name} with arguments: {json.loads(tool_call.function.arguments)}")
    print(text.content)


if __name__ == "__main__":
    main()
