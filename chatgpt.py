import openai
import sys
import dotenv
import os
import re
import subprocess
import sys
import re

# Load environment variables from .env file
dotenv.load_dotenv()

# Set OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize an empty list to hold chat history
chat_history = []

# Define the command to copy text to clipboard
copy_command = ""
if sys.platform.startswith('darwin'):
    copy_command = 'pbcopy'  # macOS
elif sys.platform.startswith('win'):
    copy_command = 'clip'  # Windows
elif sys.platform.startswith('linux'):
    copy_command = 'xclip -selection clipboard'  # Linux
else:
    print("Unsupported OS")


def switch_case(index, input_value="", scope="question"):
    """
    This function takes three parameters:
    `index` (string): a key to look up in the `switcher` dictionary,
    `input_value` (string): optional parameter that holds the input value for formatting,
    `scope` (string): specifies the type of formatting to be applied.

    The `switcher` dictionary maps keys to dictionaries with two keys: "question" and "format".
    "question" holds a string value, which is a prompt or question for the user.
    "format" holds a lambda function that formats the input_value based on the given `scope`.

    ***NOTE:
    When using the "format" scope, the lambda function must be invoked with the `()` operator.
    And the "question" scope does not require the `()` operator.
    ***

    The function returns a formatted string based on the `index` and `scope` parameters,
    or returns a default value if no key is found in `switcher`.
    """

    switcher = {
        "--cmd": {
            "question": "Write a one line bash command for this task between 2 backticks: ",
            "format": lambda: re.search(r'`(.*)`', input_value).group(1)
        },
        "--search": {
            "question": "Search the web for this and return a URL in an https format and only the URL: ",
            "format": lambda: re.search(r'(?P<url>https?://[^\s]+)', input_value).group("url")
        },
        "--comment": {
            "question": "Write a comment for this code: ",
            "format": lambda: input_value
        },
        "--chat": {
            "question": "",
            "format": lambda: input_value
        },
        "default": {
            "question": "",
            "format": lambda: input_value
        },
    }

    return_value = switcher.get(index, switcher["default"])[scope]
    return return_value


# Parse the command line arguments to determine the type of command and the input question
(flag, question) = sys.argv[1].split(maxsplit=1)

# Format the input question based on the command type
formatted_question = switch_case(flag) + question

# Call the OpenAI API to generate a response to the input question
response = openai.Completion.create(
    engine="text-davinci-002",  # Use the Davinci model to generate text
    # Include the formatted question in the prompt for the chatbot
    prompt=(f"You: {formatted_question}\nBot:"),
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

# Call switch_case() with specified flag, result, and scope "format",
# and assign the result to the variable "reply"
reply = switch_case(flag, result, "format")()

if flag == "--cmd":
    # Print a message indicating that the command has been copied to clipboard
    print("Command copied to clipboard: " + reply)
    # Run a subprocess to copy the command to clipboard
    subprocess.run(copy_command, text=True, input=reply)
else:
    # If the flag is not set to "--cmd", print the reply
    print(reply)


