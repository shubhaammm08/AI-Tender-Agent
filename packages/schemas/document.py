from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from uuid import UUID

class DocumentBase(BaseModel):
    type: str
    file_key: str
    issued_on: Optional[date] = None
    expires_on: Optional[date] = None

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: UUID
    tenant_id: UUID
    version: int

    class Config:
        from_attributes = True

class DocumentIssue(BaseModel):
    type: str
    issue: str # "missing" or "expiring"
    message: str
    expires_on: Optional[date] = None
    resolution_action: Optional[str] = None # e.g. "generate_declaration", "upload"
