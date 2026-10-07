from models.tenant import CompanyProfile, Requirement, Match, Document
from sqlalchemy.orm import Session
from uuid import UUID

class RulesEngine:
    def __init__(self, db: Session, tenant_id: UUID):
        self.db = db
        self.tenant_id = tenant_id

    def evaluate_eligibility(self, tender_id: UUID) -> Match:
        profile = self.db.query(CompanyProfile).filter_by(tenant_id=self.tenant_id).first()
        documents = self.db.query(Document).filter_by(tenant_id=self.tenant_id).all()
        requirements = self.db.query(Requirement).filter_by(tender_id=tender_id).all()
        
        doc_types = {doc.type for doc in documents}
        
        score = 100
        reasons = []
        is_eligible = True

        for req in requirements:
            if req.type == "turnover":
                req_val = float(req.value.get("amount", 0))
                if not profile or not profile.turnover or profile.turnover < req_val:
                    is_eligible = False
                    score -= 50
                    reasons.append(f"Turnover {profile.turnover if profile else 0} is less than required {req_val}")
            
            elif req.type == "certificate":
                cert_name = req.value.get("name")
                if cert_name not in doc_types:
                    if req.mandatory:
                        is_eligible = False
                        score -= 50
                    else:
                        score -= 10
                    reasons.append(f"Missing certificate: {cert_name}")
            
            # Additional rules...

        decision = "eligible" if is_eligible else "ineligible"
        
        match = Match(
            tenant_id=self.tenant_id,
            tender_id=tender_id,
            score=max(0, score),
            decision=decision,
            reasons=reasons
        )
        self.db.add(match)
        self.db.commit()
        self.db.refresh(match)
        
        return match
