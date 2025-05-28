#!/usr/bin/env python3

# https://textual.textualize.io/widget_gallery/

from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Input, Button, Log, Select, Static, ProgressBar, Footer
import asyncio
import textwrap
import time

# LLM libraries
from lib import Models
from lib import Chatbot


def load_css():
    with open("./textual.tcss", "r") as f:
        textual_css = f.read()
    return textual_css


class AIChatApp(App):
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("escape", "quit", "Quit"),
    ]
    CSS = load_css()

    def __init__(self):
        self.chatbot:Chatbot.ChatOllama|None = None
        self.model_dropdown = Models.get_chat_models_dropdown()
        # Initialize global textual.widgets widgets
        self.progress_bar = ProgressBar(total=100, id="progress-bar")
        self.timer_display = Static("⏱️  Time taken: 0s", id="timer-display")
        # Initialize global parameters for textual.widgets
        self.chatbox:Log|None = None
        self.input:Input|None = None
        self.dropdown:Select|None = None
        super().__init__()

    def init_model(self, model_name):
        if self.chatbot:
            if self.chatbot.model_name == model_name:
                return
        self.chatbot = Chatbot.ChatOllama(model_name)

    def compose(self) -> ComposeResult:
        # Title bar with styled markup
        yield Static("[b green]Nolara[/]", id="title-bar", markup=True)

        with Horizontal(id="main-layout"):
            # Sidebar with dropdown
            with Vertical(id="sidebar"):
                self.dropdown = Select(
                    options=self.model_dropdown,
                    value=self.model_dropdown[0][1],
                    prompt="Select a model...",
                    id="dropdown",
                )
                yield self.dropdown

            # Chat area
            with Vertical(id="chat-area"):
                self.chatbox = Log(id="chat")
                yield self.chatbox

                with Horizontal(id="progress-line"):
                    yield self.progress_bar
                    yield self.timer_display

                with Horizontal(id="input_bar"):
                    self.input = Input(placeholder="Type a message...", id="input")
                    yield self.input
                    yield Button("Send", id="send-button")
                    # TODO Speaker button (Speak)
                    # TODO Microphone button (Listen)

        # Footer showing keybindings (q or Esc to quit)
        yield Footer(id="app-footer")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "send-button":
            await self.process_message()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        await self.process_message()

    async def process_message(self) -> None:
        message = self.input.value.strip()
        if not message:
            return

        selected_option = self.dropdown.value
        self.init_model(selected_option)

        self.chatbox.write_line("_" * (self.chatbox.size.width-4))
        await self.update_progress(10)
        self.chatbox.write_line(f"\nYou: {message}")
        start_time = time.time()
        response = self._chat_model_process(message)
        await self.update_progress(80)
        duration = time.time() - start_time
        self.timer_display.update(f"⏱️  Time taken: {duration:.2f}s")

        if isinstance(response, list):
            self.chatbox.write_line(f"{selected_option}:")
            self.chatbox.write_lines(response)
        else:
            self.chatbox.write_line(f"{selected_option}: {response}")

        # Animate progress bar - dummy
        await self.update_progress(100)
        await asyncio.sleep(0.1)
        #self.progress_bar.progress = 0

        self.input.value = ""

    async def update_progress(self, value):
        self.progress_bar.progress = value
        await asyncio.sleep(0.01)

    def _wrap_response(self, response):
        box_width = self.chatbox.size.width -4
        response_lines = response.split('\n')
        wrapped_response = []
        for line in response_lines:
            if len(line) > box_width:
                # Wrap the response text to fit inside the Log widget width
                wrapped_response += textwrap.wrap(response, width=box_width)
            else:
                wrapped_response.append(line)
        return wrapped_response

    def _chat_model_process(self, query, wrap=True):
        if self.chatbot:
            state, response = self.chatbot.chat(query)
            response = response.message.content
        else:
            response = "No chatbot initialized"

        if wrap:
            response = self._wrap_response(response)

        return response

    def action_quit(self) -> None:
        self.exit()


if __name__ == "__main__":
    AIChatApp().run()
