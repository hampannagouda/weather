# weather

A minimal MCP (Model Context Protocol) server built with FastMCP. It currently exposes one tool:

- `get_current_time` — returns the current local time of the PC running the server.

## Setup

```
uv sync
```

## Run locally (stdio)

```
uv run weather.py
```

By default the server communicates over stdio. To use it from Claude Desktop, point the MCP server command at `.venv\Scripts\python.exe` with `weather.py` as the argument.

## Run for a remote client on your LAN (HTTP + auth)

Set an auth token once — copy `.env.example` to `.env` and fill in `MCP_AUTH_TOKEN` (generate one with `python -c "import secrets; print(secrets.token_urlsafe(32))"`). Every request must then include this token; without it the server refuses to start in HTTP mode.

Start the server bound to all interfaces so other machines on the network can reach it:

```powershell
$env:MCP_TRANSPORT = "http"
$env:MCP_HOST = "0.0.0.0"
uv run weather.py
```

By default (`MCP_HOST` unset) it binds to `127.0.0.1` only, reachable solely from this machine — useful for local testing.

**Windows Firewall**: an inbound rule must allow traffic on the port (default 8000) before another device can connect. Run this once, in an elevated PowerShell, on this machine:

```powershell
New-NetFirewallRule -DisplayName "Weather MCP server" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow -Profile Private
```

Find this machine's LAN IP with `ipconfig` (look for the "IPv4 Address" under your active network adapter). Give the remote client, which must be on the same network (or VPN) as this machine:
- **URL**: `http://<this machine's LAN IP>:8000/mcp`
- **Header**: `Authorization: Bearer <MCP_AUTH_TOKEN value>`

The token is a shared secret — treat it like a password and rotate it (generate a new one, update `.env`, restart the server) if it's ever exposed. Traffic is plain HTTP (not HTTPS) on the LAN — acceptable for a trusted internal network, but the token is the only thing standing between an on-path observer and the request contents.
