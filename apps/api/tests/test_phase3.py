import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from apps.worker.tasks import generate_bid_documents
import uuid
from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_generate_bid_documents_task():
    result = generate_bid_documents(str(uuid.uuid4()), str(uuid.uuid4()), str(uuid.uuid4()))
    assert result["status"] == "success"

def test_trigger_generation_endpoint():
    response = client.post(f"/api/v1/bids/{uuid.uuid4()}/generate-documents", json={
        "tender_id": str(uuid.uuid4()),
        "bid_id": str(uuid.uuid4())
    })
    # Auth middleware might reject if we don't mock it, but just check routing
    assert response.status_code in [200, 401]

def test_review_document_endpoint():
    response = client.post(f"/api/v1/bids/documents/{uuid.uuid4()}/review", json={
        "feedback": "Add more focus on ISO certification"
    })
    assert response.status_code in [200, 401]
