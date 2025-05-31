"""
Nolara project base chat implementation
- message history handling
    - add_assistant_message (embedded in chat)
    - add_user_message (embedded in chat)
    - clear_messages (embedded in chat)
    - system_prompt set/get
- model selection
- stream output (optional)
- tools integration (optional)
"""

import ollama

# https://www.cohorte.co/blog/using-ollama-with-python-step-by-step-guide

class ChatOllama:

    def __init__(self, model_name:str, tools:list|None=None, stream:bool=False):
        self.model_name = model_name
        self.stream = stream
        self.tools = tools if isinstance(tools, list) else []
        self.system_prompt = "Be helpful, informative, and comprehensive assistant."
        self.messages = [{"role": "system", "content": self.system_prompt}]

    def add_assistant_message(self, message):
        """
        Add an assistant message to the chat history.
        """
        assistant = {"role": "assistant", "content": message}
        self.messages.append(assistant)

    def add_user_message(self, message):
        """
        Add a user message to the chat history.
        """
        user = {"role": "user", "content": message}
        self.messages.append(user)

    def clear_messages(self):
        """
        Clear all messages in the chat history.
        """
        self.messages = [{"role": "system", "content": self.system_prompt}]

    def system_prompt(self, prompt=None) -> str:
        """
        Getter and setter for the system prompt.
        """
        if prompt is None:
            return self.system_prompt
        else:
            self.system_prompt = prompt
            self.messages[0] = {"role": "system", "content": self.system_prompt}
        return self.system_prompt

    def ollama_chat(self, stream=False):
        """
        The LLM wrapper function to handle the chat interaction.
        """
        if len(self.tools) > 0:
            # With tools
            return ollama.chat(model=self.model_name,
                               messages=self.messages,
                               tools=self.tools,
                               stream=stream)
        else:
            # Without tools
            return ollama.chat(model=self.model_name,
                               messages=self.messages,
                               stream=stream)

    def chat(self, query):
        response = None
        if not query:
            return False, response

        self.add_user_message(query)
        if self.stream:
            print(">Bot: ", end="", flush=True)
            full_response = ""
            for chunk in self.ollama_chat(stream=True):
                content = chunk.get("message", {}).get("content", "")
                print(content, end="", flush=True)
                full_response += content
            print()
            self.add_assistant_message(full_response)
            return True, {"message": {"content": full_response}}
        else:
            response = self.ollama_chat(stream=False)
            answer = response.message.content
            print(">Bot:", answer)
            self.add_assistant_message(answer)
            return True, response

    @staticmethod
    def human_output_parser(response):
        return response.message.content

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