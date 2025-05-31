try:
    from .Chatbot import ChatOllama
    from .Tools import generate_tools
except ImportError:
    from Chatbot import ChatOllama
    from Tools import generate_tools
import re


class Agent(ChatOllama):

    def __init__(self, model_name, tools_dict):
        self.tools_mapping = tools_dict
        super().__init__(model_name, tools=self._get_tools_list())

    def _get_tools_list(self):
        return list(self.tools_mapping.values())

    def chat(self, query):
        response = super().chat(query)[1]
        result = {}
        # Handle the Tool Response
        for tool in response.message.tool_calls or []:
            function_to_call = self.tools_mapping.get(tool.function.name)
            if function_to_call:
                result[tool.function.name] = function_to_call(**tool.function.arguments)
                print('Function output:', result[tool.function.name])
            else:
                result[tool.function.name] = f"Function {tool.function.name} not found"
                print(result[tool.function.name])
        return True, {"response": response, "tool_result": result}

    @staticmethod
    def human_output_parser(response):
        _response = ChatOllama.human_output_parser(response["response"])
        # Remove everything between <think> and </think>, including the tags
        _response = re.sub(r"<think>.*?</think>", "", _response, flags=re.DOTALL)
        _response = f"Thinking...\n{_response}"
        _tool_result = str(response["tool_result"])
        return _response + "\n" + _tool_result


def craft_agent_proto1(model_name='qwen3:14b'):
    _agent = Agent(model_name, tools_dict=generate_tools())
    return _agent

if __name__ == "__main__":
    agent = craft_agent_proto1()
    #agent.chat("Set a orange color with 10 percent brightness")
    agent.chat_loop()
