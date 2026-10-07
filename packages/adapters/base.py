from typing import Protocol, List, Any
from datetime import datetime
from packages.schemas.tender import UniversalTender, File, TenderStatus

class RawTender(Protocol):
    pass

class PortalAdapter(Protocol):
    name: str
    parser_version: str

    def discover(self, since: datetime) -> List[Any]:
        ...

    def fetch_documents(self, tender: Any) -> List[File]:
        ...

    def normalize(self, raw: Any) -> UniversalTender:
        ...

    def check_status(self, tender: UniversalTender) -> TenderStatus:
        ...
