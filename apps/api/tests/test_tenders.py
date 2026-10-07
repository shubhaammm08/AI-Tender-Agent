import pytest
from fastapi.testclient import TestClient
from main import app
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from packages.adapters.gem import GeMAdapter
from datetime import datetime
from packages.schemas.tender import UniversalTender, TenderStatus

client = TestClient(app)

def test_gem_adapter_discover():
    adapter = GeMAdapter()
    results = adapter.discover(datetime.now())
    assert len(results) > 0
    assert "bid_number" in results[0]

def test_gem_adapter_normalize():
    adapter = GeMAdapter()
    raw = adapter.discover(datetime.now())[0]
    ut = adapter.normalize(raw)
    assert isinstance(ut, UniversalTender)
    assert ut.portal == "GeM"
    assert ut.portal_tender_id == raw["bid_number"]

def test_gem_adapter_status():
    adapter = GeMAdapter()
    raw = adapter.discover(datetime.now())[0]
    ut = adapter.normalize(raw)
    status = adapter.check_status(ut)
    assert isinstance(status, TenderStatus)
    assert status.status == "open"

def test_adapters_health_endpoint():
    response = client.get("/api/v1/tenders/health")
    assert response.status_code == 200
    assert response.json().get("GeM") == "healthy"
