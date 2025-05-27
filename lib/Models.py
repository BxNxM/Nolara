
# https://github.com/ollama/ollama-python

import ollama
from pprint import pprint


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
    details = ollama.show(model_name).modelfile
    model_details = {"modelfile": details}
    if "<tool_call>" in details:
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
    print(f"Model pull: {out}")
    return model


if __name__ == "__main__":
    print("Available models:")
    pprint(list_models())

    print("\nValidating a model...")
    print(validate_model('gemma2:latest'))

    pprint(get_models_dropdown())
    pprint(get_chat_models_dropdown())
