"""Standalone AgentServer entry point — ``jiuwenclaw-agentserver``."""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from pathlib import Path

# Wire up vendor
_vendor_root = Path(__file__).resolve().parent / "vendor" / "openjiuwen"
if str(_vendor_root) not in sys.path:
    sys.path.insert(0, str(_vendor_root))

from dotenv import load_dotenv
from jiuwenclaw.utils import get_env_file

load_dotenv(dotenv_path=get_env_file())

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(name)s] %(message)s")
_logger = logging.getLogger("agent_server")


async def _run(host: str, port: int) -> None:
    from jiuwenclaw.agentserver.agent_ws_server import AgentWebSocketServer

    server = AgentWebSocketServer(host=host, port=port)
    await server.start()
    _logger.info("AgentServer ready: ws://%s:%s  Ctrl+C to stop", host, port)

    stop = asyncio.Event()
    try:
        await stop.wait()
    except KeyboardInterrupt:
        pass
    finally:
        await server.stop()


def main() -> None:
    host = os.getenv("AGENT_SERVER_HOST", "127.0.0.1")
    port = int(os.getenv("AGENT_SERVER_PORT", "18092"))
    asyncio.run(_run(host, port))


if __name__ == "__main__":
    main()
