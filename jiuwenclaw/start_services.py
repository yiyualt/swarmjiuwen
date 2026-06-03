"""Launch JiuwenClaw — AgentServer + Gateway in two subprocesses.

Usage: ``jiuwenclaw-start``
"""

from __future__ import annotations

import subprocess
import sys
import time


def main() -> None:
    python = sys.executable

    # Start AgentServer
    agent = subprocess.Popen([python, "-m", "jiuwenclaw.app_agentserver"])
    time.sleep(0.5)

    # Start Gateway (WebChannel)
    gateway = subprocess.Popen([
        python, "-c", """
import asyncio
from jiuwenclaw.channel.web_channel import WebChannel, WebChannelConfig

async def main():
    channel = WebChannel(WebChannelConfig())
    await channel.start()
    print("=== Gateway ready: ws://127.0.0.1:19000/ws ===")
    await asyncio.Event().wait()

asyncio.run(main())
"""])

    procs = [agent, gateway]

    def _stop():
        for p in procs:
            if p.poll() is None:
                p.terminate()
        deadline = time.time() + 8
        while time.time() < deadline:
            if all(p.poll() is not None for p in procs):
                break
            time.sleep(0.1)
        for p in procs:
            if p.poll() is None:
                p.kill()

    try:
        while True:
            if agent.poll() is not None or gateway.poll() is not None:
                break
            time.sleep(0.25)
    except KeyboardInterrupt:
        pass
    finally:
        _stop()


if __name__ == "__main__":
    main()
