from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Input, Button, Log, Select, Static, ProgressBar
import asyncio
import textwrap

from lib import Models
from lib import Chatbot

class EchoChatApp(App):
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("escape", "quit", "Quit"),
    ]

    CSS = """
    #title-bar {
        height: 3;
        content-align: center middle;
        background: black;
    }

    #main-layout {
        height: 1fr;
    }

    #sidebar {
        width: 25%;
        padding: 1;
        border: solid grey;
    }

    #chat-area {
        width: 75%;
    }

    Log {
        height: 1fr;
        border: solid green;
    }

    ProgressBar {
        height: 1;
        margin: 0 1;
    }

    Input, Button {
        height: 3;
    }

    #input_bar {
        dock: bottom;
        height: auto;
    }

    #quit-button {
        margin-left: 1;
    }
    """

    def __init__(self):
        super().__init__()
        self.chatbot = None
        self.model_dropdown = Models.get_models_dropdown()

    def init_model(self, model_name):
        if self.chatbot:
            if self.chatbot.model_name == model_name:
                return
        self.chatbot = Chatbot.ChatOllama(model_name)

    def compose(self) -> ComposeResult:
        # Title bar with styled markup
        yield Static("[b green]Nolora[/]", id="title-bar", markup=True)

        with Horizontal(id="main-layout"):
            # Sidebar with dropdown
            with Vertical(id="sidebar"):
                self.dropdown = Select(
                    options=self.model_dropdown,
                    prompt="Select a model...",
                    id="dropdown"
                )
                yield self.dropdown

            # Chat area
            with Vertical(id="chat-area"):
                self.chat = Log(id="chat")
                yield self.chat

                self.progress = ProgressBar(total=100)
                yield self.progress

                with Horizontal(id="input_bar"):
                    self.input = Input(placeholder="Type a message...", id="input")
                    yield self.input
                    yield Button("Send", id="send")
                    yield Button("Quit", id="quit-button")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "send":
            await self.process_message()
        elif event.button.id == "quit-button":
            self.exit()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        await self.process_message()

    async def process_message(self) -> None:
        message = self.input.value.strip()
        if not message:
            return

        selected_option = self.dropdown.value
        self.init_model(selected_option)

        self.chat.write_line(f"You: {message}")
        response = self._chat_model_process(message)
        if isinstance(response, list):
            self.chat.write_line(f"{selected_option}")
            self.chat.write_lines(response)
        else:
            self.chat.write_line(f"{selected_option}: {response}")

        self.input.value = ""

    def _chat_model_process(self, query):
        # Animate progress bar
        #self.progress.progress = 100
        #await asyncio.sleep(2)
        #self.progress.progress = 0
        self.progress.progress = 100
        if self.chatbot:
            state, response = self.chatbot.chat(query)
            response = response.message.content
        else:
            response = "No chatbot initialized"
        self.progress.progress = 0

        box_width = 80
        if len(response) > box_width:
            # Wrap the response text to fit inside the Log widget width
            max_width = self.chat.size.width or box_width  # Fallback width
            response = textwrap.wrap(response, width=max_width - 4)

        return response

    def action_quit(self) -> None:
        self.exit()


if __name__ == "__main__":
    EchoChatApp().run()
