from sqlalchemy.orm import Session
from datetime import datetime
from packages.schemas.tender import UniversalTender
from models.tenant import Tender, TenderVersion
import json

def ingest_tender(db: Session, ut: UniversalTender):
    # Check if tender already exists
    existing_tender = db.query(Tender).filter(
        Tender.portal == ut.portal,
        Tender.portal_tender_id == ut.portal_tender_id
    ).first()

    if not existing_tender:
        # Create new tender
        new_tender = Tender(
            portal=ut.portal,
            portal_tender_id=ut.portal_tender_id,
            title=ut.title,
            buyer=ut.buyer,
            state=ut.state,
            category=ut.category,
            estimated_value=ut.estimated_value,
            emd=ut.emd,
            closes_at=ut.closes_at,
            status="open",
            current_version=1
        )
        db.add(new_tender)
        db.commit()
        db.refresh(new_tender)
        
        # Save initial version
        version = TenderVersion(
            tender_id=new_tender.id,
            version=1,
            diff=None, # no diff for version 1
            fetched_at=datetime.now()
        )
        db.add(version)
        db.commit()
        return new_tender
    else:
        # Checking for corrigendums/changes
        # Simplistic check based on closes_at or title
        # In a real system, we'd hash the UniversalTender fields and compare
        changed = False
        diff_data = {}
        if existing_tender.closes_at.replace(tzinfo=None) != ut.closes_at.replace(tzinfo=None):
            changed = True
            diff_data['closes_at'] = {'old': str(existing_tender.closes_at), 'new': str(ut.closes_at)}
            existing_tender.closes_at = ut.closes_at
        
        if changed:
            existing_tender.current_version += 1
            db.add(existing_tender)
            
            new_version = TenderVersion(
                tender_id=existing_tender.id,
                version=existing_tender.current_version,
                diff=diff_data,
                fetched_at=datetime.now()
            )
            db.add(new_version)
            db.commit()
            return existing_tender
        
        return existing_tender
