from openai import OpenAI


class LLMService:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        self.openai = OpenAI(api_key=api_key, base_url=base_url)

    def chat(self, model_name, messages, tools):
        try:
            stream = self.openai.chat.completions.create(
                model=model_name,
                messages=messages,
                tools=tools,
                max_tokens=2000,
                temperature=0.7,
                stream=True,
            )
            return stream
        except Exception as e:
            print(e)
            raise Exception("发送消息到LLM失败", e)
