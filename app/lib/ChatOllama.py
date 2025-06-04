import ollama

try:
    from . import ChatBase
    from . import Config
except ImportError:
    import ChatBase
    import Config

# https://www.cohorte.co/blog/using-ollama-with-python-step-by-step-guide

class ChatOllama(ChatBase.ChatBase):

    def __init__(self, model_name:str, tools:list|None=None, stream:bool=False, debug_print=False):
        super().__init__(debug_print=debug_print)
        self.model_name = model_name
        self.stream = stream
        self.tools = tools if isinstance(tools, list) else []

    def run_model(self, stream=False):
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
            self.print(f"Model:{self.model_name}> ")
            full_response = ""
            for chunk in self.run_model(stream=True):
                content = chunk.get("message", {}).get("content", "")
                print(content, end="", flush=True)
                full_response += content
            self.print('')
            self.add_assistant_message(full_response)
            return True, {"message": {"content": full_response}}
        else:
            response = self.run_model(stream=False)
            answer = response.message.content
            self.print(f"Model:{self.model_name}>\n{answer}")
            self.add_assistant_message(answer)
            return True, response

    @staticmethod
    def human_output_parser(response):
        return response.message.content


if __name__ == "__main__":
    chatbot = ChatOllama(model_name='gemma2:latest', stream=True, debug_print=True)
    chatbot.chat_loop()
    print(chatbot)
