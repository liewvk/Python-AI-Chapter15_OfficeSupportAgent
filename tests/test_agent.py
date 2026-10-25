"""Offline tests: no Ollama server is required."""
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from agent import OfficeSupportAgent
from knowledge_base import KnowledgeBase


class MockClient:
    def __init__(self, content="Example output"):
        self.content = content
        self.calls = []

    def chat(self, **kwargs):
        self.calls.append(kwargs)
        return SimpleNamespace(message=SimpleNamespace(content=self.content))


class KnowledgeTests(unittest.TestCase):
    def setUp(self):
        self.entries = [
            {"id": "FAQ-X", "question": "How can I reset my password?",
             "answer": "Select Forgot Password on the portal."},
            {"id": "FAQ-Y", "question": "What is your return policy?",
             "answer": "Returns require proof of purchase."},
        ]
        self.directory = tempfile.TemporaryDirectory()
        self.path = Path(self.directory.name) / "support.json"
        self.path.write_text(json.dumps(self.entries), encoding="utf-8")
        self.kb = KnowledgeBase(self.path)

    def tearDown(self):
        self.directory.cleanup()

    def test_retrieves_password_policy(self):
        self.assertEqual(self.kb.search("How to reset password?")[0]["id"], "FAQ-X")

    def test_no_match_for_unrelated_question(self):
        self.assertEqual(self.kb.search("What is the cafeteria menu?"), [])

    def test_invalid_duplicate_id_rejected(self):
        self.path.write_text(json.dumps(self.entries + [self.entries[0]]), encoding="utf-8")
        with self.assertRaises(ValueError):
            KnowledgeBase(self.path)

    def test_unsupported_question_does_not_contact_model(self):
        client = MockClient()
        answer, ids = OfficeSupportAgent(client).support_answer(
            "What is the cafeteria menu?", self.kb
        )
        self.assertEqual(ids, [])
        self.assertIn("human support officer", answer)
        self.assertEqual(client.calls, [])

    def test_support_answer_passes_approved_context(self):
        client = MockClient("Use the Forgot Password link.")
        answer, ids = OfficeSupportAgent(client).support_answer(
            "reset my password", self.kb
        )
        self.assertIn("Forgot Password", answer)
        self.assertEqual(ids, ["FAQ-X"])
        self.assertIn("FAQ-X", client.calls[0]["messages"][1]["content"])


class AgentTests(unittest.TestCase):
    def test_email_is_draft_only(self):
        client = MockClient("Subject: Meeting\nDear Team,")
        output = OfficeSupportAgent(client).draft_email("Team", "Discuss Friday meeting")
        self.assertIn("Subject", output)
        self.assertIn("never claim to send", client.calls[0]["messages"][0]["content"])

    def test_note_summary(self):
        client = MockClient("- Review sales report")
        output = OfficeSupportAgent(client).summarize_note("Review sales report.")
        self.assertIn("Review", output)

    def test_valid_ticket_json(self):
        client = MockClient('{"category":"Technical","priority":"High","reason":"Portal outage"}')
        result = OfficeSupportAgent(client).classify_ticket("Portal offline")
        self.assertEqual(result["category"], "Technical")
        self.assertEqual(client.calls[0]["format"], "json")

    def test_invalid_ticket_rejected(self):
        client = MockClient('{"category":"Delete All","priority":"High","reason":"Bad"}')
        with self.assertRaises(ValueError):
            OfficeSupportAgent(client).classify_ticket("Test ticket")

    def test_too_long_input_rejected_before_model_call(self):
        client = MockClient()
        with self.assertRaises(ValueError):
            OfficeSupportAgent(client).summarize_note("x" * 2600)
        self.assertEqual(client.calls, [])


if __name__ == "__main__":
    unittest.main()
