## Heartbeat

`GatewayHeartbeatService` — an `asyncio` timer that sends a chat message through AgentClient at a configurable interval. Default: disabled. When enabled, defaults to 60s interval targeting the "web" channel.

## Startup

`start_services.py` — starts `app_agentserver` and a Gateway script as `subprocess.Popen`, waits for either to exit, handles Ctrl+C gracefully.
