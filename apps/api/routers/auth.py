from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from uuid import UUID
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from database import get_db
from dependencies import get_current_tenant
from models.tenant import UserTenantAccess

router = APIRouter(prefix="/auth", tags=["Auth"])

class SwitchClientRequest(BaseModel):
    target_tenant_id: UUID
    user_id: UUID # In reality extracted from current JWT

@router.post("/switch-client")
def switch_client(
    req: SwitchClientRequest,
    db: Session = Depends(get_db)
):
    # Verify consultant has access to this target client (tenant)
    access = db.query(UserTenantAccess).filter_by(
        user_id=req.user_id, 
        tenant_id=req.target_tenant_id
    ).first()
    
    if not access:
        raise HTTPException(status_code=403, detail="Not authorized to access this client workspace.")
        
    # Return a new mock JWT token bounded to target_tenant_id
    return {
        "access_token": f"mock_jwt_for_tenant_{req.target_tenant_id}",
        "token_type": "bearer",
        "tenant_id": req.target_tenant_id
    }
