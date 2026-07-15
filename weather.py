#https://github.com/modelcontextprotocol/quickstart-resources/blob/main/weather-server-python/weather.py

from typing import Any

import httpx

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any]:
