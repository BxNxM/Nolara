
# https://github.com/ollama/ollama-python

import ollama
from pprint import pprint


def list_models():
    return ollama.list()['models']


def validate_model(model):
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
