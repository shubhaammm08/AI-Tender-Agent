from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import date, timedelta
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from packages.schemas.document import DocumentResponse, DocumentCreate, DocumentIssue
from models.tenant import Document
from database import get_db
from dependencies import get_current_tenant
from typing import List
import uuid

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.get("", response_model=List[DocumentResponse])
def list_documents(
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(get_current_tenant)
):
    return db.query(Document).filter(Document.tenant_id == tenant_id).all()

@router.post("", response_model=DocumentResponse)
def upload_document(
    doc_in: DocumentCreate,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(get_current_tenant)
):
    doc = Document(tenant_id=tenant_id, **doc_in.model_dump())
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc

@router.delete("/{doc_id}")
def delete_document(
    doc_id: UUID,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(get_current_tenant)
):
    doc = db.query(Document).filter(Document.tenant_id == tenant_id, Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    db.delete(doc)
    db.commit()
    return {"message": "Deleted successfully"}

@router.get("/issues", response_model=List[DocumentIssue])
def check_document_issues(
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(get_current_tenant)
):
    docs = db.query(Document).filter(Document.tenant_id == tenant_id).all()
    issues = []
    
    # Check expiring
    today = date.today()
    thirty_days = today + timedelta(days=30)
    
    doc_types_present = set()
    for doc in docs:
        doc_types_present.add(doc.type)
        if doc.expires_on and doc.expires_on <= thirty_days:
            issues.append(
                DocumentIssue(
                    type=doc.type,
                    issue="expiring",
                    message=f"Document expires on {doc.expires_on}",
                    expires_on=doc.expires_on
                )
            )
            
    # Check missing (Example common mandatory types)
    required_types = {"GST", "PAN", "Udyam"}
    for req in required_types:
        if req not in doc_types_present:
            issues.append(
                DocumentIssue(
                    type=req,
                    issue="missing",
                    message=f"Missing {req} certificate"
                )
            )
            
    return issues
