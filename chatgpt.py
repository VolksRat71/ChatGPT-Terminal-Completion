# Importing the necessary libraries
from pychatgpt import Chat
import sys
import subprocess
import dotenv
import os
import re

# Loading environment variables from a .env file in the current directory
dotenv.load_dotenv()

# Retrieving command-line arguments and formatting them for use in the chatbot
args = sys.argv[1]
args = "Write a one line bash command for this task: " + args

# Setting up the command to copy the chatbot's response to the clipboard
copy_command = "pbcopy"

# Retrieving the API key from an environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Initializing the Chat class with the API key
chat = Chat(api_key=api_key)

# Sending the prompt to the chatbot and receiving the response, along with conversation IDs
answer, previous_convo_id, convo_id = chat.ask(args)

# Using a regular expression to extract the one-line bash command from the chatbot's response
test = re.search(r"(```\n)(.*)(\n```)", answer)
if test:
	# If a match was found, printing the command and copying it to the clipboard
	answer = test.group(2)
	print("Copied to clipboard:  " + answer)
else:
	# If no match was found, indicating that the answer could not be parsed
	print(f"Could not Parse answer:   \n{'-'*50}\n{answer}\n{'-'*50}")

# Using the subprocess library to copy the command to the clipboard
subprocess.run(copy_command, text=True, input=answer)
