import asyncio
from fastmcp import Client, FastMCP

# MCP Client built using fastmcp
class MCPClientHandler:
    def __init__(self, url="http://127.0.0.1:4200/mcp"):
        self.url = url
        self.client = Client(self.url)
    # Add tool calling
    async def add_request(self, a, b):
        async with self.client:
            result = await self.client.call_tool(name="add", arguments={"a": a, "b": b})
            return result.content[0].text

# main running
if __name__ == "__main__":
    handler = MCPClientHandler()
    # Addition parameters can be changed
    a = asyncio.run(handler.add_request(a=5, b=10))
