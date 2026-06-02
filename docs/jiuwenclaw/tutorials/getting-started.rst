Getting Started with Messages
=============================

The Message is the universal envelope that every JiuwenClaw component
uses to communicate. This tutorial shows you how to create, serialize,
and deserialize messages.

Install
-------

.. code-block:: bash

   pip install -e .

Create Your First Message
--------------------------

A **request** is what a client sends to ask the agent to do something:

.. code-block:: python

   from jiuwenclaw.schema.message import Message, ReqMethod

   msg = Message.new_req(
       ReqMethod.CHAT_SEND,
       channel_id="web",
       session_id="sess-001",
       params={"query": "What is the capital of France?"},
   )

   print(msg.to_json())
   # {"id": "a1b2c3d4e5f6", "type": "req", "method": "chat.send", ...}

A **response** is what the agent sends back:

.. code-block:: python

   res = Message.new_res(msg, ok=True, payload={"answer": "Paris"})
   print(res.to_json())
   # {"id": "a1b2c3d4e5f6", "type": "res", "ok": true, "payload": {"answer": "Paris"}}

An **event** is what the agent pushes during processing:

.. code-block:: python

   from jiuwenclaw.schema.message import EventType

   event = Message.new_event(
       EventType.CHAT_DELTA,
       payload={"content": "The capital is "},
   )
   print(event.to_json())
   # {"type": "event", "event": "chat.delta", "payload": {"content": "The capital is "}}

Parse Incoming Messages
------------------------

.. code-block:: python

   raw = '{"type": "req", "id": "abc", "method": "chat.send", "params": {"query": "Hi"}}'
   msg = Message.from_json(raw)
   print(msg.req_method)   # ReqMethod.CHAT_SEND
   print(msg.params)       # {"query": "Hi"}

Next Steps
----------

- See :doc:`/jiuwenclaw/examples/message-example` for practical patterns.
