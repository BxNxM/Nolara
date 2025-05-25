import ollama

# https://www.cohorte.co/blog/using-ollama-with-python-step-by-step-guide

class ChatOllama:

    def __init__(self, model_name:str, tools:list|None=None, stream:bool=False):
        self.model_name = model_name
        self.stream = stream
        self.tools = tools if isinstance(tools, list) else []
        self.messages = [{"role": "system", "content": "You are a helpful assistant."}]

    def add_assistant_message(self, message):
        assistant = {"role": "assistant", "content": message}
        self.messages.append(assistant)

    def add_user_message(self, message):
        user = {"role": "user", "content": message}
        self.messages.append(user)

    def chat(self, query):
        response = None
        if not query:
            return False, response

        if self.stream:
            print(">Bot: ", end="", flush=True)
            full_response = ""
            for chunk in ollama.chat(model=self.model_name, messages=self.messages, tools=self.tools, stream=True):
                content = chunk.get("message", {}).get("content", "")
                print(content, end="", flush=True)
                full_response += content
            print()
            self.add_assistant_message(full_response)
            return True, {"message": {"content": full_response}}
        else:
            self.add_user_message(query)
            response = ollama.chat(model=self.model_name, messages=self.messages, tools=self.tools)
            answer = response.message.content
            print(">Bot:", answer)
            self.add_assistant_message(answer)
            return True, response

    def chat_loop(self):
        # Continue the conversation:
        while True:
            try:
                user_input = input(f"[{self.model_name}] Ask me something: ")
            except KeyboardInterrupt:
                break
            if user_input.lower() in ['exit', 'quit', 'bye']:
                break
            state, response = self.chat(query=user_input)
            if not state:
                break
        print("Bye!")

if __name__ == "__main__":
    chatbot = ChatOllama(model_name='gemma2:latest', stream=False)
    chatbot.chat_loop()