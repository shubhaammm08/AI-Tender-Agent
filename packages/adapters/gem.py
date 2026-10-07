from typing import List, Dict, Any
from datetime import datetime, timedelta
from packages.schemas.tender import UniversalTender, File, TenderStatus
from packages.adapters.base import PortalAdapter

class GeMAdapter(PortalAdapter):
    name: str = "GeM"
    parser_version: str = "v1"

    def discover(self, since: datetime) -> List[Dict[str, Any]]:
        # In a real implementation, this would use Playwright to scrape public GeM listings
        # For M3, returning a mock raw tender
        return [
            {
                "bid_number": "GEM/2026/B/1234567",
                "title": "Supply of IT Equipment",
                "buyer": "Ministry of Defence",
                "state": "Delhi",
                "estimated_value": 2500000.0,
                "published_at": datetime.now() - timedelta(days=1),
                "closes_at": datetime.now() + timedelta(days=15),
                "url": "https://bidplus.gem.gov.in/bidlists"
            }
        ]

    def fetch_documents(self, tender: Dict[str, Any]) -> List[File]:
        # Return mock files
        return [
            File(name="NIT.pdf", url="https://example.com/nit.pdf", size=1024),
            File(name="BOQ.xlsx", url="https://example.com/boq.xlsx", size=512)
        ]

    def normalize(self, raw: Dict[str, Any]) -> UniversalTender:
        return UniversalTender(
            portal=self.name,
            portal_tender_id=raw["bid_number"],
            title=raw["title"],
            buyer=raw["buyer"],
            state=raw["state"],
            estimated_value=raw.get("estimated_value"),
            published_at=raw["published_at"],
            closes_at=raw["closes_at"],
            files=self.fetch_documents(raw),
            source_url=raw["url"],
            parser_version=self.parser_version
        )

    def check_status(self, tender: UniversalTender) -> TenderStatus:
        if datetime.now() > tender.closes_at:
            return TenderStatus(status="closed")
        return TenderStatus(status="open")
