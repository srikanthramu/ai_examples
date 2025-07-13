import asyncio
from fastmcp import Client, FastMCP

# MCP Client implmentation using fastmcp
async def main():
    # Connecting to local mcp demo server
    client = Client("http://127.0.0.1:4200/mcp")
    async with client: 
        print(f"Connected: {client.is_connected()}")
        await tool_request(client)
        await resource_request(client)
    print(f"Connected: {client.is_connected()}")


# Listing available Tools and Tool calling
async def tool_request(client):
    tools = await client.list_tools()
    for tool in tools:
        print(f"Tool: {tool}")
    
    result = await client.call_tool(name="add", arguments={"a": 5, "b": 3})
    print(f"Result of add: {result.content[0].text}")


# Listing available resources and featching them
async def resource_request(client):
    resources = await client.list_resources()
    for resource in resources:
        print(f"Resource:  {resource}")
    
    result = await client.read_resource("resource://system-details")
    print(f"Resource Content : {result[0].text}")


# Main runnner
if __name__ == "__main__":
    asyncio.run(main())