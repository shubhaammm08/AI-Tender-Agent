# Security and Compliance

## Tenant isolation

- `tenant_id` on every tenant-owned table, set from the auth token.
- PostgreSQL Row-Level Security as a second layer.
- Object storage keys are prefixed `tenant/{id}/`.
- Automated tests try to read another tenant's data and must fail.

## Data protection

| Area | Practice |
|---|---|
| In transit | TLS everywhere |
| At rest | Encrypted database and storage, per-tenant keys for the vault |
| Secrets | Environment variables or a secret manager, never in code |
| Logs | Never log document contents, GSTIN, PAN or tokens |
| Backups | Encrypted, daily, tested restore each quarter |

## DSC (digital signature)

Never store, upload or process DSC private keys or PINs. Signing happens only on the user's machine.

## Audit trail

- Append-only `audit_log`. The app database role has no UPDATE or DELETE.
- Each row stores `prev_hash` and `hash` (SHA-256 of the row plus the previous hash). A nightly job verifies the chain.
- Log: who, what, when, model, prompt version, source chunks, before and after.

## DPDP Act 2023

| Requirement | How we meet it |
|---|---|
| Consent | Clear consent at signup for processing company and personal data |
| Purpose limit | Use data only for tender work |
| Retention | Delete or anonymize on request and after plan end, with a stated period |
| User rights | Export and delete endpoints |
| Data location | Host in AWS Mumbai or Azure Central India |
| Breach handling | Written incident process |

## AI safety

- Treat tender documents as untrusted input. Ignore instructions found inside them (prompt injection).
- Never let the LLM call tools that write to portals or send messages without a human step.
- Show source citations for every claim in the UI.

## Checklist before launch

- [ ] Tenant isolation tests pass
- [ ] Dependency and container scans clean
- [ ] Rate limits and file size limits set
- [ ] Virus scan on uploaded files
- [ ] Privacy policy and terms published
- [ ] Incident contact documented
