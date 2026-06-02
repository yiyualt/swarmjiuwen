Message Usage Patterns
======================

Practical examples of creating and working with Messages.

Pattern 1: Build a Chat Request
--------------------------------

.. code-block:: python

   from jiuwenclaw.schema.message import Message, ReqMethod

   msg = Message.new_req(
       ReqMethod.CHAT_SEND,
       channel_id="web",
       session_id="sess-abc",
       params={"query": "Explain quantum computing in one sentence."},
       is_stream=True,
   )

   # Send over WebSocket:
   # await ws.send(msg.to_json())

Pattern 2: Stream a Response
-----------------------------

.. code-block:: python

   from jiuwenclaw.schema.message import EventType

   req = Message.new_req(ReqMethod.CHAT_SEND)

   # Agent streams tokens one at a time
   for token in ["Quantum ", "computing ", "uses ", "qubits..."]:
       event = Message.new_event(
           EventType.CHAT_DELTA,
           channel_id=req.channel_id,
           session_id=req.session_id,
           payload={"content": token},
       )
       # await ws.send(event.to_json())

   # Then send the final event
   final = Message.new_event(
       EventType.CHAT_FINAL,
       session_id=req.session_id,
       payload={"content": "Quantum computing uses qubits..."},
   )

   # Then acknowledge the request
   res = Message.new_res(req, ok=True)

Pattern 3: Handle Errors
-------------------------

.. code-block:: python

   req = Message.new_req(ReqMethod.CHAT_SEND)

   # Something went wrong
   res = Message.new_res(
       req,
       ok=False,
       error="Model API key not configured.",
   )
   # {"id": "...", "type": "res", "ok": false, "payload": {"error": "Model API key not configured."}}

Pattern 4: Session Management
------------------------------

.. code-block:: python

   # List sessions
   list_req = Message.new_req(ReqMethod.SESSION_LIST, channel_id="web")

   # Create a new session
   create_req = Message.new_req(
       ReqMethod.SESSION_CREATE,
       channel_id="web",
   )
