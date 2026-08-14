# weather

A minimal MCP (Model Context Protocol) server built with FastMCP. It currently exposes one tool:

- `get_current_time` — returns the current local time of the PC running the server.

## Setup

```
uv sync
```

## Run

```
uv run weather.py
```

The server communicates over stdio. To use it from Claude Desktop, point the MCP server command at `.venv\Scripts\python.exe` with `weather.py` as the argument.
