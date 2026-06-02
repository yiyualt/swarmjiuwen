Configuring JiuwenClaw
======================

The Config system lets you change settings without editing source code.
A full template ships with the package; you only write what you want to
change.

How It Works
------------

.. code-block:: text

   Package template                          Your override
   ┌──────────────────────┐                 ┌─────────────┐
   │ channels:            │      merge      │ channels:   │
   │   web:               │  ─────────────► │   web:      │
   │     port: 19000      │                 │     port: 3000
   │     host: 127.0.0.1  │                 └─────────────┘
   │ models:              │
   │   default:           │       ┌──────────────────────┐
   │     temperature: 0.95│       │ channels:            │
   └──────────────────────┘       │   web:               │
                                  │     port: 3000        │ ← your value
                                  │     host: 127.0.0.1   │ ← template default
                                  │ models:               │
                                  │   default:            │
                                  │     temperature: 0.95 │ ← template default
                                  └──────────────────────┘

Set Your API Key
-----------------

Create ``~/.jiuwenclaw/config/.env`` with your credentials:

.. code-block:: bash

   API_BASE=https://api.openai.com/v1
   API_KEY=sk-your-key-here
   MODEL_NAME=gpt-4o
   MODEL_PROVIDER=openai

Change the Web Port
--------------------

Create ``~/.jiuwenclaw/config/config.yaml``:

.. code-block:: yaml

   channels:
     web:
       port: 3000

Restart JiuwenClaw, and the WebChannel now listens on port 3000.
Everything else stays at template defaults.

Environment Variable Syntax
----------------------------

Any config value can reference environment variables:

.. code-block:: yaml

   api_key: ${API_KEY}              # required — empty if not set
   api_base: ${API_BASE:-https://api.openai.com/v1}  # with default

Read Config in Code
--------------------

.. code-block:: python

   from jiuwenclaw.config import get_config

   config = get_config()
   port = config["channels"]["web"]["port"]
   print(f"Web port: {port}")

Next Steps
----------

- Return to :doc:`/jiuwenclaw/tutorials/web-channel` to see the config in action.
