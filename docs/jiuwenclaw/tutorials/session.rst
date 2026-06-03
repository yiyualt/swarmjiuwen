Session History
===============

JiuwenClaw remembers conversation context within each session. Messages
in the same session are included in the LLM's context, enabling natural
multi-turn dialogue.

How It Works
-------------

Each ``chat.send`` request includes a ``session_id``. Agent stores past
messages per session and injects them into the LLM call:

.. code-block:: text

   Session "sess-1"
   ┌───────────────────────────────────────────┐
   │ User:    "My name is Alex"                │  ← stored
   │ Agent:   "Got it, Alex!"                  │  ← stored
   │                                           │
   │ User:    "What is my name?"               │  ← new query
   │           ↑                               │
   │           past messages injected as context│
   │                                           │
   │ Agent:   "Your name is Alex"              │  ← uses history
   └───────────────────────────────────────────┘

   Session "sess-2"
   ┌───────────────────────────────────────────┐
   │ User:    "What is my name?"               │
   │ Agent:   "I don't know your name yet."    │  ← isolated from sess-1
   └───────────────────────────────────────────┘

Sending Messages with Session IDs
----------------------------------

.. code-block:: python

   await ws.send(json.dumps({
       "type": "req",
       "id": "abc",
       "method": "chat.send",
       "params": {
           "query": "My name is Alex",
           "session_id": "sess-1"        # ← same session = shared context
       },
   }))

   # Later, same session
   await ws.send(json.dumps({
       "type": "req",
       "id": "def",
       "method": "chat.send",
       "params": {
           "query": "What is my name?",
           "session_id": "sess-1"        # ← Agent remembers "Alex"
       },
   }))

Session Lifecycle
------------------

- **Active**: Session receives messages, history grows
- **Idle**: No messages for >1 hour → history evicted from memory
- **Max 50 sessions**: Oldest idle session evicted when limit reached
- **Persistent**: History saved to ``sessions/<session_id>/history.json`` — survives restarts

Next Steps
----------

- :doc:`/jiuwenclaw/tutorials/memory` for long-term (cross-session) memory.
