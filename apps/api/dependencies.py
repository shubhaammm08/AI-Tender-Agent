import uuid
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db

def get_current_tenant(authorization: str = Header(None)) -> uuid.UUID:
    # In a real app, this would decode a JWT to get the tenant_id.
    # For now, we simulate by checking the token or returning a default UUID.
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        try:
            return uuid.UUID(token)
        except ValueError:
            pass
    # fallback test tenant ID
    return uuid.UUID("00000000-0000-0000-0000-000000000001")
