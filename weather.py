import os
import sys
from datetime import datetime

import uvicorn
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from starlette.datastructures import Headers
from starlette.responses import JSONResponse
from starlette.types import Receive, Scope, Send

load_dotenv()

mcp = FastMCP(
    "time-server",
    host=os.environ.get("MCP_HOST", "127.0.0.1"),
    port=int(os.environ.get("MCP_PORT", "8000")),
)


@mcp.tool()
async def get_current_time() -> str:
    """Get the current local time from the PC running the MCP server."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


class BearerTokenMiddleware:
    """Rejects any HTTP request that doesn't carry the configured bearer token."""

    def __init__(self, app, token: str):
        self.app = app
        self.token = token

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        if Headers(scope=scope).get("authorization") != f"Bearer {self.token}":
            await JSONResponse({"error": "unauthorized"}, status_code=401)(scope, receive, send)
            return
        await self.app(scope, receive, send)


def run_http() -> None:
    token = os.environ.get("MCP_AUTH_TOKEN")
    if not token:
        sys.exit("MCP_AUTH_TOKEN is not set. Put it in .env or export it before starting the server.")

    app = BearerTokenMiddleware(mcp.streamable_http_app(), token)
    uvicorn.run(app, host=mcp.settings.host, port=mcp.settings.port, log_level=mcp.settings.log_level.lower())


if __name__ == "__main__":
    if os.environ.get("MCP_TRANSPORT", "stdio") == "http":
        run_http()
    else:
        mcp.run()
