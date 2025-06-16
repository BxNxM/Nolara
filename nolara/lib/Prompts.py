import os

SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
PROMPT_DIR = os.path.join(SCRIPT_DIR, "system_prompts")

def list_system_prompts_files():
    txt_files = [f for f in os.listdir(PROMPT_DIR) if f.endswith('.txt')]
    return txt_files


def system_prompts_dropdown():
    options = list_system_prompts_files()
    dropdown_options = [(f.split(".")[0], load_prompt(f)) for f in options]
    return dropdown_options


def load_prompt(prompt_name):
    with open(os.path.join(PROMPT_DIR, prompt_name), 'r') as file:
        content = file.read()
    return content


if __name__ == "__main__":
    prompt_files = list_system_prompts_files()
    print(prompt_files)

    prompt_content = load_prompt(prompt_files[0])
    print(prompt_content)

    print(system_prompts_dropdown())