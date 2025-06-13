import ollama
import asyncio

try:
    from . import ChatBase
    from . import Config
except ImportError:
    import ChatBase
    import Config

# https://www.cohorte.co/blog/using-ollama-with-python-step-by-step-guide

class ChatOllama(ChatBase.ChatBase):

    def __init__(self, model_name:str, tools:list|None=None, stream:bool=False, debug_print=False, tui_console=None):
        super().__init__(debug_print=debug_print, tui_console=tui_console)
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

    async def async_run_model(self, stream=False):
        """
        Async version of the LLM wrapper to handle chat interaction.
        """
        if self.tools:
            client = ollama.AsyncClient()
            response  = await client.chat(model=self.model_name, messages=self.messages, tools=self.tools, stream=stream)
            return response
        else:
            client = ollama.AsyncClient()
            response = await client.chat(model=self.model_name, messages=self.messages,stream=stream)
            return response

    def chat(self, query) -> (bool, ollama._types.ChatResponse|dict|None):
        response = None
        if not query:
            return False, response

        self.add_user_message(query)
        if self.stream:
            self.write_tui(f"Model:{self.model_name}> ")
            full_response = ""
            for chunk in self.run_model(stream=True):
                content = chunk.get("message", {}).get("content", "")
                print(content, end="", flush=True)
                full_response += content
            self.write_tui('')
            self.add_assistant_message(full_response)
            return True, {"message": {"content": full_response}}
        else:
            response = self.run_model(stream=False)
            answer = response.message.content
            self.write_tui(f"Model:{self.model_name}>\n{answer}")
            self.add_assistant_message(answer)
            return True, response

    async def async_chat(self, query) -> (bool, dict | None):
        """
        Async version of chat that offloads blocking calls to a thread.
        Suitable for integration in asyncio-based apps.
        """
        if not query:
            return False, None

        self.add_user_message(query)

        if self.stream:
            self.write_tui(f"Model:{self.model_name}> ")
            full_response_parts = []

            async def run_streaming():
                self.write_tui(f"Model:{self.model_name}>")
                async for chunk in await self.async_run_model(stream=True):
                    content = chunk.get("message", {}).get("content", "")
                    #print(content, end="", flush=True)
                    self.write_tui(content, end="", flush=True)
                    full_response_parts.append(content)
                self.write_tui('')

            full_response_parts = []
            await run_streaming()

            full_response = ''.join(full_response_parts)
            self.add_assistant_message(full_response)
            return True, {"message": {"content": full_response}}

        else:
            response = await self.async_run_model(stream=False)
            answer = response.message.content
            self.write_tui(f"Model:{self.model_name}>\n{answer}")
            self.add_assistant_message(answer)
            return True, response

    @staticmethod
    def human_output_parser(response):
        if isinstance(response, dict):
            return response.get("message", {}).get("content", "")
        return response.message.content


if __name__ == "__main__":
    chatbot = ChatOllama(model_name='gemma2:latest', stream=True, debug_print=True)
    chatbot.chat_loop(asynchronous=True)
    print(chatbot)
