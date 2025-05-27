from Chatbot import ChatOllama
from Tools import add_two_numbers, set_color

class Agent:

    def __init__(self, model_name, tools_dict):
        self.tools_mapping = tools_dict
        self.chatbot = ChatOllama(model_name, tools=self._get_tools_list())

    def _get_tools_list(self):
        return list(self.tools_mapping.values())

    def run(self, query):
        response = self.chatbot.chat(query)[1]
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
        return True, result

    def run_loop(self):
        while True:
            try:
                query = input('>Ask: ')
            except KeyboardInterrupt:
                break
            if query.lower() in ['exit', 'quit']:
                break
            self.run(query)
        print('\nExiting...')


FUNCTION_TOOLS_MAPPER  = {
  'add_two_numbers': add_two_numbers,
  'set_color': set_color
}

if __name__ == "__main__":
    agent = Agent('qwen3:14b', tools_dict=FUNCTION_TOOLS_MAPPER)
    #agent.run("Set a orange color with 10 percent brightness")
    agent.run_loop()
