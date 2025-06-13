# IMPORT LLM LIBRARIES
try:
    from .lib import Models
    from .lib.ChatOllama import ChatOllama
    from .lib.ChatOpenAI import ChatOpenAI
    from .lib import Agents
    from .lib import Config
except ImportError:
    from lib import Models
    from lib.ChatOllama import ChatOllama
    from lib.ChatOpenAI import ChatOpenAI
    from lib import Agents
    from lib import Config

# IMPORT AUDIO LIBRARY IF AVAILABLE
try:
    from .lib import Audio
except ImportError:
    try:
        from lib import Audio
    except ImportError:
        Audio = None


class NolaraCore:

    def __init__(self):
        self.version:str = "0.0.1"
        self.chatbot:ChatOllama|ChatOpenAI|None = None          # Chatbot instance
        self._tool_calls:bool = False                           # Selected Chatbot tool call capability
        self.last_response:str = ""                             # Cache last response

    def init_model(self, model_name, tui_console=None):
        """
        This method initializes a new model instance.
        - Chat mode
        - Agentic mode (if available and enabled)
        """
        if self.chatbot:
            local_model_match = model_name == self.chatbot.model_name
            remote_model_match = model_name.startswith(":") and model_name.endswith(self.chatbot.model_name)
            if local_model_match or remote_model_match:     # Handle Agent switch
                return self.chatbot

        self._tool_calls = self.is_agent_enabled(model_name)
        if model_name.startswith(":"):
            # remote model (workaround for OpenAI API)
            _remote = model_name.split(":")
            remote_vendor = _remote[1]
            remote_model_name = _remote[2]
            if remote_vendor == "openai":
                self.chatbot = ChatOpenAI(remote_model_name, tui_console=tui_console)
                return self.chatbot
        else:
            # local model
            if self._tool_calls:
                # Craft agent chat model
                self.chatbot = Agents.Agent(model_name, max_tool_steps=10, tui_console=tui_console)
                return self.chatbot
            # Create chat model
            self.chatbot = ChatOllama(model_name, stream=False, tui_console=tui_console)
        return self.chatbot

    def is_agent_enabled(self, model_name=None) -> bool:
        """
        This method checks whether agents are enabled in the configuration
        and if tool calls are available.
        """
        if model_name is None:
            return self._tool_calls
        _tool_calls = Models.show_model(model_name)["tool"]
        return Config.get("agents")["enabled"] and _tool_calls

    def model_process(self, query, wrap=True, box_width=80):
        """
        This method processes the query using the current chatbot model.
        """
        if self.chatbot:
            state, response = self.chatbot.chat(query)
            response = self.chatbot.human_output_parser(response)
        else:
            response = "No chatbot initialized"
        self.last_response = response
        return response

    def speach_to_text(self):
        if Audio is None:
            return
        if len(self.last_response) > 0:
            Audio.text_to_speech(self.last_response)

    @staticmethod
    def teardown():
        if Audio is not None:
            Audio.delete_audio_cache()