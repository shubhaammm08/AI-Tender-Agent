from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import uuid
from sqlalchemy.sql import func

class BidDocument(Base):
    __tablename__ = "bid_documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    bid_id = Column(UUID(as_uuid=True), ForeignKey("bids.id"), nullable=False)
    kind = Column(String, nullable=False) # e.g. "technical_proposal", "covering_letter"
    content = Column(String, nullable=True) # Text or markdown content
    status = Column(String, nullable=False, default="draft") # draft, reviewed, approved
    model = Column(String, nullable=True)
    prompt_version = Column(String, nullable=True)
    sources = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=True)
