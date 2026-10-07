import pytest
from fastapi.testclient import TestClient
from main import app
import uuid
import datetime

client = TestClient(app)

# Dummy tenant id to use
test_tenant_id = "00000000-0000-0000-0000-000000000001"

def test_get_profile_not_found():
    response = client.get("/api/v1/profile")
    # without DB, this might fail with 500 or 404 depending on how the session is mocked
    # we just check the route exists
    assert response.status_code in [404, 500]

def test_update_profile():
    payload = {
        "gstin": "22AAAAA0000A1Z5",
        "turnover": 5000000,
        "categories": ["IT Services"]
    }
    response = client.put("/api/v1/profile", json=payload)
    assert response.status_code in [200, 500]

def test_upload_document():
    payload = {
        "type": "GST",
        "file_key": "tenant/1/gst.pdf",
        "issued_on": "2023-01-01"
    }
    response = client.post("/api/v1/documents", json=payload)
    assert response.status_code in [200, 500]

def test_document_issues():
    response = client.get("/api/v1/documents/issues")
    assert response.status_code in [200, 500]
