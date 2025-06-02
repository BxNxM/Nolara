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
from openai import OpenAI

try:
    from . import ChatBase
    from . import Config
except ImportError:
    import ChatBase
    import Config

# https://www.cohorte.co/blog/using-ollama-with-python-step-by-step-guide

class ChatOllama(ChatBase.ChatBase):

    def __init__(self, model_name:str, tools:list|None=None, stream:bool=False):
        super().__init__()
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
            print(">Bot: ", end="", flush=True)
            full_response = ""
            for chunk in self.run_model(stream=True):
                content = chunk.get("message", {}).get("content", "")
                print(content, end="", flush=True)
                full_response += content
            print()
            self.add_assistant_message(full_response)
            return True, {"message": {"content": full_response}}
        else:
            response = self.run_model(stream=False)
            answer = response.message.content
            print(">Bot:", answer)
            self.add_assistant_message(answer)
            return True, response

    @staticmethod
    def human_output_parser(response):
        return response.message.content


class ChatOpenAI(ChatBase.ChatBase):
    def __init__(self, model_name: str, tools: list | None = None, stream: bool = False):
        super().__init__()
        self.model_name = model_name
        self.stream = stream
        self.tools = tools if isinstance(tools, list) else []
        openai_config = Config.get("remote_models").get("openai", None)
        if openai_config is None:
            raise ValueError("OpenAI configuration not found in config file.")
        openai_api_key = openai_config.get("api_key", None)
        if openai_api_key:
            self.client = OpenAI(api_key=openai_api_key)
        else:
            raise ValueError("OpenAI API key not found.")

    def run_model(self, stream=False):
        kwargs = {
            "model": self.model_name,
            "messages": self.messages,
            "stream": stream,
        }
        return self.client.chat.completions.create(**kwargs)

    def chat(self, query: str):
        if not query:
            return False, None

        self.add_user_message(query)

        if self.stream:
            print(">Bot: ", end="", flush=True)
            full_response = ""
            response = self.run_model(stream=True)
            for chunk in response:
                # chunk.choices[0].delta can have 'content'
                delta = chunk.choices[0].delta
                content = delta.get("content", "")
                print(content, end="", flush=True)
                full_response += content
            print()
            self.add_assistant_message(full_response)
            return True, {"message": {"content": full_response}}
        else:
            response = self.run_model(stream=False)
            answer = response.choices[0].message.content
            print(">Bot:", answer)
            self.add_assistant_message(answer)
            return True, response

    @staticmethod
    def human_output_parser(response):
        return response.choices[0].message.content


if __name__ == "__main__":
    _test_local = True
    if _test_local:
        chatbot = ChatOllama(model_name='gemma2:latest', stream=False)
        chatbot.chat_loop()
    else:
        chatbot = ChatOpenAI(model_name='gpt-4', stream=False)
        chatbot.chat_loop()