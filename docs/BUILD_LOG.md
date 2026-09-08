# BUILD_LOG — Milestone 1

## Phase 0 — Inspect and Lock
**Status:** ✅ Complete
**Date:** 2026-08-31

- Read all 6 source-of-truth markdown files.
- Project PDF exists but is not programmatically readable; markdown specs treated as complete contract.
- Inspected existing repo: only scaffolding files exist (README, .gitignore, .env.example).
- Detected environment: Python 3.13.3, Node 22.16.0, npm 11.4.1, PostgreSQL 18.6.
- PostgreSQL service running (`postgresql-x64-18`).
- `psql` not on PATH — not blocking.
- Created `docs/ENVIRONMENT.md`.
- Created implementation checklist and got user approval.
- `.env.example` already present and correct.

**Deliverables:**
- `docs/ENVIRONMENT.md` ✅
- Implementation checklist (approved) ✅

---

## Phase 1 — Repository Foundation
**Status:** ✅ Complete
**Date:** 2026-08-31

### Backend
- Created `Backend/pyproject.toml` with pinned dependencies.
- Created Python venv at `Backend/.venv/`.
- Installed all dependencies (fastapi 0.115.12, sqlalchemy 2.0.41, alembic 1.15.2, etc.).
- Created full project structure per `BACKEND_STRUCTURE.md` §2:
  - `app/core/` — config.py (pydantic-settings), errors.py (standard error handler)
  - `app/db/` — session.py (engine + SessionLocal), base.py (DeclarativeBase), seed.py
  - `app/models/` — business.py, category.py, inventory.py, inventory_transaction.py
  - `app/schemas/`, `app/services/`, `app/repositories/`, `app/utils/` — package stubs
  - `app/api/deps.py` — DB session + tenant context dependencies
  - `app/api/routes/health.py` — health check endpoint
  - `app/main.py` — FastAPI application factory
- Initialized Alembic with `alembic/env.py` configured to use app settings + model metadata.
- Created `tests/conftest.py` with transactional test fixtures.
- Verified: `from app.main import app` imports successfully.
- Ruff linting: All checks passed.

### Frontend
- Scaffolded with `create-vite@9.2.0` (react-ts template).
- Vite 8.2.2, React 19.2.8, TypeScript 6.0.2.
- Installed project dependencies (all pinned):
  - tailwindcss 4.3.3 + @tailwindcss/vite 4.3.3
  - react-router-dom 7.18.3
  - react-hook-form 7.87.0 + @hookform/resolvers 5.9.1 + zod 4.5.4
  - axios 1.20.0
  - @zxing/browser 0.2.1
- Configured `vite.config.ts` with Tailwind plugin and `/api` proxy to backend.
- Created `src/index.css` with Tailwind v4 `@theme` design tokens (primary green, neutral slate, semantic colors, radius, font).
- Verified: `npm run build` succeeds.

### Actual Pinned Versions

| Backend Package    | Version |
|--------------------|---------|
| fastapi            | 0.115.12|
| uvicorn            | 0.34.3  |
| sqlalchemy         | 2.0.41  |
| alembic            | 1.15.2  |
| psycopg[binary]    | 3.2.9   |
| pydantic           | 2.11.4  |
| pydantic-settings  | 2.9.1   |
| pandas             | 2.2.3   |
| python-multipart   | 0.0.20  |
| pytest             | 8.3.5   |
| httpx              | 0.28.1  |
| ruff               | 0.11.13 |

| Frontend Package     | Version |
|----------------------|---------|
| react                | 19.2.8  |
| vite                 | 8.2.2   |
| typescript           | 6.0.2   |
| tailwindcss          | 4.3.3   |
| react-router-dom     | 7.18.3  |
| react-hook-form      | 7.87.0  |
| @hookform/resolvers  | 5.9.1   |
| zod                  | 4.5.4   |
| axios                | 1.20.0  |
| @zxing/browser       | 0.2.1   |


## Phase 2 — Database Foundation

Status: Complete

Completed:
- PostgreSQL connected
- Alembic migration applied
- businesses table created
- categories table created
- inventory_items table created
- inventory_transactions table created
- Demo business seeded
- Default food categories seeded
- Database verified

## Phase 3 — Inventory CRUD + Search & Filter APIs

**Status:** ✅ Complete

**Date:** 2026-09-01

### Backend

Implemented the complete Inventory module following the existing layered architecture (Route → Service → Repository → Model).

#### Created files

* `app/models/inventory.py`
* `app/schemas/inventory.py`
* `app/repositories/inventory_repository.py`
* `app/services/inventory_service.py`
* `app/api/routes/inventory.py`

#### Implemented APIs

* `POST /api/v1/inventory`
* `GET /api/v1/inventory`
* `GET /api/v1/inventory/{inventory_id}`
* `PUT /api/v1/inventory/{inventory_id}`
* `DELETE /api/v1/inventory/{inventory_id}`

#### Added Features

* Product name search
* Category filtering
* Business filtering
* Expiry-date filtering
* Combined query filters

#### Database Validation

Verified:

* UUID validation
* Foreign key constraints
* Unique barcode per business
* Quantity validation

#### API Testing

Manually tested all endpoints through Swagger UI.

Verified:

* 200 OK
* 201 Created
* 204 No Content
* 404 Not Found
* 422 Validation Error
* Search functionality
* Filter combinations
* Duplicate barcode constraint

#### Version Control

* Committed Inventory module.
* Pushed changes to GitHub.
* Created release tag `v0.1.0`.


### Frontend

Current status:

* React + Vite + TypeScript project scaffold completed.
* Tailwind CSS configuration in place.
* Entry structure (`main.tsx`, `App.tsx`, `index.css`) verified.
* Frontend feature implementation is deferred to later milestones after backend completion.

## Phase 4 — Inventory Transaction Audit Trail

Status: ✅ Complete

Date: 2026-09-02

### Backend

- Created `InventoryTransaction` schema with validation.
- Created `TransactionRepository` for immutable transaction storage.
- Created `TransactionService` with inventory adjustment logic.
- Added transaction API routes:
  - `GET /api/v1/transactions`
  - `POST /api/v1/transactions`
  - `GET /api/v1/transactions/inventory/{inventory_id}`
- Implemented automatic inventory updates for:
  - SOLD
  - DONATED
  - EXPIRED
- Added insufficient-stock validation.
- Verified complete audit trail functionality.

### Testing

Verified through Swagger UI:

- SOLD reduced Fresh Milk (25.500 → 20.500).
- DONATED reduced Bread (15 → 12).
- EXPIRED reduced Fresh Spinach (12 → 10).
- Negative-stock attempt returned `400 Bad Request`.
- Inventory history correctly records transactions.
Swagger testing completed successfully.

---

## Phase 5 — Expiry Tracking Engine

**Status:** ✅ Complete
**Date:** 2026-09-02

### Backend
- Added `get_expiring(threshold_days)` repository method.
- Added `get_expired()` repository method.
- Added service logic for `days_remaining` calculation and `EXPIRING_SOON` / `EXPIRED` status derivation.
- Added endpoints:
  - `GET /api/v1/inventory/expiring` (with customizable threshold query parameter)
  - `GET /api/v1/inventory/expired`

### Testing
- Threshold-based expiry detection verified.
- Already-expired endpoint returns correct results.
- Search, category, business, expiry-date and combined filters verified.

---

## Phase 6 — CSV Inventory Upload

**Status:** ✅ Complete
**Date:** 2026-09-02

### Backend
- Implemented `upload_csv` in `InventoryService` using pandas.
- Implemented `POST /api/v1/inventory/upload-csv` endpoint.
- Validates file type (`.csv`) and required columns.
- Implemented `bulk_create` in `InventoryRepository` with duplicate handling (IntegrityError rollback per row).
- Returns import summary with total rows, imported count, and skipped count.

---

## Phase 7 — Barcode/QR Rapid Stock Updates

**Status:** ✅ Complete
**Date:** 2026-09-02

### Backend
- Added `get_by_barcode(barcode, business_id)` to `InventoryRepository` for tenant-scoped barcode lookup with fallback.
- Added `get_by_barcode(barcode, business_id)` to `InventoryService` (returns 404 with clear message if not found).
- Added `GET /api/v1/inventory/barcode/{barcode}` route registered before `/{inventory_id}` to prevent path conflicts.
- Reuses existing `POST /api/v1/transactions` endpoint for rapid stock updates (`SOLD`, `ADDED`).
- Created automated unit tests in `Backend/tests/test_barcode.py` testing lookup success, 404 handling, ADDED transaction, SOLD transaction, and insufficient stock validation.

### Frontend
- Created `src/types/inventory.ts` with `InventoryItem`, `TransactionCreate`, and `TransactionResponse` interfaces.
- Created `src/services/api.ts` with configured Axios client (`/api/v1`).
- Created `src/services/inventoryService.ts` with typed `lookupByBarcode`, `createTransaction`, `getInventory`, and `listInventory`.
- Created reusable `src/components/BarcodeScanner.tsx` using `@zxing/browser` (`BrowserMultiFormatReader`):
  - Environment/rear camera preferred with camera switching selector.
  - Animated targeting reticle with laser scan bar.
  - Automatic stream cleanup on unmount and after successful scan.
  - Manual barcode entry fallback for desktop/devices without cameras.
  - Graceful handling of camera permission denial and missing device errors.
- Created `src/pages/ScanPage.tsx`:
  - Instant camera scanner modal trigger.
  - Live item card with product name, current quantity, unit, barcode, and expiry date.
  - Rapid action buttons: "Sell Stock (SOLD)" and "Add Stock (ADDED)".
  - Quantity input with quick increment presets (+1, +5, +10).
  - Validation for non-positive quantities and insufficient stock.
  - Instant state refresh from server after transaction commit.
  - Quick test buttons for all 9 demo barcodes (Fresh Milk, Bread, Fresh Spinach, Frozen Peas, Rice Bag, Orange Juice, Greek Yogurt, Apple Juice, Wheat Flour).
- Updated `src/App.tsx` and `src/App.css` with responsive layout and design tokens.

### Verification
- Backend pytest: 4 passed in 0.18s (`tests/test_barcode.py`).
- Backend ruff: clean on modified repository, service, and routes.
- Frontend oxlint: 0 warnings, 0 errors.
- Frontend build: `tsc -b && vite build` succeeded in 300ms.

Phase 8 — External POS REST API Integration

Status: ✅ Complete

Date: 2026-09-03

Backend

Implemented a REST API for external POS system integration.

New Endpoint

POST /api/v1/pos/sync

Features

Barcode-based product lookup

Automatic inventory reduction

Transaction audit trail creation

Multi-sale batch processing

Unknown barcode handling

Insufficient stock validation

Sync summary response

Testing

Verified through Swagger UI:

Successful POS sync

Inventory updated automatically

Transaction created automatically

Invalid barcode handling

Insufficient stock validation