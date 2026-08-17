# Remote Access — What Was Done & What You Need To Do

This file explains, in plain language, how this server was changed so a
client on another computer can use it, and the steps you need to take
to actually turn that on.

## What this server does

It's a small program that answers one question: "what time is it on this
PC?" Claude Desktop already talks to it directly on this same computer.
The ask was: let some other computer ("the client") ask it the same
question over the network.

## What was done

1. **Added a second way to talk to the server.**
   Before, the server only understood requests from a program running on
   the *same* PC (this is called "stdio"). Claude Desktop still uses this
   exact same method — nothing changed for it. A second mode was added
   that the server can run in instead, which listens on the network like
   a website does, so another computer can send it requests.

2. **Added a password check (the "token").**
   Anyone who can reach the server over the network would be able to
   use it — so a secret password (called a "token") was added. The
   server now refuses every request unless it includes the correct
   token. A random token has already been generated for you and saved
   in a file called `.env` in this folder. That file is deliberately
   **not** uploaded to GitHub, since it's a secret.

3. **Tried to make it reachable from anywhere on the internet — this
   part didn't work.**
   The original plan was to use a free "tunnel" service (Cloudflare) so
   the client could reach the server from anywhere, without you needing
   to change router or firewall settings. This was blocked by your
   company's network security (Unisys's Cisco Umbrella filter blocks
   tunnel services), so that option was dropped.

4. **Switched the plan to "same network only" instead.**
   Instead of the whole internet, the server can now be reached by
   any other device on the **same office/home network** (or over a
   VPN connection into that network). This needs no tunnel and no
   internet exposure — the client just has to be on the same network
   as this PC when it connects.

## What you need to do to actually turn this on

Nothing runs automatically — these steps have to be done each time you
want the service reachable.

### Step 1 — Allow the connection through Windows Firewall (do this once)

Windows blocks incoming network connections by default. Run this once,
in a PowerShell window opened **as Administrator**:

```powershell
New-NetFirewallRule -DisplayName "Weather MCP server" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow -Profile Private
```

This wasn't done for you automatically — changing firewall/security
settings is something you need to approve and run yourself.

### Step 2 — Start the server in "network mode"

Normally the server only listens for Claude Desktop on this same PC. To
make it listen for other devices on the network, open a normal
PowerShell window in this project folder and run:

```powershell
$env:MCP_TRANSPORT = "http"
$env:MCP_HOST = "0.0.0.0"
uv run weather.py
```

Leave this window open — closing it stops the server. If you close it
and reopen it later, run the same two lines again.

### Step 3 — Find this PC's network address

Run this to find the address other devices will use to reach this PC:

```powershell
ipconfig
```

Look for "IPv4 Address" under your active network connection (Wi-Fi or
Ethernet) — it'll look something like `10.80.35.54`.

### Step 4 — Give the client two things

Whoever is setting up the remote client needs:

- **The address**: `http://<the IPv4 address from Step 3>:8000/mcp`
- **The token (password)**: open the `.env` file in this folder and
  copy the value after `MCP_AUTH_TOKEN=`

They must be on the same network (or VPN into it) as this PC, and this
PC's server (Step 2) has to be running, for it to work.

## Things to keep in mind

- **The token is a password.** Don't post it anywhere public (chat
  channels, tickets, committed files). If it ever leaks, generate a new
  one, put it in `.env`, and restart the server — the old one stops
  working immediately.
- **This only works on the same network**, not from home or a coffee
  shop, unless the client connects through a VPN into that network
  first.
- **The traffic isn't encrypted** (it's `http://`, not `https://`) —
  fine for a trusted internal office network, but the token is the only
  thing protecting it. If this ever needs to work from outside the
  network, that's a bigger change (a real domain with HTTPS, or getting
  IT to approve a tunnel exception) and should be revisited then.
