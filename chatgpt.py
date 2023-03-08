import openai
import sys
import dotenv
import os
import re
import subprocess

dotenv.load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
copy_command = "pbcopy"

def switch_case(index):
    switcher = {
        "--cmd": "Write a one line bash command for this task between two backticks: ",
        "--search": "Search the web for this and return a URL in an https format: ",
        "--comment": "Write a comment for this code: ",
        "--chat": "",
        "default": ""
    }
    return switcher.get(index, switcher["default"])

(flag, question) = sys.argv[1].split(maxsplit=1)
formatted_question = switch_case(flag) + question

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user", "content": formatted_question},
        ]
)

result = ''
reply = ''
for choice in response.choices:
    result += choice.message.content

if flag == "--cmd":
    try :
        reply = re.search(r'`(.*)`', result).group(1)
    except AttributeError:
        reply = "error"

if flag == "--search":
    try :
        reply = re.search(r'(?P<url>https?://[^\s]+)', result).group("url")
    except AttributeError:
        reply = "error"

print(result)
