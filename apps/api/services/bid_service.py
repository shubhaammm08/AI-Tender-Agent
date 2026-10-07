import zipfile
import io
from uuid import UUID
from sqlalchemy.orm import Session
from models.tenant import Bid, Document, Match
from fastapi import HTTPException

class BidService:
    def __init__(self, db: Session):
        self.db = db

    def prepare_bid_zip(self, tenant_id: UUID, tender_id: UUID) -> bytes:
        # First check if match exists and is eligible
        match = self.db.query(Match).filter_by(tenant_id=tenant_id, tender_id=tender_id).first()
        if not match or match.decision != "eligible":
            raise HTTPException(status_code=400, detail="Cannot prepare bid for ineligible or unmatched tender.")
            
        # Get all relevant documents for this tenant
        # In a real app, you might filter by requirements. Here we fetch all active ones.
        documents = self.db.query(Document).filter_by(tenant_id=tenant_id).all()
        
        # Create a ZIP file in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for doc in documents:
                # Mock file content fetching - in a real app this pulls from MinIO
                file_content = b"Mock PDF content for " + doc.type.encode()
                filename = f"{doc.type}_{doc.id}.pdf"
                zf.writestr(filename, file_content)
                
            # Add a cover letter or summary
            summary = f"Bid for Tender {tender_id}\nTenant {tenant_id}\nMatch Score: {match.score}"
            zf.writestr("bid_summary.txt", summary.encode())
            
        return zip_buffer.getvalue()

    def create_bid(self, tenant_id: UUID, tender_id: UUID) -> Bid:
        # Prevent auto-submission! State must be 'draft' or 'pending_approval'
        bid = self.db.query(Bid).filter_by(tenant_id=tenant_id, tender_id=tender_id).first()
        if not bid:
            bid = Bid(
                tenant_id=tenant_id,
                tender_id=tender_id,
                status="pending_approval",
                approved_by=None
            )
            self.db.add(bid)
            self.db.commit()
            self.db.refresh(bid)
        return bid

    def approve_bid(self, bid_id: UUID, tenant_id: UUID, approver_name: str) -> Bid:
        bid = self.db.query(Bid).filter_by(id=bid_id, tenant_id=tenant_id).first()
        if not bid:
            raise HTTPException(status_code=404, detail="Bid not found.")
            
        if bid.status != "pending_approval":
            raise HTTPException(status_code=400, detail="Bid is not in pending_approval state.")
            
        bid.status = "approved"
        bid.approved_by = approver_name
        self.db.commit()
        self.db.refresh(bid)
        return bid
