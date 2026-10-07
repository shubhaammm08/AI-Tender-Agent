from packages.adapters.base import PortalAdapter
from packages.schemas.tender import UniversalTender
from typing import List

class MaharashtraAdapter(PortalAdapter):
    @property
    def name(self) -> str:
        return "Maharashtra"

    def fetch_recent_tenders(self, days: int = 7) -> List[UniversalTender]:
        # Mocking Mahatenders scraping
        return []

    def fetch_tender_details(self, portal_tender_id: str) -> UniversalTender:
        raise NotImplementedError()

    def check_health(self) -> bool:
        # Mock health check for mahatenders.gov.in
        return True
