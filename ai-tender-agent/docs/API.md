# API

Base path `/api/v1`. JSON only. Auth with a bearer token. The tenant comes from the token, never from the request body.

## Conventions

- Errors: `{ "error": { "code": "...", "message": "..." } }`
- Pagination: `?page=1&page_size=20`
- Long jobs return `202` with a `job_id`. Poll `GET /jobs/{id}`.
- Every write that involves AI creates an audit entry.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| POST | /auth/login | Sign in |
| GET | /me | Current user and tenant |
| GET / PUT | /profile | Company profile |
| POST | /profile/prefill | Prefill from GSTIN or Udyam number |
| GET | /documents | List vault documents |
| POST | /documents | Upload a document |
| DELETE | /documents/{id} | Remove a document |
| GET | /documents/issues | Missing and expiring documents |
| GET | /tenders | List tenders (`?match=true&decision=bid&state=MH`) |
| GET | /tenders/{id} | Tender detail and versions |
| GET | /tenders/{id}/requirements | Cited requirement list |
| GET | /tenders/{id}/analysis | Score, decision, reasons, gaps |
| POST | /tenders/{id}/analyze | Re-run analysis (202) |
| POST | /bids | Start a bid from a tender |
| POST | /bids/{id}/generate | Generate documents (202) |
| GET | /bids/{id}/verify | Inconsistency report |
| POST | /bids/{id}/approve | Human approval |
| GET | /bids/{id}/audit | Audit trail |
| GET | /reminders | Deadlines and alerts |
| POST | /webhooks/whatsapp | WhatsApp replies |
| GET | /jobs/{id} | Job status |

## Example: analysis response

```json
{
  "tender_id": "c1a...",
  "score": 92,
  "decision": "bid",
  "reasons": ["Turnover meets MSME-relaxed limit", "3 similar orders found"],
  "requirements": [
    {
      "type": "certification",
      "label": "ISO 9001",
      "mandatory": true,
      "status": "expired",
      "source": { "file": "NIT.pdf", "page": 6, "clause": "3.7" }
    }
  ]
}
```
