from jiuwenclaw.schema.message import EventType
from jiuwenclaw.schema.message import Message, ReqMethod

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
print(res)