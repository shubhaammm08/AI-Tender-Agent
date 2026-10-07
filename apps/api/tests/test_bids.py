import pytest
import uuid
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))
from apps.api.services.bid_service import BidService
from models.tenant import Bid, Match
from fastapi import HTTPException

class MockQuery:
    def __init__(self, result=None):
        self.result = result
        
    def filter_by(self, **kwargs):
        return self
        
    def first(self):
        return self.result

    def all(self):
        return [self.result] if self.result else []

class MockSession:
    def __init__(self, query_result=None):
        self.query_result = query_result
        self.added = []
        
    def query(self, model):
        return MockQuery(self.query_result)
        
    def add(self, obj):
        self.added.append(obj)
        
    def commit(self):
        pass
        
    def refresh(self, obj):
        pass

def test_prepare_bid_zip_ineligible():
    db = MockSession(query_result=Match(decision="ineligible", score=0))
    service = BidService(db)
    with pytest.raises(HTTPException):
        service.prepare_bid_zip(uuid.uuid4(), uuid.uuid4())

def test_create_bid():
    db = MockSession(query_result=None)
    service = BidService(db)
    bid = service.create_bid(uuid.uuid4(), uuid.uuid4())
    assert bid.status == "pending_approval"

def test_approve_bid():
    mock_bid = Bid(id=uuid.uuid4(), status="pending_approval")
    db = MockSession(query_result=mock_bid)
    service = BidService(db)
    approved = service.approve_bid(mock_bid.id, uuid.uuid4(), "Admin")
    assert approved.status == "approved"
    assert approved.approved_by == "Admin"
