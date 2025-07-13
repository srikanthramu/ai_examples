from fastmcp import FastMCP, Context
from starlette.responses import PlainTextResponse

# MCP server demo built using fastmcp
server = FastMCP(name="Math Tools")

# Tool with addition logic
@server.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Tool defintion with fastmcp annotations
@server.tool(
        name= "health_check",
        description="Returns health of the MCP Server"
    )
def health_check() -> PlainTextResponse:
    return PlainTextResponse("OK")

# Resource is returing system details accessing context 
@server.resource("resource://system-details")
async def get_system_status(ctx: Context) -> dict:
    """Provides system status information."""
    return {
        "version": "beta",
        "status": "OK",
        "request_id": ctx.request_id
    }


# Running http streamable server
if __name__ == "__main__":
    server.run(
        transport="http",
        host="127.0.0.1",
        port=4200,
        path="/mcp",
        log_level="debug"
    )