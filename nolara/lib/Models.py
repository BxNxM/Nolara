"""
Nolara project base model handling
"""
# https://github.com/ollama/ollama-python

import ollama
from pprint import pprint

try:
    from . import Config
except ImportError:
    import Config


#############################################################
#                     LOCAL MODEL HANDLING                  #
#############################################################

def list_models():
    """
    List local ollama models
    """
    return ollama.list()['models']


def show_model(model_name):
    """
    Show model details, check tool feature
    :return:
        {"modelfile": details, "tool": True/False}
    """
    model_details = {"modelfile": f"Remote model {model_name} (beta)", "tool": False}
    if model_name.startswith(":"):
        # Remote model indicator prefix (workaround for OpenAI API)
        return model_details

    if validate_model(model_name):
        details = ollama.show(model_name).modelfile
        model_details = {"modelfile": details}
        if "<tool_call>" in details or "tool call" in details:
            model_details["tool"] = True
        else:
            model_details["tool"] = False
    return model_details


def get_models_dropdown() -> list:
    """
    Filter models for dropdown
    :return:
        [("Visible name", "model name"), ...]
    """
    models = list_models()
    dropdown_options = [(f"{m.model.split(":")[0]} {m.details.parameter_size}", m.model) for m in models]
    # Return list of tuples [("Visible name", "model name"), ...]
    return dropdown_options


def get_chat_models_dropdown() -> list:
    """
    Filter chat models for dropdown
    :return:
        [("Visible name", "model name"), ...]
    """
    models = get_models_dropdown()
    chat_models = [m for m in models if "code" not in m[1] and "embed" not in m[1]]
    return chat_models


def validate_model(model) -> str:
    """
    Validate model availability
    """
    models = [m.model for m in list_models()]
    if model not in models:
        raise ValueError(f"Model {model} not available. Available models are: {models}")
    return model


def pull_model(model):
    out = ollama.pull(model)
    print(f"Model pulled successfully.: {out}")
    return model


def models_requirement() -> None:
    """
    Check local models requirements and pull if not available
    """
    requirements = Config.get('models') or []
    requirements_cnt = len(requirements)
    models = [m.model for m in list_models()]
    for i, requirement in enumerate(requirements):
        if requirement not in models:
            print(f"[{i+1}/{requirements_cnt}] Pull: {requirement} (Please wait...)")
            pull_model(requirement)
        else:
            print(f"[{i+1}/{requirements_cnt}] Model {requirement} already available.")

#############################################################
#                   REMOTE MODEL HANDLING (beta)            #
#############################################################

def list_remote_models() -> dict:
    """
    List all remote models available
    :return:
        {"openai": ["model1", "model2"], ...}
    """
    remote_models_config = Config.get("remote_models")
    remote_models = {}
    if remote_models_config:
        # Check openai configuration for remote models
        openai_conf = remote_models_config.get("openai")
        if openai_conf:
            remote_models["openai"] = []
            if openai_conf["api_key"] is not None:
                remote_models["openai"] = openai_conf["models"]
        # Check etc. if needed later on
    return remote_models

def get_remote_models_dropdown() -> list:
    """
    Filter remote models for dropdown
    :return:
        [("Visible name", ":vendor:model_name"), ...]
    """
    remote_models = list_remote_models()
    dropdown_options = []
    for ai, models in remote_models.items():
        for m in models:
            name = f"{m} ☁️"
            model = f":{ai}:{m}"
            dropdown_options.append((name, model))
    # Return list of tuples [("Visible name", "model name"), ...]
    return dropdown_options



#############################################################
#                         TEST FUNCTIONS                    #
#############################################################


if __name__ == "__main__":
    print("Available models:")
    pprint(list_models())

    print("\nValidating a model...")
    print(validate_model('gemma2:latest'))

    pprint(get_models_dropdown())
    pprint(get_chat_models_dropdown())

    #models_requirement()
    #print(show_model("llama3.2:1b"))

    pprint(list_remote_models())
    pprint(get_remote_models_dropdown())
