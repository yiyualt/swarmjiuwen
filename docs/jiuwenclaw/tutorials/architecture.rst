Architecture
============

JiuwenClaw uses a split-process architecture: AgentServer handles LLM
processing while Gateway handles channel communication.

.. code-block:: text

   Browser                    Gateway                    AgentServer
      │                          │                          │
      │── WebSocket ────────────►│                          │
      │   ws://127.0.0.1:19000   │                          │
      │                          │── WebSocket ────────────►│
      │                          │   ws://127.0.0.1:18092   │
      │                          │                          │
      │                          │   chat.send("Hello")     │
      │                          │─────────────────────────►│
      │                          │                          │── Agent.chat()
      │                          │                          │── LLM call
      │                          │◄── chat.final ───────────│
      │◄── chat.final ──────────│                          │
      │◄── res(ok) ────────────│                          │

AgentServer (Port 18092)
-------------------------

The AgentServer wraps the Agent runtime in a WebSocket server. It accepts
connections from the Gateway, processes chat requests, and returns
responses.

Start it standalone:

.. code-block:: bash

   python -m jiuwenclaw.app_agentserver

Or with environment variables:

.. code-block:: bash

   AGENT_SERVER_PORT=9090 python -m jiuwenclaw.app_agentserver

Gateway (Port 19000)
---------------------

The Gateway runs the WebChannel (browser WebSocket server) and connects
to AgentServer via ``AgentClient``. It translates browser messages to
AgentServer requests.

Start both together:

.. code-block:: bash

   python -m jiuwenclaw.app

Why Split?
----------

1. **Independent scaling** — AgentServer (LLM-heavy) and Gateway
   (IO-heavy) can run on different machines.
2. **Independent restarts** — Restart Gateway for channel config changes
   without killing active agent sessions.
3. **Clear boundaries** — Each process has one responsibility.

Message Flow
-------------

Every interaction uses the Message schema:

.. code-block:: json

   // Browser → Gateway
   {"type": "req", "method": "chat.send", "params": {"query": "Hello"}}

   // Gateway → AgentServer (same format, forwarded)
   {"type": "req", "method": "chat.send", "params": {"query": "Hello"}}

   // AgentServer → Gateway (streaming event)
   {"type": "event", "event": "chat.final", "payload": {"content": "..."}}

   // AgentServer → Gateway (acknowledgment)
   {"type": "res", "id": "...", "ok": true}

Next Steps
----------

- :doc:`/jiuwenclaw/tutorials/first-chat` to send messages.
