import asyncio
from jiuwenclaw.channel.web_channel import WebChannel, WebChannelConfig

async def main():
    config = WebChannelConfig(host="127.0.0.1", port=19000)
    channel = WebChannel(config)
    await channel.start()
    print("Ready at ws://127.0.0.1:19000/ws")
    await asyncio.Event().wait()

asyncio.run(main())