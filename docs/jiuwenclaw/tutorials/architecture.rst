Architecture
============

JiuwenClaw runs as two processes communicating over WebSocket.

The Two Processes
-----------------

.. code-block:: text

   Terminal 1                           Terminal 2
   ┌──────────────────────────┐        ┌──────────────────────────┐
   │  Agent Process           │        │  Gateway Process         │
   │                          │        │                          │
   │  app_agentserver.py      │        │  WebChannel              │
   │    ↓                     │        │  (channel/web_channel.py)│
   │  AgentWebSocketServer    │◄───────│    ↓                     │
   │  (agentserver/           │  WS   │  AgentClient             │
   │   agent_ws_server.py)    │ 18092 │  (gateway/agent_client.py│
   │    ↓                     │        │    ↓                     │
   │  Agent                   │        │  connect() to 18092     │
   │  (agentserver/agent.py)  │        │                          │
   │    ↓                     │        │  Browser connects to     │
   │  LLM (openjiuwen)        │        │  ws://127.0.0.1:19000   │
   └──────────────────────────┘        └──────────────────────────┘

   Agent Process:                     Gateway Process:
   • 启动 WS 服务端 (端口 18092)        • 启动 WS 客户端 → 连 AgentServer
   • 等待 Gateway 连接                  • 启动 WS 服务端 (端口 19000) → 等浏览器连接
   • 收到请求 → Agent.chat() → LLM     • 收到浏览器请求 → AgentClient.chat() → 发给 AgentServer

Agent Process — ``app_agentserver.py``
---------------------------------------

.. code-block:: python

   # app_agentserver.py
   from jiuwenclaw.agentserver.agent_ws_server import AgentWebSocketServer

   server = AgentWebSocketServer(host="127.0.0.1", port=18092)
   await server.start()  # 开始监听，等待 Gateway 连接

``AgentWebSocketServer`` (``agentserver/agent_ws_server.py``) 是一个
**WS 服务端**。它做的事：

1. 监听 18092 端口，接受 Gateway 的 WebSocket 连接
2. 收到 ``chat.send`` → 调 ``Agent.chat(query)``
3. 把结果发回 Gateway

.. code-block:: python

   # agentserver/agent_ws_server.py (简化)
   async def _on_message(self, websocket, raw):
       msg = Message.from_json(raw)                        # JSON → Message
       answer = await self._agent.chat(msg.params["query"]) # 调 Agent
       await websocket.send(chat_final_event)              # 发 chat.final
       await websocket.send(response)                      # 发 res(ok)

Gateway — WebChannel + AgentClient
-----------------------------------

Gateway 有两个 WS 角色：

.. code-block:: text

   浏览器 ──WS──► WebChannel (服务端, 19000) ──► AgentClient (客户端) ──WS──► AgentServer (18092)

**WebChannel** (``channel/web_channel.py``) — WS **服务端**，等浏览器连。

**AgentClient** (``gateway/agent_client.py``) — WS **客户端**，主动连 AgentServer。

.. code-block:: python

   # channel/web_channel.py (简化)
   class WebChannel:
       async def start(self):
           await self._agent.connect()         # AgentClient 连 AgentServer
           self._server = await serve(...)      # 启动 WS 服务端等浏览器

       async def _handle_message(self, websocket, raw):
           msg = Message.from_json(raw)
           answer = await self._agent.chat(     # AgentClient 把请求转发给 AgentServer
               msg.params["query"]
           )
           await websocket.send(chat_final)     # 把 Agent 的回复发给浏览器
           await websocket.send(response)

.. code-block:: python

   # gateway/agent_client.py (简化)
   class AgentClient:
       async def connect(self):
           self._ws = await connect("ws://127.0.0.1:18092")  # 连 AgentServer

       async def chat(self, query):
           await self._ws.send(chat_send_message)            # 发请求
           response = await self._ws.recv()                  # 收回复
           return response

启动
----

两个终端分别启动：

.. code-block:: bash

   # 终端 1: Agent
   python -m jiuwenclaw.app_agentserver

   # 终端 2: Gateway (WebChannel + AgentClient)
   python 02start_webchannel.py

或者一键启动两个子进程：

.. code-block:: bash

   python -m jiuwenclaw.app

文件角色总览
-------------

===================== ========== ======================== ===========
文件                   进程侧     角色                      端口
===================== ========== ======================== ===========
agent_ws_server.py    Agent      WS **服务端**              18092
agent_client.py       Gateway    WS **客户端**              连 18092
web_channel.py        Gateway    WS **服务端**              19000
agent.py              Agent      LLM 调用                   无
message.py            共用       Message 消息格式            无
===================== ========== ======================== ===========
