

class ChatBase:

    def __init__(self, system_prompt="Be helpful assistant.", debug_print=False):
        self.model_name:str = None
        self._system_prompt:str = system_prompt
        self.messages:list = [{"role": "system", "content": self._system_prompt}]
        self.debug_print:bool = debug_print

    def __str__(self):
        return (f"ChatBase(model_name={self.model_name},"
                f"system_prompt={self._system_prompt}), message_history={len(self.messages)}")

    def print(self, message, end="\n", flush=True):
        if self.debug_print:
            print(message,  end=end, flush=flush)

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

    def run_model(self, stream=False):
        """
        The LLM wrapper function to handle the chat interaction.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def chat(self, query: str):
        """
        Chat with the model.
        """
        raise NotImplementedError("This method should be overridden by subclasses.")

    def chat_loop(self):
        """
        Start a chat loop.
        """
        if not self.debug_print:
            self.debug_print = True
            print("Force enable debug_print - only command line mode supported in chat_loop")
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
        self.print("Bye!")
