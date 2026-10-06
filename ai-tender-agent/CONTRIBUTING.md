# Contributing

## Branches and commits

- Branch from `main`: `feat/short-name`, `fix/short-name`, `docs/short-name`.
- Commit style: `feat(rules): add MSME turnover relaxation`. Types: feat, fix, docs, test, refactor, chore.
- Keep pull requests small and focused on one change.

## Pull request checklist

- [ ] Tests added or updated, and passing
- [ ] Migration included if the schema changed
- [ ] `tenant_id` filter present on new queries
- [ ] Audit log entry added for any AI action
- [ ] Docs updated
- [ ] No secrets, no document contents in logs

## Local setup

See the Quick start in `README.md`. Use `.env.example` as the template and never commit `.env`.

## Reporting a portal break

Open an issue with the portal name, tender URL, the date, and the adapter health message. Attach a saved HTML sample with no personal data.
