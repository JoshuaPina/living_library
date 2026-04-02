# Investigation Learnings

## 2026-03-24

- The first practical blocker for project recovery is environment bootstrap, not application logic.
- Startup error messaging is clear for missing `DATABASE_URL`, but there is no companion quickstart artifact (`.env.example`) to resolve it quickly.
- Frontend asset path consistency should be validated early because one wrong path can make healthy backend features appear broken.
- Prioritized bug logging with consistent metrics helps prevent chasing medium-impact issues before startup blockers.
