import io
import os
from itertools import chain

from src.agent.llm_service import LLMService
from src.agent.mcp_client import MCPClient
from src.util import interact_utils


class Agent:
    def __init__(self, name, description):
        self.name = name
        self.description = description

        self.mcp_server_url = None
        self.mcp_transport = None
        self.tools = []

    async def try_mcp_connect(self, server_url, transport):
        self.mcp_server_url = server_url
        self.mcp_transport = transport
        async with MCPClient(self.mcp_server_url, self.mcp_transport) as client:
            if client.is_connected:
                self.tools = client.get_available_tools()
            return client.is_connected

    def disconnect_mcp(self):
        self.tools = []

    def process_query(self, query):
        # 初始化模型
        model_name = interact_utils.get_session_value('model_name')
        if not model_name:
            model_name = os.environ.get('model_name')
        base_url = os.environ.get('base_url')
        api_key = os.environ.get('api_key')
        llm_service = LLMService(base_url, api_key)

        if self.tools:
            print('chat with tools:\n', self.tools)
        res_stream = llm_service.chat(model_name, self._user_msg(query), self.tools)

        # TODO
        if model_name.startswith('deepseek-ai'):
            return self._deepseek_stream(res_stream)
        elif model_name.startswith('Qwen'):
            return self._qwen_stream(res_stream)
        return False, res_stream

    async def call_tool(self, tool_name, tool_input):
        if self.mcp_server_url and not self.mcp_transport:
            async with MCPClient(self.mcp_server_url, self.mcp_transport) as client:
                if client.is_connected:
                    return await client.call_tool(tool_name, tool_input)
        else:
            print('\n Mcp Server info required.')
        return None

    @staticmethod
    def _user_msg(query):
        return [{"role": "user", "content": query}]

    @staticmethod
    def _deepseek_stream(res_stream):
        is_use_tool = False
        # first_chunk = None
        first_content = ''
        tool_call_final = {
            'id': '',
            'type': '',
            'function': {
                'name': '',
                'arguments': ''
            }
        }

        for chunk in res_stream:
            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta
            if delta.content:
                is_use_tool = False
                # first_chunk = chunk
                first_content = delta.content
                break

            if delta.tool_calls:
                is_use_tool = True
                tool_call = delta.tool_calls[0]
                if tool_call.function.name:
                    tool_call_final['function']['name'] += tool_call.function.name
                if tool_call.function.arguments:
                    tool_call_final['function']['arguments'] += tool_call.function.arguments

        if not is_use_tool:
            return is_use_tool, chain(first_content, res_stream)
            # return is_use_tool, res_stream
        else:
            return is_use_tool, io.StringIO(
                f'<tool_call>{{"name":"{tool_call_final['function']['name']}","arguments":"{tool_call_final['function']['arguments']}"}}</tool_call>')

    @staticmethod
    def _qwen_stream(res_stream):
        is_use_tool = False
        first_content = ''
        for chunk in res_stream:
            first_content = chunk.choices[0].delta.content
            if first_content == '<tool_call>':
                is_use_tool = True
            break

        return is_use_tool, chain(first_content, res_stream)

    @staticmethod
    def _concat_stream(first, res_stream):
        return chain(first, res_stream)
