try:
    from .ChatOllama import ChatOllama
    from .Tools import generate_tools
except ImportError:
    from ChatOllama import ChatOllama
    from Tools import generate_tools

import re
import json


class Agent(ChatOllama):

    def __init__(self, model_name, max_tool_steps=5, tui_console=None):
        """
        Initialize an Agent with a specific model and tools.
        Args:
            model_name: model name to use for generating responses
            tools_dict: dictionary mapping tool names to their corresponding functions or classes
            max_tool_steps: maximum number of steps allowed for a single tool execution (prevent infinite loops)
        """
        self.tools_mapping = generate_tools()
        self.max_tool_steps = max_tool_steps
        super().__init__(model_name, tools=self._get_tools_list(), tui_console=tui_console)

    def _get_tools_list(self):
        return list(self.tools_mapping.values())

    def add_function_message(self, name, content, tool_call_id=None):
        """
        Add a function (tool) response to the chat history.
        This mimics the tool result message expected by the model.
        """
        function_msg = {
            "role": "tool",
            "name": name,
            "content": content if isinstance(content, str) else str(content)
        }
        if tool_call_id is not None:
            function_msg["tool_call_id"] = tool_call_id
        self.messages.append(function_msg)

    def _tool_call(self, tool):
        """
        Execute a single tool and return its result.
        """
        tool_result = {}
        fn_name = tool.function.name

        # Handle arguments: accept dict or JSON string
        if isinstance(tool.function.arguments, dict):
            fn_args = tool.function.arguments
        else:
            try:
                fn_args = json.loads(tool.function.arguments or "{}")
            except json.JSONDecodeError:
                fn_args = {}
                self.print(f"[Warning] Could not decode arguments for tool '{fn_name}': {tool.function.arguments}")

        # Resolve callable - function with its parameters
        fn = self.tools_mapping.get(fn_name)
        # Try to get the tool call id safely
        tool_call_id = getattr(tool, 'tool_call_id', None) or getattr(tool, 'call_id', None)

        if fn:
            try:
                result = fn(**fn_args)
                tool_result[fn_name] = result
                self.print(f"[Tool] {fn_name}({fn_args}) => {result}")
                self.add_function_message(name=fn_name, content=result, tool_call_id=tool_call_id)
            except Exception as e:
                error_msg = f"[Error calling {fn_name}]: {e}"
                tool_result[fn_name] = error_msg
                self.print(error_msg)
                self.add_function_message(name=fn_name, content=error_msg, tool_call_id=tool_call_id)
        else:
            error_msg = f"[Function {fn_name} not found]"
            tool_result[fn_name] = error_msg
            self.print(error_msg)
            self.add_function_message(name=fn_name, content=error_msg, tool_call_id=tool_call_id)

        return tool_result

    def chat(self, query):
        """
        Chat with the model and support iterative tool usage.
        """
        self.add_user_message(query)
        tool_result = {}
        response = {}

        for _ in range(self.max_tool_steps):
            response = self.run_model(stream=self.stream)
            message = response.message
            tool_calls = message.tool_calls or []

            # Add assistant message (text response and tool metadata)
            if message.content:
                self.add_assistant_message(message.content)

            if not tool_calls:
                break  # No tools requested, we're done

            for tool in tool_calls:
               tool_result.update(self._tool_call(tool))

        return True, {"response": response, "tool_result": tool_result}

    def human_output_parser(self, response, remove_thinking=True):
        _response = ChatOllama.human_output_parser(response["response"])
        if remove_thinking:
            _is_thinking = "<think>" in _response.lower()
            _response = re.sub(r"<think>.*?</think>", "", _response, flags=re.DOTALL)
            _response = f"{'Thinking...\n' if _is_thinking else ''}{_response}".strip()
        _tool_result = str(response["tool_result"])

        _response = _response + "\n\n" + _tool_result
        self.write_tui(f"Assistant {self.model_name}:")
        self.write_tui(_response)
        return _response


if __name__ == "__main__":
    agent = Agent(model_name='qwen3:4b', tui_console=None)
    agent.chat_loop()
