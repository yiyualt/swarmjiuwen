"""Orchestrate AgentServer + Gateway in two subprocesses."""

from __future__ import annotations

import subprocess
import sys
import time


def main() -> None:
    python = sys.executable

    agent = subprocess.Popen([python, "-m", "jiuwenclaw.app_agentserver"])
    gateway = None
    try:
        time.sleep(0.5)
        gateway = subprocess.Popen([python, "-c", """
import asyncio
from jiuwenclaw.channel.web_channel import WebChannel, WebChannelConfig

async def main():
    channel = WebChannel(WebChannelConfig())
    await channel.start()
    print("Gateway ready: ws://127.0.0.1:19000/ws")
    await asyncio.Event().wait()

asyncio.run(main())
"""])
    except Exception:
        agent.terminate()
        raise

    procs = [agent, gateway]

    def _terminate():
        for p in procs:
            if p.poll() is None:
                p.terminate()
        time.sleep(0.5)
        for p in procs:
            if p.poll() is None:
                p.kill()

    try:
        while True:
            if agent.poll() is not None:
                break
            if gateway.poll() is not None:
                break
            time.sleep(0.25)
    except KeyboardInterrupt:
        pass
    finally:
        _terminate()


if __name__ == "__main__":
    main()
