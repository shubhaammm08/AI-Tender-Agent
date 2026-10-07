from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from database import get_db
from dependencies import get_current_tenant
from models.price_history import PriceHistory

router = APIRouter(prefix="/pricing", tags=["Pricing Insights"])

@router.get("/insights")
def get_pricing_insights(
    item: str,
    db: Session = Depends(get_db),
    tenant_id: UUID = Depends(get_current_tenant)
):
    # Retrieve past award prices for this item category
    results = db.query(
        func.avg(PriceHistory.l1_price).label("average_l1_price"),
        func.min(PriceHistory.l1_price).label("min_l1_price"),
        func.max(PriceHistory.l1_price).label("max_l1_price"),
        func.count(PriceHistory.id).label("total_contracts")
    ).filter(PriceHistory.item.ilike(f"%{item}%")).first()
    
    if not results or results.total_contracts == 0:
        return {"item": item, "message": "No pricing history available for this item."}
        
    return {
        "item": item,
        "average_l1_price": float(results.average_l1_price) if results.average_l1_price else 0,
        "min_l1_price": float(results.min_l1_price) if results.min_l1_price else 0,
        "max_l1_price": float(results.max_l1_price) if results.max_l1_price else 0,
        "total_contracts": results.total_contracts,
        "recommendation": "Bid near the average L1 price to stay competitive."
    }
