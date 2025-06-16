import asyncio


class ChatBase:

    def __init__(self, system_prompt="Be helpful assistant.", debug_print=False, tui_console=None):
        self.model_name:str|None = None
        self._system_prompt:str = system_prompt
        self.messages:list = [{"role": "system", "content": self._system_prompt}]
        self.debug_print:bool = debug_print
        self.tui_console:callable|None = tui_console

    def __str__(self):
        return (f"ChatBase(model_name={self.model_name},"
                f"system_prompt={self._system_prompt}), message_history={len(self.messages)}")

    #####################################################
    #           Output handlers - STDOUT / TUI          #
    #####################################################
    def print(self, message, end="\n", flush=True):
        """
        Terminal debug print function
        """
        if self.debug_print:
            print(message,  end=end, flush=flush)

    def write_tui(self, message, end="\n", flush=True):
        """
        Write to TUI console (with terminal print fallback)
        """
        if self.tui_console is None:
            print(message, end=end, flush=flush)
            return
        self.tui_console(message)

    #####################################################
    #              Chat History Management              #
    #####################################################
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
        self.messages = [{"role": "system", "content": self._system_prompt}]

    def system_prompt(self, prompt=None) -> str:
        """
        Getter and setter for the system prompt.
        """
        if prompt is None or prompt.strip() == self._system_prompt:
            return self._system_prompt
        else:
            self._system_prompt = prompt.strip()
            self.messages[0] = {"role": "system", "content": self._system_prompt}
        return self._system_prompt

    #####################################################
    #                   LLM Model usage                 #
    #####################################################
    def run_model(self, stream=False):
        """
        The LLM wrapper function to handle the chat interaction.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    async def async_run_model(self, stream=False):
        """
        Async version of the LLM wrapper to handle chat interaction.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def chat(self, query: str):
        """
        Chat with the model.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    async def async_chat(self, query) -> (bool, dict | None):
        """
        AsyncChat with the model.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    #####################################################
    #               Debug Chat loop for STDOUT          #
    #####################################################
    def chat_loop(self, asynchronous=False):
        """
        Start a chat loop.
        """
        def _user_input():
            try:
                _input = input(f"[{self.model_name}] Ask me something: ")
                if _input.lower() in ['exit', 'quit', 'bye']:
                    _input = None
            except KeyboardInterrupt:
                _input = None
            return _input

        if not self.debug_print:
            self.debug_print = True
            self.print("Force enable debug_print - only command line mode supported in chat_loop")

        if asynchronous:
            # For interactive async test:
            async def _main():
                while True:
                    user_input = _user_input()
                    if user_input is None:  # User pressed Ctrl+C or similar
                        break
                    success, response = await self.async_chat(query=user_input)
                    if not success:
                        break
            asyncio.run(_main())
        else:
            while True:
                user_input = _user_input()
                if user_input is None:  # User pressed Ctrl+C or similar
                    break
                success, response = self.chat(query=user_input)
                if not success:
                    break
        self.print("Bye!")
