from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class File(BaseModel):
    name: str
    url: str
    size: Optional[int] = None

class Corrigendum(BaseModel):
    published_at: datetime
    summary: str
    diff: str

class UniversalTender(BaseModel):
    portal: str
    portal_tender_id: str
    title: str
    buyer: Optional[str] = None
    state: Optional[str] = None
    category: Optional[str] = None
    estimated_value: Optional[float] = None
    emd: Optional[float] = None
    published_at: datetime
    closes_at: datetime
    bid_opening_at: Optional[datetime] = None
    files: List[File] = []
    corrigendums: List[Corrigendum] = []
    source_url: str
    parser_version: str

class TenderStatus(BaseModel):
    status: str # open, closed, cancelled
