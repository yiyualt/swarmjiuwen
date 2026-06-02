Channel Usage Patterns
======================

Practical examples for working with WebChannel.

Pattern 1: Start and Stop
--------------------------

.. code-block:: python

   import asyncio
   from jiuwenclaw.channel.web_channel import WebChannel, WebChannelConfig

   async def main():
       config = WebChannelConfig(host="127.0.0.1", port=19000)
       channel = WebChannel(config)

       await channel.start()
       try:
           # Server is running — do work here
           await asyncio.sleep(60)
       finally:
           await channel.stop()

   asyncio.run(main())

Pattern 2: Register with ChannelManager
----------------------------------------

.. code-block:: python

   from jiuwenclaw.gateway.channel_manager import ChannelManager

   manager = ChannelManager()

   web = WebChannel(WebChannelConfig(port=19000))
   manager.register_channel(web)
   await web.start()

   # Later, check registered channels
   print(manager.list_channels())  # ['web']

   # Deliver a message to all web clients
   from jiuwenclaw.schema.message import Message, EventType
   msg = Message.new_event(
       EventType.CHAT_FINAL,
       payload={"content": "Hello everyone!"},
   )
   await manager.send_to_channel("web", msg)

   await web.stop()
   manager.unregister_channel("web")

Pattern 3: Wire Format Reference
---------------------------------

Request (client → server):

.. code-block:: json

   {
     "type": "req",
     "id": "req-abc123",
     "method": "chat.send",
     "channel_id": "web",
     "session_id": "sess-xyz",
     "params": {"query": "What is the capital of France?"}
   }

Response (server → client):

.. code-block:: json

   {
     "type": "res",
     "id": "req-abc123",
     "ok": true,
     "payload": {"echo": "What is the capital of France?"}
   }

Event (server → client):

.. code-block:: json

   {
     "type": "event",
     "event": "connection.ack",
     "payload": {"protocol_version": "1.0", "transport": "web"}
   }
