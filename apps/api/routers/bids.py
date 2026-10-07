from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from uuid import UUID
from pydantic import BaseModel
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from database import get_db
from dependencies import get_current_tenant
from apps.api.services.bid_service import BidService

router = APIRouter(prefix="/bids", tags=["Bids"])

class BidResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    tender_id: UUID
    status: str
    approved_by: str = None
    
    class Config:
        from_attributes = True

@router.post("/{tender_id}", response_model=BidResponse)
def prepare_bid(
    tender_id: UUID,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(get_current_tenant)
):
    service = BidService(db)
    # This prepares the row in pending_approval
    bid = service.create_bid(tenant_id, tender_id)
    return bid

@router.get("/{tender_id}/download")
def download_bid_zip(
    tender_id: UUID,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(get_current_tenant)
):
    service = BidService(db)
    zip_bytes = service.prepare_bid_zip(tenant_id, tender_id)
    
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename=bid_{tender_id}.zip"}
    )

class ApprovalRequest(BaseModel):
    approver_name: str

@router.put("/{bid_id}/approve", response_model=BidResponse)
def approve_bid(
    bid_id: UUID,
    req: ApprovalRequest,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(get_current_tenant)
):
    service = BidService(db)
    bid = service.approve_bid(bid_id, tenant_id, req.approver_name)
    return bid
