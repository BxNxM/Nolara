#!/usr/bin/env python3

try:
    from .lib import Models, Config
    from . import tui
    from .NolaraCore import NolaraCore
    from .user_links import setup_nolara_user_config_links
except ImportError:
    from lib import Models, Config
    import tui
    from NolaraCore import NolaraCore
    from user_links import setup_nolara_user_config_links

import argparse
import select
import sys

def _gui_interface():
    """
    Runs the GUI interface.
    - Default interface
    """
    setup_nolara_user_config_links()
    tui.AIChatApp().run()


def _command_line_interface(prompt, text):
    """
    Runs the command line interface.
    """
    #print(f"=== PoC ===\nPrompt: {prompt}, TextIn:\n{text}")
    print("Processing...")
    command_line_model = Config.get("command_line")["model"]
    command_line_prompt = prompt if prompt else Config.get("command_line")["prompt"]

    llm = NolaraCore(stream=True)
    llm.init_model(command_line_model)
    llm.chatbot.system_prompt(prompt=command_line_prompt)  # Set system prompt for the chatbot
    response = llm.model_process(query=text)               # Process the provided text context


def interface_selector():
    """
    Selects the interface based on user input.
    """
    # Arg parser for command line interface
    arg_parser = argparse.ArgumentParser(description='Reads input from STDIN')
    arg_parser.add_argument("-p", '--prompt', help='Set custom user prompt')
    args, _ = arg_parser.parse_known_args()
    # Handle Prompt and STDIN parameters
    prompt = args.prompt if args.prompt else ''
    stdin_readable, _, _ = select.select([sys.stdin], [], [], 0)

    if sys.stdin in stdin_readable:
        text = sys.stdin.read().strip()
        return lambda: _command_line_interface(prompt, text)
    return lambda: _gui_interface()



def main():
    Models.models_requirement()
    interface = interface_selector()
    interface()


if __name__ == '__main__':
    main()

