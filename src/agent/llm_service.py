from openai import OpenAI


class LLMService:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.openai = OpenAI(base_url=base_url, api_key=api_key)

    def chat_raw(self, model_name, messages, tools, stream=True):
        try:
            res_stream = self.openai.chat.completions.create(
                model=model_name, messages=messages, tools=tools,
                max_tokens=2000, temperature=0.7, stream=stream,
            )
            return res_stream
        except Exception as e:
            print(e)
            raise RuntimeError(f"发送消息到LLM失败: {str(e)}") from e

    def chat(self, model_name, messages, tools, stream=True):
        # TODO
        return self.chat_raw(model_name, messages, tools, stream)


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv

    load_dotenv()

    env_base_url = os.environ.get("base_url")
    env_api_key = os.environ.get("api_key")
    env_model_name = os.environ.get("model_name")

    llm_service = LLMService(env_base_url, env_api_key)
    use_stream = True

    # res = llm_service.chat(env_model_name, [{"role": "user", "content": "你好"}], [], stream=use_stream)

    import json

    with open('./tools_example.json', encoding='utf8') as fp:
        tools = json.load(fp)
    res = llm_service.chat(env_model_name, [{"role": "user", "content": "当前时间是多少"}], tools, stream=use_stream)

    if use_stream:
        tool_call_final = {
            'id': '',
            'type': '',
            'function': {
                'name': '',
                'arguments': ''
            }
        }
        for chunk in res:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta
            if delta.content:
                print(delta.content)

            if delta.tool_calls:
                tool_call = delta.tool_calls[0]
                if tool_call.function.name:
                    tool_call_final['function']['name'] += tool_call.function.name
                if tool_call.function.arguments:
                    tool_call_final['function']['arguments'] += tool_call.function.arguments
        print(tool_call_final)
        # print(chunk.choices[0].delta)
        # print(chunk.choices[0].delta.content)
    else:
        if res.choices[0].finish_reason == 'tool_calls':
            print(f'function name: {res.choices[0].message.tool_calls[0].function.name}')
            print(f'function args: {res.choices[0].message.tool_calls[0].function.arguments}')
        else:
            print(res.choices[0].message.content)
