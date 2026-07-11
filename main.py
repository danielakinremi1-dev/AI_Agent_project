import os
import sys 
from dotenv import load_dotenv 
import argparse
from openai import OpenAI
from call_function import available_functions, call_function

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
    When a user asks a question or makes a request, make a function call plan and execute the request. 
    You can perform the following operations via these functions given to you:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. 
    Answer questions in a concise manner.
    Ensure if you use keyword arguments that they are relevant to the function you are calling.
    You do not need to specify the working directory in your function calls. 
    It is automatically injected for security reasons.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
        ]
    
    for _ in range(20):
        
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key,)
        response = client.chat.completions.create(
            model="openrouter/free", 
            messages=messages, 
            tools=available_functions
            )

        if response.usage == None:
            raise RuntimeError("Usage metadata is not available in the response. Please check the API response for details.")
        if args.verbose == True:
            print(f"Prompt tokens: {response.usage.prompt_tokens}")
            print(f"Response tokens: {response.usage.completion_tokens}")
            print(f"User prompt: {args.user_prompt}")

        #Log the response content and tool calls
        text = response.choices[0].message
        messages.append(text) 

        
        if text.tool_calls != None: 
            for tool_call in text.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                if result_message["content"] == None:
                    raise Exception("Function call did not return a result. Please check the function implementation.")
                elif args.verbose:
                    print(f"-> {result_message['content']}")
                    messages.append(result_message)
                else:
                    messages.append(result_message)
        else:
            print("Final response:")
            print(text.content)
            return
        
    
    sys.exit(1, "Error: Maximum number of iterations reached. The conversation did not converge to a final response.")

if __name__ == "__main__":
    main()
