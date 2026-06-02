Using the Web Channel
======================

The WebChannel lets browsers talk to JiuwenClaw over WebSocket. This
tutorial shows how to start the channel and test it.

Start the WebChannel
--------------------

.. code-block:: python

   import asyncio
   from jiuwenclaw.channel.web_channel import WebChannel, WebChannelConfig

   async def main():
       config = WebChannelConfig(host="127.0.0.1", port=19000, path="/ws")
       channel = WebChannel(config)
       await channel.start()
       print("WebChannel running on ws://127.0.0.1:19000/ws")
       # Keep running until Ctrl+C
       await asyncio.Event().wait()

   asyncio.run(main())

Connect from Browser
--------------------

Open ``http://127.0.0.1:19000`` (or any page) and use the browser console:

.. code-block:: javascript

   const ws = new WebSocket("ws://127.0.0.1:19000/ws");

   ws.onmessage = (e) => console.log("Received:", JSON.parse(e.data));

   ws.onopen = () => {
       ws.send(JSON.stringify({
           type: "req",
           id: "abc123",
           method: "chat.send",
           params: { query: "Hello, world!" }
       }));
   };

   // Received: {"type":"event","event":"connection.ack",...}
   // Received: {"type":"res","id":"abc123","ok":true,"payload":{"echo":"Hello, world!"}}

Connect from Python
-------------------

.. code-block:: python

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

What's Happening
----------------

.. code-block:: text

   Client                    WebChannel
      │                          │
      │── {"type":"req", ...} ──►│  JSON → Message
      │                          │
      │◄─ {"type":"event",       │  Connection ack
      │    "event":"connection.ack"} ──│
      │                          │
      │◄─ {"type":"res",         │  Echo (no agent yet)
      │    "payload":{"echo":"Hello!"}} ──│

Next Steps
----------

- See :doc:`/jiuwenclaw/examples/channel-example` for more patterns.
