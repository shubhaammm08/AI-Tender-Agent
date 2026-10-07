import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from packages.llm.client import LLMClient
from packages.llm.prompts import EXTRACTION_PROMPT
from packages.rules.engine import RulesEngine
import uuid

# We mock DB sessions for tests
class MockSession:
    def add(self, obj):
        pass
    def commit(self):
        pass
    def query(self, model):
        class MockQuery:
            def filter_by(self, **kwargs):
                return self
            def first(self):
                return None
            def all(self):
                return []
        return MockQuery()
    def refresh(self, obj):
        pass

def test_llm_client_mock():
    db = MockSession()
    client = LLMClient()
    response = client.generate(EXTRACTION_PROMPT, "System Prompt", db, uuid.uuid4())
    assert "extracted" in response

def test_rules_engine():
    db = MockSession()
    engine = RulesEngine(db, uuid.uuid4())
    match = engine.evaluate_eligibility(uuid.uuid4())
    assert match.score >= 0
    assert match.decision in ["eligible", "ineligible"]
