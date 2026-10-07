from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from packages.schemas.profile import CompanyProfileResponse, CompanyProfileCreate, CompanyProfileUpdate
from models.tenant import CompanyProfile
from database import get_db
from dependencies import get_current_tenant

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("", response_model=CompanyProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(get_current_tenant)
):
    profile = db.query(CompanyProfile).filter(CompanyProfile.tenant_id == tenant_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("", response_model=CompanyProfileResponse)
def update_profile(
    profile_in: CompanyProfileUpdate,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(get_current_tenant)
):
    profile = db.query(CompanyProfile).filter(CompanyProfile.tenant_id == tenant_id).first()
    if not profile:
        profile = CompanyProfile(tenant_id=tenant_id, **profile_in.model_dump())
        db.add(profile)
    else:
        for key, value in profile_in.model_dump(exclude_unset=True).items():
            setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return profile

@router.post("/prefill")
def prefill_profile(
    source: str, # "gstin" or "udyam"
    value: str,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(get_current_tenant)
):
    # Dummy implementation for prefill
    return {"message": f"Prefilled from {source}: {value}", "data": {"turnover": 5000000}}
