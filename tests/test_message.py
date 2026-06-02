"""Tests for the message schema."""

import json

from jiuwenclaw.schema.message import EventType, Message, Mode, ReqMethod


class TestReqMethod:
    def test_values_are_strings(self):
        assert ReqMethod.CHAT_SEND.value == "chat.send"
        assert ReqMethod.SESSION_LIST.value == "session.list"

    def test_unique_values(self):
        values = [m.value for m in ReqMethod]
        assert len(values) == len(set(values))


class TestEventType:
    def test_values_are_strings(self):
        assert EventType.CHAT_DELTA.value == "chat.delta"
        assert EventType.CONNECTION_ACK.value == "connection.ack"


class TestMode:
    def test_from_raw_with_string(self):
        assert Mode.from_raw("agent_plan") == Mode.AGENT_PLAN
        assert Mode.from_raw("agent_exec") == Mode.AGENT_EXEC

    def test_from_raw_with_unknown_falls_back(self):
        assert Mode.from_raw("unknown") == Mode.AGENT_PLAN

    def test_from_raw_with_none(self):
        assert Mode.from_raw(None) == Mode.AGENT_PLAN


class TestMessageRoundTrip:
    """JSON serialization round-trip for all three message types."""

    def test_req_round_trip(self):
        msg = Message.new_req(
            ReqMethod.CHAT_SEND,
            channel_id="web",
            session_id="sess-001",
            params={"query": "Hello"},
        )
        restored = Message.from_json(msg.to_json())

        assert restored.id == msg.id
        assert restored.type == "req"
        assert restored.req_method == ReqMethod.CHAT_SEND
        assert restored.channel_id == "web"
        assert restored.session_id == "sess-001"
        assert restored.params["query"] == "Hello"

    def test_res_round_trip(self):
        req = Message.new_req(ReqMethod.CHAT_SEND)
        res = Message.new_res(req, ok=True, payload={"answer": "Paris"})

        restored = Message.from_json(res.to_json())

        assert restored.id == req.id
        assert restored.type == "res"
        assert restored.ok is True
        assert restored.payload["answer"] == "Paris"

    def test_event_round_trip(self):
        msg = Message.new_event(
            EventType.CHAT_DELTA,
            channel_id="web",
            payload={"content": "Hello "},
        )
        restored = Message.from_json(msg.to_json())

        assert restored.type == "event"
        assert restored.event_type == EventType.CHAT_DELTA
        assert restored.payload["content"] == "Hello "

    def test_all_req_methods_round_trip(self):
        for method in ReqMethod:
            msg = Message.new_req(method, channel_id="test")
            restored = Message.from_json(msg.to_json())
            assert restored.req_method == method

    def test_all_event_types_round_trip(self):
        for event_type in EventType:
            msg = Message.new_event(event_type)
            restored = Message.from_json(msg.to_json())
            assert restored.event_type == event_type

    def test_error_response(self):
        req = Message.new_req(ReqMethod.CHAT_SEND)
        res = Message.new_res(req, ok=False, error="Something went wrong")

        assert res.ok is False
        assert res.payload["error"] == "Something went wrong"

    def test_from_json_string(self):
        raw = json.dumps({
            "type": "req",
            "id": "abc123",
            "method": "chat.send",
            "params": {"query": "Hi"},
        })
        msg = Message.from_json(raw)
        assert msg.id == "abc123"
        assert msg.req_method == ReqMethod.CHAT_SEND

    def test_metadata_preserved(self):
        msg = Message.new_req(ReqMethod.CHAT_SEND, metadata={"user": "alex"})
        restored = Message.from_json(msg.to_json())
        assert restored.metadata["user"] == "alex"

    def test_default_values(self):
        msg = Message()
        assert msg.type == "req"
        assert msg.mode == Mode.AGENT_PLAN
        assert msg.ok is True
        assert msg.params == {}
