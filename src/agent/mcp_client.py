from contextlib import AsyncExitStack
from typing import Optional
from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.client.streamable_http import streamable_http


class MCPClient:
    def __init__(self, server_url, transport="sse"):
        self.server_url = server_url
        self.transport = transport

        self.tools = []
        self.exit_stack = AsyncExitStack()
        self.session: ClientSession = None

    async def __aenter__(self):
        await self.connect_to_server()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.exit_stack.aclose()

    async def connect_to_server(self):
        # 连接服务器
        try:
            if self.transport == "sse":
                await self._connect_sse
            elif self.transport == "streamable-http":
                await self._connect_http()
            else:
                raise ValueError(f"Unsupported transport: {self.transport}")
            await self.session.initialize()
        except Exception as e:
            print(f"Error connecting to server: {e}")
            return False
        # 获取工具
        self.tools = await self.session.list_tools
        return True

    async def get_available_tools(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.parameters,
                    "input_schema": tool.input_schema,
                    "output_schema": tool.output_schema,
                },
            }
            for tool in self.tools
        ]

    async def call_tool(self, tool_name, tool_args):
        try:
            call_result = await self.session.call_tool(tool_name, tool_args)
            return call_result.content[0].text
        except Exception as e:
            print(f"Error calling tool: {e}")
            return None

    async def _connect_http(self):
        read_stream, write_stream, _ = await self.exit_stack.enter_async_context(
            streamable_http(self.server_url)
        )
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )

    async def _connect_sse(self):
        read_stream, write_stream = await self.exit_stack.enter_async_context(
            sse_client(self.server_url)
        )
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )
