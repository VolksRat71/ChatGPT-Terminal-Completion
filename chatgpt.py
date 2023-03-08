import openai
import sys
import dotenv
import os
import re
import subprocess

# Load environment variables from .env file
dotenv.load_dotenv()

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define the command to copy text to clipboard
copy_command = "pbcopy"

# Initialize an empty list to hold chat history
chat_history = []

# Define a function to handle different types of commands
def switch_case(index):
    switcher = {
        "--cmd": "Write a one line bash command for this task between two backticks: ",
        "--search": "Search the web for this and return a URL in an https format: ",
        "--comment": "Write a comment for this code: ",
        "--chat": "",
        "default": ""
    }
    return switcher.get(index, switcher["default"])

# Parse the command line arguments to determine the type of command and the input question
(flag, question) = sys.argv[1].split(maxsplit=1)

# Format the input question based on the command type
formatted_question = switch_case(flag) + question

# Call the OpenAI API to generate a response to the input question
response = openai.Completion.create(
    engine="text-davinci-002",  # Use the Davinci model to generate text
    prompt=(f"You: {formatted_question}\nBot:"),  # Include the formatted question in the prompt for the chatbot
    temperature=0.7,  # Adjust the "creativity" of the chatbot's responses
    max_tokens=1024,  # Limit the maximum length of the response
)

# Initialize a string to hold the chatbot's response and a variable to hold the output (if any) of the command
result = ''
reply = ''

# Loop over each potential response from the chatbot and append it to the result string and chat history
for choice in response.choices:
    result += choice.text
    chat_history.append({"role": "bot", "content": choice.text})

# If the command type is "--cmd", extract the command from the chatbot's response
if flag == "--cmd":
    try :
        reply = re.search(r'`(.*)`', result).group(1)
    except AttributeError:
        reply = "error"

# If the command type is "--search", extract the URL from the chatbot's response
if flag == "--search":
    try :
        reply = re.search(r'(?P<url>https?://[^\s]+)', result).group("url")
    except AttributeError:
        reply = "error"

# Print the chatbot's response to the console
print(result)
