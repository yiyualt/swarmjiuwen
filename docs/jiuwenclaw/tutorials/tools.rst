Using Tools
===========

JiuwenClaw can read files, write files, and run shell commands. Tools
make the agent capable of doing real work, not just chatting.

Available Tools
---------------

=================== =============================================
Tool                Description
=================== =============================================
``read_file``       Read a file in the workspace
``write_file``      Create or overwrite a file
``command``         Run a shell command
``remember``        Save a fact to persistent memory
``recall``          Search memory for facts
=================== =============================================

How Tools Work
--------------

When you send a message, the Agent passes all available tool descriptions
to the LLM. If the LLM decides a tool would help, it returns a tool call.
The Agent executes the tool and feeds the result back to the LLM for a
final answer.

.. code-block:: text

   "What's in config.py?"
       │
       ▼
   LLM: "I should read_file('config.py')"
       │
       ▼
   Agent executes read_file
       │
       ▼
   Tool result: "port = 19000\nhost = 127.0.0.1..."
       │
       ▼
   LLM: "The config file sets port to 19000 and host to 127.0.0.1"

Example: Read a File
---------------------

.. code-block:: text

   You:     Show me the first 10 lines of agent.py

   Agent:   [calls read_file(path="jiuwenclaw/agentserver/agent.py")]
            Here are the first 10 lines:
            """Agent — single-turn chat with memory and tools."""
            ...

Example: Create a File
-----------------------

.. code-block:: text

   You:     Create a file called hello.py that prints "Hello, JiuwenClaw!"

   Agent:   [calls write_file(path="hello.py", content='print("Hello, JiuwenClaw!")')]
            Created hello.py. Run it with: python hello.py

Example: Run a Command
-----------------------

.. code-block:: text

   You:     What files are in the current directory?

   Agent:   [calls command(cmd="ls -la")]
            Here's what's in the directory:
            agent.py, config.py, channel/, gateway/, ...

Safety
------

File tools can only access files inside the workspace directory. Path
traversal (like ``../../../etc/passwd``) is blocked.

Next Steps
----------

- :doc:`/jiuwenclaw/tutorials/memory` to see memory tools in action.
