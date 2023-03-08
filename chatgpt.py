import openai
import sys
import dotenv
import os
import re
import subprocess

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
copy_command = "pbcopy"

def switch_case(flag):
    switcher = {
        "--chat": "",
        "default": "Write a one line bash command for this task: "
    }
    return switcher.get(flag, switcher["default"])

question = sys.argv[1]
formatted_question = switch_case("") + question

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user", "content": formatted_question},
        ]
)

result = ''
for choice in response.choices:
    result += choice.message.content

# Using a regular expression to extract the one-line bash command from the chatbot's response
test = re.search(r"(```\n)(.*)(\n```)", result)
if test:
	# If a match was found, printing the command and copying it to the clipboard
	result = test.group(2)
	print("Copied to clipboard:  " + result)
else:
	# If no match was found, indicating that the answer could not be parsed
	print(f"Could not Parse answer:   \n{'-'*50}\n{result}\n{'-'*50}")

# Using the subprocess library to copy the command to the clipboard
subprocess.run(copy_command, text=True, input=result)

print(result)
