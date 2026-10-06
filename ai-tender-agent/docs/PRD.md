# Product Requirements (PRD)

## Problem

Indian MSMEs lose government business because tender work is slow and error-prone. They miss tenders, read long PDFs by hand, find missing certificates too late, and get disqualified for small mistakes.

## Users

| User | Need |
|---|---|
| MSME owner / GeM seller | Know which tenders to bid on and get a ready bid |
| Bid consultant / CA | Manage many clients in one place (later phase) |
| Company staff | Upload documents, review drafts, approve |

## Goals

1. Show matched tenders with a clear Bid / Check / Skip decision and reasons.
2. Turn tender documents into a cited requirement checklist.
3. Warn about missing or expired documents before the deadline.
4. Prepare bid documents for human review (Phase 3).
5. Keep a full audit trail of every AI action.

## Non-goals (for now)

- Automatic submission of bids
- Handling digital signature tokens on the server
- Guaranteeing eligibility or winning
- Private-sector tenders

## Core user stories

- As a seller, I enter my GSTIN and categories and see matched tenders the same day.
- As a seller, I open a tender and see each requirement with its page and clause, and whether I meet it.
- As a seller, I see which certificate is expired and how many days I have.
- As a seller, I get a WhatsApp alert for a strong match and reply Bid or Skip.
- As an approver, I review every AI-written document and approve before anything leaves the system.
- As a seller, I see corrigendum changes and an updated decision.

## Phase 1 scope

Company profile, GeM discovery, document pipeline, requirement extraction, rule-based scoring, document vault with expiry, dashboard, audit log.

## Pricing (planned)

| Plan | Price | Notes |
|---|---|---|
| Starter | ₹999/month | Discovery, alerts, limited analyses |
| Professional | ₹2,999/month | Vault, more analyses, bid generation |
| Business | ₹7,999+/month | Multi-user, pricing intelligence |
| Pay-per-tender | Per bid package | Occasional bidders |

Cap analyses per plan, because OCR and LLM cost per tender is real.

## Success metrics

| Metric | Target |
|---|---|
| Requirement extraction recall (mandatory items) | 95% or higher |
| Time from tender found to decision | Under 5 minutes |
| Users who upload 3 or more vault documents in week 1 | 60% |
| Paid conversion after free trial | 8% or higher |
| Bids with zero verify-stage errors | Improving every month |

## Risks

| Risk | Mitigation |
|---|---|
| Portals block automation | Public data first, assisted submission later |
| Wrong extraction | Citations, evaluation set, human review |
| Wrong bid causes forfeited EMD | Rule checks, approval step, disclaimers |
| High AI cost | Credits, caching, cheaper models for simple steps |
| Strong search competitors | Win on preparation, verification and outcome data |
