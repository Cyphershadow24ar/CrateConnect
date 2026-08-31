# IMPLEMENTATION_PLAN — Milestone 1 Build Sequence

## Goal
Build a stable local MVP for Weeks 1–2 before touching AI, NGO marketplace, or cloud deployment.

## Phase 0 — Inspect and Lock
1. Read all project specification files in the repository.
2. Read the project PDF.
3. Inspect existing code before creating anything.
4. Detect installed versions:
   - Python
   - Node
   - npm/package manager
   - PostgreSQL/psql
5. Do not overwrite existing project work without inspection.
6. Pin exact dependency versions.
7. Create/update `.env.example`.

Deliverable:
`docs/ENVIRONMENT.md`

## Phase 1 — Repository Foundation
Create:
- frontend/
- backend/
- database/
- docs/
- tests where appropriate

Add:
- README
- `.gitignore`
- `.env.example`
- lockfiles
- formatter/linter configs

Goal:
Both frontend and backend can start locally.

## Phase 2 — Database Foundation
1. Verify local PostgreSQL is running.
2. Create/use local database `food_rescue`.
3. Configure DATABASE_URL through environment variables.
4. Set up SQLAlchemy.
5. Set up Alembic.
6. Create initial migration.
7. Create seed script:
   - one demo business
   - initial categories
8. Run migration.
9. Verify tables and relationships.

Goal:
Fresh local DB can be created/rebuilt from migrations.

## Phase 3 — Backend Foundation
1. FastAPI app.
2. CORS for local frontend.
3. API versioning `/api/v1`.
4. Error handling.
5. DB session dependency.
6. Health endpoint.
7. Basic test harness.

Goal:
`/api/v1/health` works and verifies DB connectivity.

## Phase 4 — Category Module
1. Models.
2. Schemas.
3. CRUD service.
4. Routes.
5. Seed data.
6. Tests.

Goal:
Categories are usable by inventory creation/import.

## Phase 5 — Inventory Module
1. Inventory model.
2. Transaction model.
3. CRUD schemas/services/routes.
4. Tenant-scoped access.
5. Search/filter/pagination.
6. Transaction creation.
7. Tests.

Goal:
Create/update/delete inventory works and is auditable.

## Phase 6 — Expiry Tracking
1. Server-date utility.
2. Expiry classification.
3. Expiry alert service.
4. Endpoint.
5. Dashboard summary counts.
6. Tests for boundaries:
   - -1
   - 0
   - 1
   - 2
   - 3
   - 4 days

Goal:
Expiry behavior is deterministic and correct.

## Phase 7 — CSV Import
1. Define schema.
2. Validate upload.
3. Parse with Pandas.
4. Normalize fields.
5. Produce row-level errors.
6. Commit valid import transactionally according to documented policy.
7. Record `ADDED` transactions.
8. Tests.

Goal:
Sample CSV imports into local PostgreSQL.

## Phase 8 — POS REST Adapter
1. Define vendor-neutral sales payload.
2. Implement endpoint.
3. Resolve item by tenant + barcode (or ID).
4. Decrement quantity.
5. Create SOLD transaction.
6. Test insufficient-stock and missing-item errors.

Goal:
Demonstrate REST-based POS ingestion without a real external POS provider.

## Phase 9 — Frontend Foundation
1. React/Vite/TypeScript.
2. Routing.
3. Tailwind.
4. API client.
5. Shared layout/navigation.
6. Design tokens.
7. Reusable components.

Goal:
A consistent responsive shell.

## Phase 10 — Frontend Screens
Implement in order:
1. Dashboard
2. Inventory list
3. Add/Edit inventory modal or page
4. Category manager
5. CSV import
6. Barcode scanner/search
7. Expiry-filtered views

Goal:
Every M1 feature works end-to-end.

## Phase 11 — QA
- Run backend tests.
- Test frontend manually.
- Test CSV with valid and invalid files.
- Test expiry boundaries.
- Test duplicate barcode.
- Test tenant isolation.
- Test POS sale.
- Test refresh persistence.
- Test responsive behavior.
- Test empty/error/loading states.

## Phase 12 — Documentation
Create/update:
- README
- ENVIRONMENT.md
- API.md or OpenAPI notes
- DATABASE.md
- CSV_FORMAT.md
- TROUBLESHOOTING.md

## Definition of Done
M1 is done only when:
- A fresh clone can be run locally.
- Local PostgreSQL is the database.
- No cloud dependency exists.
- Inventory CRUD works.
- CSV upload works.
- Expiry alerts work.
- Categories work.
- Barcode is stored and scan/search flow works.
- Mock POS REST sale works.
- Transactions are persisted.
- Tenant boundaries are enforced.
- Tests pass.
- Documentation is sufficient for another teammate to run the project.

## Build Discipline
- Complete one phase before moving to the next.
- After each phase run tests/lint/type checks where applicable.
- Do not build future modules early.
- Do not introduce a new framework/library unless justified in the docs.
- Do not leave placeholder TODO code for required Milestone 1 behavior.
- Use real working integrations within the local scope, not visual mockups.
