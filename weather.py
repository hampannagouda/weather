from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("time-server")

@mcp.tool()
async def get_current_time() -> str:
    """Get the current local time from the PC running the MCP server."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

if __name__ == "__main__":
    mcp.run()