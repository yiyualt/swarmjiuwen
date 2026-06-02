from jiuwenclaw.schema.message import Message, ReqMethod

msg = Message.new_req(
    ReqMethod.CHAT_SEND,
    channel_id="web",
    session_id="sess-001",
    params={"query": "What is the capital of France?"},
)

print(msg.to_json())


res = Message.new_res(msg, ok=True, payload={"answer": "Paris"})
print(res.to_json())


from jiuwenclaw.schema.message import EventType

event = Message.new_event(
    EventType.CHAT_DELTA,
    payload={"content": "The capital is "},
)
print(event.to_json())



raw = '{"type": "req", "id": "abc", "method": "chat.send", "params": {"query": "Hi"}}'
msg = Message.from_json(raw)
print(msg.req_method)   # ReqMethod.CHAT_SEND
print(msg.params)       # {"query": "Hi"}