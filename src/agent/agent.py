
class Agent:
    def __init__(self, name, description, tools):
        self.name = name
        self.description = description
        self.tools = tools

        self.mcp_server_url = None
        self.mcp_transport = None

    def try_mcp_connect(server_url, transport):
        self.mcp_server_url = server_url
        self.mcp_transport = transport
        pass

    def process_query(query):
        pass

    def call_tool(tool_name, tool_input):
        pass