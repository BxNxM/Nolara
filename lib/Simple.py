import ollama

# https://github.com/ollama/ollama-python
# https://ollama.com/blog/tool-support
# https://ollama.com/blog/functions-as-tools
# https://www.cohorte.co/blog/using-ollama-with-python-step-by-step-guide

# Use the generate function for a one-off prompt
result = ollama.generate(model='gemma2:latest', prompt='Why is the sky blue?')
print(result['response'])