import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from main import app
from fastapi.testclient import TestClient
import uuid

client = TestClient(app)

def test_get_bid_payload():
    response = client.get(f"/api/v1/bids/{uuid.uuid4()}/payload")
    # Due to auth and missing DB data, expect 401 or similar, 
    # but confirms endpoint is wired correctly.
    assert response.status_code in [200, 401]
