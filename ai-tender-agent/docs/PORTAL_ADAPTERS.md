# Portal Adapters

Each procurement portal is an independent adapter that outputs the Universal Tender model.

## Interface

```python
class PortalAdapter(Protocol):
    name: str
    parser_version: str

    def discover(self, since: datetime) -> list[RawTender]: ...
    def fetch_documents(self, tender: RawTender) -> list[File]: ...
    def normalize(self, raw: RawTender) -> UniversalTender: ...
    def check_status(self, tender: UniversalTender) -> TenderStatus: ...
    # Later, with human approval:
    # def prefill(self, bid) -> None
    # def assist_submit(self, bid) -> None
```

## Universal Tender model (fields)

`portal`, `portal_tender_id`, `title`, `buyer`, `state`, `category`, `estimated_value`, `emd`, `published_at`, `closes_at`, `bid_opening_at`, `files[]`, `corrigendums[]`, `source_url`, `parser_version`.

## Rollout

| Order | Portal | Notes |
|---|---|---|
| 1 | GeM | Largest MSME audience |
| 2 | CPPP | Central tenders, CAPTCHA likely |
| 3 | One or two state portals | Pick by user demand |

## Rules for building an adapter

1. Prefer official feeds or APIs. Use Playwright only where none exist.
2. Only read public listings in Phase 1. Do not automate logged-in seller accounts without explicit user consent and a legal check.
3. Respect rate limits. Add random delays and a per-portal concurrency cap.
4. Version the parser. When the HTML changes, add `v2` and keep `v1` for old tenders.
5. Save a sample page (no personal data) for each parser version, and test against it.
6. Never log credentials. Store portal logins encrypted per tenant if ever needed.

## Health monitoring

| Check | Action |
|---|---|
| Zero tenders for 24 hours | Alert on-call |
| Parse error rate over 5% | Pause adapter, alert |
| Field missing in over 20% of rows | Mark parser as degraded |

Show users a "data may be delayed" notice when an adapter is degraded.

## DSC and submission

CPPP and most state portals need a hardware DSC token. A cloud browser cannot use it. Final submission, when added, runs through a local agent or browser extension on the user's machine, and only after the user approves.
