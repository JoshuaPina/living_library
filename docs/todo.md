# Living Library Investigation TODO

## Active
- [ ] Run API startup with valid environment and capture baseline endpoint results. (Blocked by missing DATABASE_URL in current shell/.env)
- [ ] Verify semantic search path against real embeddings data. (Probe script hardened; waiting on runtime env)
- [ ] Verify document loading path for both `local` and `supabase` providers. (Blocked until API starts)
- [ ] Verify browse/viewer pages in browser and capture frontend runtime errors. (Blocked until API starts)

## Next
- [x] Add rich console summary command for bug scoring.
- [x] Add structured backend logs for startup + PDF/document paths.
- [x] Add targeted frontend console diagnostics around search and topic browsing.

## Later
- [x] Add machine-checkable smoke test script for API endpoints.
- [x] Add runbook with known failure signatures and fixes.
