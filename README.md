# Create a new directory for project
uv init visual
cd visual

# Create virtual environment and activate it
uv venv
source .venv/bin/activate

# Install dependencies
uv add "mcp[cli]" httpx

# Create our server file
touch visual.py

Install required dependencies: pip install mcp httpx fastapi uvicorn

from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("visual_code_server")

async def get_code(url: str) -> str:
    """
    Fetch source code from a GitHub URL.
    
    Args:
        url: GitHub URL of the code file
    Returns:
        str: Source code content or error message
    """
    USER_AGENT = "visual-fastmcp/0.1"

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "text/html"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            # Convert GitHub URL to raw content URL
            raw_url = url.replace("github.com", "raw.githubusercontent.com")\
                        .replace("/blob/", "/")
            response = await client.get(raw_url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.text
        except Exception as e:
            return f"Error fetching code: {str(e)}"
