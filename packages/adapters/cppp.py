from packages.adapters.base import PortalAdapter
from packages.schemas.tender import UniversalTender
from typing import List

class CPPPAdapter(PortalAdapter):
    @property
    def name(self) -> str:
        return "CPPP"

    def fetch_recent_tenders(self, days: int = 7) -> List[UniversalTender]:
        # Mocking CPPP XML/HTML scraping
        return []

    def fetch_tender_details(self, portal_tender_id: str) -> UniversalTender:
        raise NotImplementedError()

    def check_health(self) -> bool:
        # Mock health check for eprocure.gov.in
        return True
