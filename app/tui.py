#!/usr/bin/env python3

# Textual is a Python library for building rich, interactive terminal applications.
# https://textual.textualize.io/widget_gallery/
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Input, Button, Log, Select, Static, ProgressBar, Footer

# Additional libraries
import asyncio
import time
import os
import re
import textwrap

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TCSS_PATH = os.path.join(SCRIPT_DIR, "textual.tcss")

# IMPORT LLM LIBRARIES
try:
    from .lib import Models
    from .lib import Prompts
    from . import NolaraCore
except ImportError:
    from lib import Models
    from lib import Prompts
    import NolaraCore

# Load CSS file
def load_css():
    with open(TCSS_PATH, "r") as f:
        textual_css = f.read()
    return textual_css


class AIChatApp(App, NolaraCore.NolaraCore):
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("escape", "quit", "Quit"),
    ]
    CSS = load_css()

    def __init__(self):
        NolaraCore.NolaraCore.__init__(self)
        # Initialize global variables for the app
        self.model_dropdown_content = Models.get_chat_models_dropdown() + Models.get_remote_models_dropdown()
        # Initialize global textual.widgets widgets
        self.progress_bar = ProgressBar(total=100, id="progress-bar")
        self.timer_display = Static("⏱️  Time taken: 0s", id="timer-display")
        # Initialize global parameters for textual.widgets
        self._chatbox:Log|None = None
        self.input:Input|None = None
        self.model_dropdown:Select|None = None
        self.system_prompt_input:Input|None = None
        self.prompt_dropdown:Select|None = None
        self.init_model(self._get_default_model(), tui_console=self.write_to_chatbox)      # Preload model
        App.__init__(self)

    @staticmethod
    def _get_default_model():
        return Models.get_chat_models_dropdown()[0][1]

    def compose(self) -> ComposeResult:
        # Title bar with styled markup
        yield Static("[b green]Nolara[/]", id="title-bar", markup=True)

        with Horizontal(id="main-layout"):
            ############################# SIDEBAR with dropdowns #############################
            with Vertical(id="sidebar"):
                self.model_dropdown = Select(
                    options=self.model_dropdown_content,
                    value=self._get_default_model(),
                    prompt="Select a model...",
                    id="model-dropdown",
                )
                yield self.model_dropdown
                # Label for model features section (Chat/Agentic)
                yield Static("Model Features", id="model-feature-label", markup=True)
                # Bottom section with dropdown + input stacked
                with Vertical(id="bottom-controls"):
                    # Prompt input dropdown for system prompts
                    self.prompt_dropdown = Select(
                        options=Prompts.system_prompts_dropdown(),
                        prompt="Select system prompt...",
                        id="prompt-dropdown")
                    yield self.prompt_dropdown
                    # New editable input field for system prompts
                    self.system_prompt_input = Input(
                        placeholder=self.chatbot.system_prompt(),
                        id="system-prompt-input")
                    yield self.system_prompt_input

            ######################### CHAT area with chatbox and buttons #########################
            with Vertical(id="chat-area"):
                self._chatbox = Log(id="chat")
                yield self._chatbox

                with Horizontal(id="progress-line"):
                    yield self.progress_bar
                    yield self.timer_display

                with Horizontal(id="input_bar"):
                    self.input = Input(placeholder="Type a message...", id="input")
                    yield self.input
                    yield Button("Send", id="send-button")
                    if NolaraCore.Audio is not None:
                        yield Button("Speak", id="speak-button")
                    # TODO Microphone button (Listen)

        # Footer showing keybindings (q or Esc to quit)
        yield Footer(id="app-footer")

    #######################################################################
    ##                              Events                               ##
    #######################################################################
    def on_select_changed(self, event: Select.Changed) -> None:
        """
        Handle the selection change event for the model dropdown.
        """
        if event.select.id == "model-dropdown":
            # MODEL SELECTION
            model_name = event.value
            self._chatbox.clear()
            self.progress_bar.progress = 0
            label_widget = self.query_one("#model-feature-label", Static)
            if self.is_agent_enabled(model_name):
                label_widget.update("[b blue]Agentic[/]")
            else:
                label_widget.update("[b green]Chat[/]")
        if event.select.id == "prompt-dropdown":
            # PROMPT SELECTION
            selected_prompt = event.value
            self.system_prompt_input.value = selected_prompt
            self.chatbot.system_prompt(selected_prompt)

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """
        Handle the button press event for sending a message, etc.
        """
        if event.button.id == "send-button":
            await self.process_message()
        if event.button.id == "speak-button":
            self.write_to_chatbox("Speak...")
            self.speach_to_text()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """
        Handle the input submission event for sending a message.
        """
        if event.input.id == "input":
            await self.process_message()
        if event.input.id == "system-prompt-input":
            self.chatbot.system_prompt(event.value)

    def action_quit(self) -> None:
        self.teardown()
        self.exit()

    #######################################################################
    ##                        AI Chat features                           ##
    #######################################################################
    async def process_message(self) -> None:
        message = self.input.value.strip()
        if not message:
            return

        selected_option = self.model_dropdown.value
        self.init_model(selected_option, tui_console=self.write_to_chatbox)

        self.write_to_chatbox("_" * (self._chatbox.size.width-4))
        await self.update_progress(10)
        self.write_to_chatbox(f"\nYou: {message}")
        start_time = time.time()
        box_width = self._chatbox.size.width - 4
        response = self.model_process(message, wrap=True, box_width=box_width)
        await self.update_progress(80)
        duration = time.time() - start_time
        self.timer_display.update(f"⏱️  Time taken: {duration:.2f}s")

        #self.write_to_chatbox(f"Assistant {self.chatbot.model_name}:")
        #self.write_to_chatbox(response)

        # Animate progress bar - dummy
        await self.update_progress(100)
        await asyncio.sleep(0.1)
        #self.progress_bar.progress = 0

        self.input.value = ""

    def write_to_chatbox(self, content):
        """
        Write content to the chatbox (Log widget), supporting single string, word, or list of strings.

        Args:
            content (str | list[str]): The message or list of messages to log.
            wrap (bool): Whether to enable wrapping (uses chatbox width).
            prefix (str): Optional string to prepend before each line.
        """
        if self._chatbox is None:
            return

        content = self._wrap_response(content, self._chatbox.size.width-4)

        if isinstance(content, str):
            self._chatbox.write_line(content)
        elif isinstance(content, list):
            self._chatbox.write_lines(content)
        else:
            raise TypeError("Content must be a string or list of strings.")

    @staticmethod
    def _wrap_response(response, box_width):
        response_lines = re.split(r'\n| \* ', response)
        wrapped_response = []
        for line in response_lines:
            if len(line) > box_width:
                # Wrap the response text to fit inside the Log widget width
                wrapped_response += textwrap.wrap(line, width=box_width)
            else:
                wrapped_response.append(line)
        return wrapped_response

    async def update_progress(self, value):
        self.progress_bar.progress = value
        await asyncio.sleep(0.01)



if __name__ == "__main__":
    AIChatApp().run()
