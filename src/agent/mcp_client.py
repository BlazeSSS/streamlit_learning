from contextlib import AsyncExitStack
from typing import Optional

from mcp import ClientSession
from mcp.client.sse import sse_client
from mcp.client.streamable_http import streamablehttp_client


class MCPClient:
    def __init__(self, server_url, transport="sse"):
        self.server_url = server_url
        self.transport = transport

        self.tools = []
        self.is_connected = False

        self.exit_stack = AsyncExitStack()
        self.session: Optional[ClientSession] = None

    async def __aenter__(self):
        await self.connect_to_server()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.exit_stack.aclose()

    async def connect_to_server(self):
        # 连接服务器
        try:
            if self.transport == "sse":
                await self._connect_sse()
            elif self.transport == "streamable-http":
                await self._connect_http()
            else:
                raise ValueError(f"Unsupported transport: {self.transport}")
            await self.session.initialize()
        except ExceptionGroup as eg:
            for ex in eg.exceptions:
                print(f"\nException connecting to server: ", ex)
            self.is_connected = False
            return
        except Exception as e:
            print(f"\nError connecting to server.", e)
            self.is_connected = False
            return
        # 获取工具
        list_tools_result = await self.session.list_tools()
        self.tools = list_tools_result.tools
        self.is_connected = True

    def get_available_tools(self):
        return [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema,
            }
        } for tool in self.tools]

    async def call_tool(self, tool_name, tool_args):
        if not self.session:
            print('Not connected to MCP Server.')
            return None

        try:
            call_result = await self.session.call_tool(tool_name, tool_args)
            return call_result.content[0].text
        except ExceptionGroup as eg:
            for ex in eg.exceptions:
                print(f"\nException connecting to server: ", ex)
            return None
        except Exception as e:
            print(f"Error calling tool: {e}")
            return None

    async def _connect_http(self):
        read_stream, write_stream, _ = await self.exit_stack.enter_async_context(
            streamablehttp_client(self.server_url)
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


async def main():
    async with MCPClient('http://127.0.0.1:8000/sse', 'sse') as client:
        print(client.is_connected)
        print(client.get_available_tools())
        # print(await client.call_tool('get_current_time', ''))

    async with MCPClient('http://127.0.0.1:8085/mcp', 'streamable-http') as client:
        print(client.is_connected)
        print(client.get_available_tools())


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
