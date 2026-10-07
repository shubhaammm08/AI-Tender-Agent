from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector
from database import Base
import uuid

class TenderChunk(Base):
    __tablename__ = "chunks"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tender_id = Column(UUID(as_uuid=True), ForeignKey("tenders.id"), nullable=False)
    file_key = Column(String, nullable=False)
    page = Column(Integer, nullable=True)
    clause = Column(String, nullable=True)
    text = Column(String, nullable=False)
    embedding = Column(Vector(1536)) # Assuming OpenAI embeddings size 1536
