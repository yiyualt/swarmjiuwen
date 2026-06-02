Persistent Memory
=================

JiuwenClaw remembers facts across conversations using file-based memory.
Everything is stored as Markdown files under the workspace memory directory.

How Memory Works
----------------

.. code-block:: text

   ~/.jiuwenclaw/agent/jiuwenclaw_workspace/memory/
   ├── MEMORY.md           # Long-term memory (loaded every session)
   ├── USER.md             # User profile (learned over time)
   └── daily_memory/       # Daily memory files (YYYY-MM-DD.md)

On startup, Agent loads all memory files and injects them into the system
prompt. The LLM sees past facts and user preferences automatically.

The Agent also has two memory tools:

- ``remember`` — save a fact to memory
- ``recall`` — search memory for a query

Using Memory in Chat
--------------------

.. code-block:: text

   You:     My name is Alex and I prefer Python over JavaScript.

   Agent:   Got it, Alex. I'll remember that you prefer Python.

            [Agent calls remember(content="User's name is Alex.
            Prefers Python over JavaScript.")]

   You:     What language should I use for this new API?

   Agent:   Since you prefer Python, I'd recommend FastAPI...

The agent recalled Alex's Python preference from memory without being
told again.

Edit Memory Files Directly
---------------------------

You can edit memory files with any text editor:

.. code-block:: bash

   # Add a fact about yourself
   echo "- Works at Acme Corp" >> \
     ~/.jiuwenclaw/agent/jiuwenclaw_workspace/memory/USER.md

   # Add a permanent memory
   echo "Project deployment uses Docker on port 8080" >> \
     ~/.jiuwenclaw/agent/jiuwenclaw_workspace/memory/MEMORY.md

Changes take effect on the next message — no restart needed.

What Gets Remembered
---------------------

``USER.md``
   Facts about you: name, preferences, projects, tools you use.
   Built up automatically as you chat.

``MEMORY.md``
   Long-term knowledge: project details, decisions, important context.
   Edit this manually for persistent facts.

``daily_memory/YYYY-MM-DD.md``
   Daily conversation highlights. Created automatically when the agent
   calls ``remember``.

Next Steps
----------

- :doc:`/jiuwenclaw/tutorials/first-chat` to see memory in action.
