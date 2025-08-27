# imports

import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic
from IPython.display import Markdown, display, update_display

# import for google
# in rare cases, this seems to give an error on some systems, or even crashes the kernel
# If this happens to you, simply ignore this cell - I give an alternative approach for using Gemini later

import google.generativeai

# Load environment variables in a file called .env
# Print the key prefixes to help with any debugging

load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
google_api_key = os.getenv('GOOGLE_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    
if anthropic_api_key:
    print(f"Anthropic API Key exists and begins {anthropic_api_key[:7]}")
else:
    print("Anthropic API Key not set")

if google_api_key:
    print(f"Google API Key exists and begins {google_api_key[:8]}")
else:
    print("Google API Key not set")


# Connect to OpenAI, Anthropic

openai = OpenAI()

claude = anthropic.Anthropic()


# This is the set up code for Gemini
# Having problems with Google Gemini setup? Then just ignore this cell; when we use Gemini, I'll give you an alternative that bypasses this library altogether

google.generativeai.configure()

topic = "pineapple on pizza"

gpt_model = "gpt-4.1-mini"
claude_model = "claude-3-5-haiku-latest"

gpt_system = "You are a chatbot who does not support the idea of " + topic + ". \
    You are to listen and understand the points the other person says, and then reply with truthful statements \
    that support your idea. Do your best to keep a productive conversation going. If you cannot present any other \
    compelling case, admit it and say that you agree with the other person."

claude_system = "You are a chatbot who supports the idea of " + topic + ". \
    You are to listen and understand the points the other person says, and then reply with truthful statements \
    that support your idea. Do your best to keep a productive conversation going. If you cannot present any other \
    compelling case, admit it and say that you agree with the other person."

def call_gpt():
    messages = [{"role": "system", "content": gpt_system}]
    for gpt, claude in zip(gpt_messages, claude_messages):
        messages.append({"role": "assistant", "content": gpt})
        messages.append({"role": "user", "content": claude})
    completion = openai.chat.completions.create(
        model=gpt_model,
        messages=messages
    )
    return completion.choices[0].message.content

def call_claude():
    messages = []
    for gpt, claude_message in zip(gpt_messages, claude_messages):
        messages.append({"role": "user", "content": gpt})
        messages.append({"role": "assistant", "content": claude_message})
    messages.append({"role": "user", "content": gpt_messages[-1]})
    message = claude.messages.create(
        model=claude_model,
        system=claude_system,
        messages=messages,
        max_tokens=500
    )
    return message.content[0].text

gpt_messages = ["Hi there"]
claude_messages = ["Hi"]

print(f"GPT:\n{gpt_messages[0]}\n")
print(f"Claude:\n{claude_messages[0]}\n")

for i in range(10):
    gpt_next = call_gpt()
    print(f"GPT:\n{gpt_next}\n")
    gpt_messages.append(gpt_next)
    
    claude_next = call_claude()
    print(f"Claude:\n{claude_next}\n")
    claude_messages.append(claude_next)

