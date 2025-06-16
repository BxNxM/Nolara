from openai import OpenAI

try:
    from . import ChatBase
    from . import Config
except ImportError:
    import ChatBase
    import Config


class ChatOpenAI(ChatBase.ChatBase):
    def __init__(self, model_name:str, tools: list|None=None, stream:bool=False, debug_print:bool=False, tui_console=None):
        super().__init__(debug_print=debug_print, tui_console=tui_console)
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
            self.write_tui(f"Model:{self.model_name}> ")
            full_response = ""
            response = self.run_model(stream=True)
            for chunk in response:
                # chunk.choices[0].delta can have 'content'
                delta = chunk.choices[0].delta
                content = delta.get("content", "")
                self.write_tui(content, end="", flush=True)
                full_response += content
            self.write_tui('')
            self.add_assistant_message(full_response)
            return True, {"message": {"content": full_response}}
        else:
            response = self.run_model(stream=False)
            answer = response.choices[0].message.content
            self.write_tui(f"Model:{self.model_name}>\n{answer}")
            self.add_assistant_message(answer)
            return True, response

    @staticmethod
    def human_output_parser(response):
        return response.choices[0].message.content


if __name__ == "__main__":
    # TODO: OpenAI stream mode
    chatbot = ChatOpenAI(model_name='gpt-4', stream=False, debug_print=True)
    chatbot.chat_loop()
    print(chatbot)
