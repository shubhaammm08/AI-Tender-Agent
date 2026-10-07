from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from datetime import datetime
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from packages.adapters.gem import GeMAdapter
from packages.adapters.cppp import CPPPAdapter
from packages.adapters.maharashtra import MaharashtraAdapter

router = APIRouter(prefix="/tenders", tags=["Tenders"])

@router.get("/health")
def check_adapters_health():
    health_status = {}
    adapters = [GeMAdapter(), CPPPAdapter(), MaharashtraAdapter()]
    
    for adapter in adapters:
        try:
            # We attempt a light discovery (e.g. from 1 hour ago) to verify it's working
            # Or just check if the class instantiates and returns a mock successfully.
            # Real implementation would have a specific health check or fast endpoint.
            tenders = adapter.discover(since=datetime.now())
            if isinstance(tenders, list):
                health_status[adapter.name] = "healthy"
            else:
                health_status[adapter.name] = "degraded"
        except Exception as e:
            health_status[adapter.name] = f"error: {str(e)}"
            
    return health_status

from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_tenant
from uuid import UUID
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from packages.rules.engine import RulesEngine

@router.get("/{tender_id}/compliance-matrix")
def get_compliance_matrix(
    tender_id: UUID,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(get_current_tenant)
):
    engine = RulesEngine(db, tenant_id)
    matrix = engine.generate_compliance_matrix(tender_id)
    return {"tender_id": str(tender_id), "matrix": matrix}
