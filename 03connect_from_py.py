import asyncio
import json
from websockets.asyncio.client import connect

async def test():
    async with connect("ws://127.0.0.1:19000/ws") as ws:
        # Read the connection ack
        ack = json.loads(await ws.recv())
        print("Ack:", ack["event"])  # connection.ack

        # Send a request
        await ws.send(json.dumps({
            "type": "req",
            "id": "abc",
            "method": "chat.send",
            "params": {"query": "Hello!"},
        }))

        # Read the echo response
        res = json.loads(await ws.recv())
        print("Response:", res["payload"]["echo"])  # Hello!

asyncio.run(test())