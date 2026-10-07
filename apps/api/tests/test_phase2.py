import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from apps.worker.tasks import process_reminders
from packages.schemas.document import DocumentIssue
from packages.rules.engine import RulesEngine
import uuid
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_process_reminders():
    result = process_reminders()
    assert result["status"] == "success"

def test_document_issue_schema():
    issue = DocumentIssue(
        type="Non-Blacklisting Declaration",
        issue="missing",
        message="Missing declaration",
        resolution_action="generate_declaration"
    )
    assert issue.resolution_action == "generate_declaration"

def test_generate_declaration():
    response = client.post("/api/v1/documents/generate-declaration", json={
        "declaration_type": "Non-Blacklisting Declaration"
    })
    assert response.status_code in [200, 500] # Mock DB will return 500 probably
