# OpenAI Chatbot

This is a command-line application that uses the OpenAI API to generate responses to user input. The application currently supports four types of commands:

- `--cmd`: Ask the chatbot to generate a one-line Bash command for a given task.
- `--search`: Ask the chatbot to search the web for information and return a URL in an HTTPS format.
- `--comment`: Ask the chatbot to generate a comment for a given block of code.
- `--chat`: Ask the chatbot to engage in a free-form conversation.

## Installation

To use this application, you will need to have an OpenAI API key. You can sign up for an API key [here](https://beta.openai.com/signup/).

Once you have an API key, you can download the source code for this application from GitHub:

```bash
git clone https://github.com/your_username/openai-chatbot.git
cd openai-chatbot
```

Next, create a virtual environment and install the required dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To run the chatbot application, you can use the chatbot.py script with appropriate command-line arguments.

Alternatively, you can add the following function to your .bashrc or .zshrc file to make running the chatbot more convenient:

```sh
function gpt {
  args=$@
  python3.9 "Directory of the script" "$args"
}
```

Replace "Directory of the script" with the full path to the chatbot.py script on your machine.

With this function in place, you can run the chatbot by typing gpt followed by the appropriate command-line arguments:

```sh
gpt --cmd "What's a good command to rename a file in Linux?"
```

The chatbot will generate a response based on the input question and command type, and print it to the console.

In addition to the response, the chatbot will save the chat history to a list of dictionaries in the chat_history variable, which can be accessed from within the script.

## License
This project is licensed under the terms of the MIT license. See the LICENSE file for more details.
