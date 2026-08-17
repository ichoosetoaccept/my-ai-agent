import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from call_function import available_functions, call_function
from prompts import system_prompt

# Load the openrouter API key in .env to make it available
load_dotenv()

# Here we can use the variable from .env because of the previous line
api_key = os.environ.get("OPENROUTER_API_KEY")

# If no API key is around, throw a runtime error
if not api_key:
    raise RuntimeError("no api key found")

# Argument parsing logic for when main.py is called
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

# The openai SDK client
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

messages: list[ChatCompletionMessageParam] = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

# The agentic loop
for _ in range(20):
    # call the model, handle responses, etc.
    response = client.chat.completions.create(
        model="deepseek/deepseek-v4-flash",
        messages=messages,
        tools=available_functions,
        temperature=0,
    )

    message = response.choices[0].message
    messages.append(message)

    if response.usage is None:
        raise RuntimeError("api response failed")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    if message.tool_calls:
        for tool_call in message.tool_calls:
            if tool_call.type != "function":
                continue
            result_message = call_function(tool_call, verbose=args.verbose)
            if not result_message["content"]:
                raise RuntimeError(f"no content returned from {tool_call.function.name}")
            if args.verbose:
                print(f"-> {result_message['content']}")
            messages.append(result_message)
    else:
        print("Final response:\n", message.content)
        sys.exit(0)

print("Couldn't complete task within 20 turns.")
sys.exit(1)
