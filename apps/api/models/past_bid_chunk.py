from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from database import Base
import uuid

class PastBidChunk(Base):
    __tablename__ = "past_bid_chunks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False)
    bid_id = Column(UUID(as_uuid=True), ForeignKey("bids.id"), nullable=False)
    text = Column(String, nullable=False)
    embedding = Column(Vector(1536), nullable=False)
