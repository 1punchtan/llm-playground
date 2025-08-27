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

system_message = "You are an assistant that is great at telling jokes"
user_prompt = "Tell a light-hearted joke for an audience of Data Scientists"

prompts = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_prompt}
  ]

completion = openai.chat.completions.create(model='gpt-4o-mini', messages=prompts)
print(completion.choices[0].message.content)