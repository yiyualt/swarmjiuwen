import asyncio, json
from websockets.asyncio.client import connect

async def chat():
    async with connect("ws://127.0.0.1:19000/ws") as ws:
        ack = json.loads(await ws.recv())
        print("ACK:", ack["event"])

        await ws.send(json.dumps({
            "type": "req",
            "id": "abc",
            "method": "chat.send",
            "params": {"query": "What is Python?"},
        }))

        # Read all responses until we get the final res
        while True:
            raw = await ws.recv()
            msg = json.loads(raw)
            print(f"\n[{msg['type']}]", json.dumps(msg, indent=2, ensure_ascii=False))
            if msg["type"] == "res":
                break

asyncio.run(chat())
