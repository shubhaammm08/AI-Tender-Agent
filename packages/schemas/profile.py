from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from uuid import UUID

class CompanyProfileBase(BaseModel):
    gstin: Optional[str] = None
    pan: Optional[str] = None
    udyam_no: Optional[str] = None
    turnover: Optional[float] = None
    categories: Optional[List[str]] = []
    states: Optional[List[str]] = []

class CompanyProfileCreate(CompanyProfileBase):
    pass

class CompanyProfileUpdate(CompanyProfileBase):
    pass

class CompanyProfileResponse(CompanyProfileBase):
    id: UUID
    tenant_id: UUID

    class Config:
        from_attributes = True
