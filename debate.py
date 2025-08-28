# imports

import os
from dotenv import load_dotenv
from openai import OpenAI
import anthropic

# import for google
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

print("\n")

# Connect to OpenAI, Anthropic, and Gemini

openai = OpenAI()
claude = anthropic.Anthropic()
google.generativeai.configure()

# Set topic to discuss

topic = "pineapple on pizza"

# Set ending safe phrase

ender = "And that ends our lovely conversation."

# Specify models we want to use

gpt_model = "gpt-4.1-mini"
claude_model = "claude-3-5-haiku-latest"


# Set system prompts

gpt_system = "You are a thoughtful debater who examines evidence carefully and listens to different viewpoints. " \
"You ask probing questions, build arguments on facts rather than assumptions, and try to understand " \
"opposing perspectives before responding. You're willing to change your mind when presented with stronger evidence. " \
"You combine intellectual rigor with humility - you admit when you don't know something and focus on " \
"finding truth rather than winning arguments. " \
"You strongly OPPOSE the topic " + topic + ". " \
"When presented with a counter-argument, counter the other person's viewpoint with truthful, respectful responses that support your stance. " \
"Keep responses focused on " + topic + ". Do not ask questions that change the topic. " \
"If you finally agree with the other person and cannot offer any other argument, end your message with '" + ender + "'"

claude_system = "You are a thoughtful debater who examines evidence carefully and listens to different viewpoints. " \
"You ask probing questions, build arguments on facts rather than assumptions, and try to understand " \
"opposing perspectives before responding. You're willing to change your mind when presented with stronger evidence. " \
"You combine intellectual rigor with humility - you admit when you don't know something and focus on " \
"finding truth rather than winning arguments. " \
"You strongly SUPPORT the topic " + topic + ". " \
"When presented with a counter-argument, counter the other person's viewpoint with truthful, respectful responses that support your stance. " \
"Keep responses focused on " + topic + ". Do not ask questions that change the topic. " \
"If you finally agree with the other person and cannot offer any other argument, end your message with '" + ender + "'"


# Core functions calling the LLMs
# We set the system context, and feed the conversation thus far in messages

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

# (Fake) starting messages

gpt_messages = ["Hi there"]
claude_messages = ["Hi"]

print(f"GPT:\n{gpt_messages[0]}\n")
print(f"Claude:\n{claude_messages[0]}\n")


# Conversation loop

for i in range(10):
    gpt_next = call_gpt()
    print(f"GPT:\n{gpt_next}\n")
    gpt_messages.append(gpt_next)
    
    if gpt_next.endswith(ender):
        break;
    
    claude_next = call_claude()
    print(f"Claude:\n{claude_next}\n")
    claude_messages.append(claude_next)
    
    if claude_next.endswith(ender):
        break;

