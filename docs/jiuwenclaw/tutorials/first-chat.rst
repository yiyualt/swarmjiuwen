Your First Chat
================

Now that JiuwenClaw has an Agent connected to openjiuwen's LLM, you can
have a real conversation. Here's how the pieces fit together.

How the LLM Gets Called
------------------------

.. code-block:: text

   chat.send ──► WebChannel ──► Agent.chat(query)
                                   │
                                   │  reads config
                                   ▼
                              get_config()
                                   │
                                   │  api_key, api_base, model_name
                                   ▼
                              openjiuwen Model
                                   │
                                   │  HTTP POST /v1/chat/completions
                                   ▼
                              OpenAI API (or compatible)
                                   │
                                   ▼
                              streaming response
                                   │
                                   ▼
                              chat.final event → browser

Step 1: Configure Your API Key
-------------------------------

Create ``~/.jiuwenclaw/config/.env``:

.. code-block:: bash

   API_BASE=https://api.openai.com/v1
   API_KEY=sk-your-real-key-here
   MODEL_NAME=gpt-4o
   MODEL_PROVIDER=openai

Or use any OpenAI-compatible provider (Ollama, vLLM, DeepSeek, etc.):

.. code-block:: bash

   API_BASE=http://localhost:11434/v1
   API_KEY=ollama
   MODEL_NAME=llama3
   MODEL_PROVIDER=openai

The template at ``jiuwenclaw/resources/config.yaml`` references these
variables:

.. code-block:: yaml

   models:
     default:
       model_client_config:
         api_base: ${API_BASE}
         api_key: ${API_KEY}
         model_name: ${MODEL_NAME}
         client_provider: ${MODEL_PROVIDER:-openai}

At startup, ``get_config()`` reads the ``.env`` file and resolves
``${API_KEY}`` to your actual key.

Step 2: Start the WebChannel
-----------------------------

.. code-block:: python

   import asyncio
   from jiuwenclaw.channel.web_channel import WebChannel, WebChannelConfig

   async def main():
       config = WebChannelConfig.from_config()  # reads port from config
       channel = WebChannel(config)
       await channel.start()
       print("Ready at ws://127.0.0.1:19000/ws")
       await asyncio.Event().wait()

   asyncio.run(main())

Step 3: Send a Message
-----------------------

.. code-block:: python

   import asyncio, json
   from websockets.asyncio.client import connect

   async def chat():
       async with connect("ws://127.0.0.1:19000/ws") as ws:
           await ws.recv()  # connection ack

           await ws.send(json.dumps({
               "type": "req",
               "id": "abc",
               "method": "chat.send",
               "params": {"query": "What is Python?"},
           }))

           # chat.final — the complete LLM response
           event = json.loads(await ws.recv())
           print(event["payload"]["content"])

           # res — request acknowledged
           res = json.loads(await ws.recv())
           print("ok:", res["ok"])

   asyncio.run(chat())

If your API key is configured correctly, you'll see a real LLM response.

What the Agent Does Internally
--------------------------------

When ``Agent.chat(query)`` is called:

.. code-block:: python

   # agent.py (simplified)
   from openjiuwen.core.foundation.llm.model import Model
   from openjiuwen.core.foundation.llm.schema.config import ModelClientConfig
   from openjiuwen.core.foundation.llm.schema.message import UserMessage
   from jiuwenclaw.config import get_config

   cfg = get_config()
   mcc = cfg["models"]["default"]["model_client_config"]

   model = Model(
       model_client_config=ModelClientConfig(
           api_key=mcc["api_key"],       # resolved from ${API_KEY}
           api_base=mcc["api_base"],     # resolved from ${API_BASE}
           model_name=mcc["model_name"], # resolved from ${MODEL_NAME}
           client_provider=mcc["client_provider"],
       ),
   )
   messages = [UserMessage(content=query)]
   response = await model.invoke(messages, model=mcc["model_name"])  # ← actual HTTP call
   return response.content

Next Steps
----------

- :doc:`/jiuwenclaw/tutorials/configuring-models` for more provider options.
