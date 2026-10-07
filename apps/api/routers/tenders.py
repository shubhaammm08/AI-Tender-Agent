from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from datetime import datetime
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from packages.adapters.gem import GeMAdapter

router = APIRouter(prefix="/tenders", tags=["Tenders"])

@router.get("/health")
def check_adapters_health():
    health_status = {}
    adapters = [GeMAdapter()]
    
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
