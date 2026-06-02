## 1. Channel Base

- [x] 1.1 Implement `channel/base.py` — `ChannelBase` ABC with `channel_id`, `start()`, `stop()`

## 2. WebChannel

- [x] 2.1 Add `websockets` dependency to `pyproject.toml`
- [x] 2.2 Implement `channel/web_channel.py` — WebSocket server on configurable host:port:path
- [x] 2.3 Implement JSON→Message parsing on incoming WebSocket frames
- [x] 2.4 Implement echo: receive `req` → send back `res` with same content

## 3. ChannelManager

- [x] 3.1 Implement `gateway/channel_manager.py` — register, unregister, send to channel

## 4. Tests

- [x] 4.1 Write `tests/test_web_channel.py` — start server, connect, send, receive echo

## 5. Documentation

- [x] 5.1 Write `docs/jiuwenclaw/tutorials/web-channel.rst` — start WebChannel, connect from browser
- [x] 5.2 Write `docs/jiuwenclaw/examples/channel-example.rst` — echo pattern, JSON wire format
- [x] 5.3 Update `docs/index.rst` — add new docs to toctree
