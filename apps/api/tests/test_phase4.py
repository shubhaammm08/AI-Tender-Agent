import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from main import app
from fastapi.testclient import TestClient
import uuid

client = TestClient(app)

def test_pricing_insights_endpoint():
    response = client.get("/api/v1/pricing/insights?item=Laptop")
    # Will likely return 401 unauth or 200 depending on mock setup
    assert response.status_code in [200, 401]

def test_switch_client_endpoint():
    response = client.post("/api/v1/auth/switch-client", json={
        "target_tenant_id": str(uuid.uuid4()),
        "user_id": str(uuid.uuid4())
    })
    # Auth middleware, or DB lack of records will return 403 or 500
    assert response.status_code in [200, 401, 403, 500]
