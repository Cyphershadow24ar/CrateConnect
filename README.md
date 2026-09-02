# AI-Powered Food Waste Management Platform for Surplus Identification and Redistribution Optimization

An enterprise-grade food rescue inventory management platform designed to track perishable inventory, prevent waste through automated expiry tracking, ingest bulk records via CSV, and enable rapid stock updates using a mobile-friendly barcode/QR scanner.

**Current Milestone:** Milestone 1 — Core Inventory Foundation, Expiry Tracking & Barcode Operations (Weeks 1–2).

---

## Table of Contents

- [Overview](#overview)
- [Key Features (Milestone 1)](#key-features-milestone-1)
  - [Backend Features](#backend-features)
  - [Frontend Features](#frontend-features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Environment Configuration](#environment-configuration)
  - [Database Setup & Migrations](#database-setup--migrations)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
- [API Endpoints Summary](#api-endpoints-summary)
- [Core Workflows](#core-workflows)
  - [Barcode & QR Scanner Workflow](#barcode--qr-scanner-workflow)
  - [CSV Bulk Ingestion Workflow](#csv-bulk-ingestion-workflow)
  - [Expiry Tracking Workflow](#expiry-tracking-workflow)
- [Testing & Quality Verification](#testing--quality-verification)
- [Version Control & Release Status](#version-control--release-status)
- [Future Roadmap](#future-roadmap)

---

## Overview

Food waste in commercial retail and food rescue initiatives is often driven by lack of real-time inventory visibility and delayed action on perishable goods. This platform provides multi-tenant inventory tracking, real-time expiry monitoring, an audit trail of stock adjustments, and high-speed in-store barcode/QR mobile scanning.

All features documented here represent **Milestone 1 completed deliverables**.

---

## Key Features (Milestone 1)

### Backend Features
- **Multi-Tenant Architecture**: Business-scoped inventory data isolating tenant records (`businesses`, `categories`, `inventory_items`, `inventory_transactions`).
- **Category & Business Management**: Complete CRUD endpoints with constraints on perishability (`HIGH`, `MEDIUM`, `LOW`) and storage conditions (`COLD`, `DRY`, `FROZEN`).
- **Inventory CRUD**: Full item lifecycle management with product attributes, unique business-scoped barcodes, unit quantities, and purchase/expiry dates.
- **Search & Multi-Filter Querying**: Case-insensitive product name search combined with category, business, and expiry-date threshold filtering.
- **Inventory Transaction Audit Trail**: Immutable transaction ledger tracking all stock movements (`ADDED`, `UPDATED`, `SOLD`, `EXPIRED`, `DONATED`) with automated stock adjustment and strict negative-inventory prevention.
- **Expiry Engine**: Automated detection of items approaching expiry (`/expiring` with custom thresholds) and already expired items (`/expired`).
- **CSV Bulk Import**: Upload endpoint validating CSV headers, parsing data via Pandas, handling duplicate barcode conflicts per tenant, and returning structured row-level import summaries.
- **Barcode Lookup API**: Tenant-scoped barcode resolution returning comprehensive item details and current quantity.

### Frontend Features
- **Mobile-Responsive Barcode & QR Scanner**: Integrates `@zxing/browser` camera stream with automatic rear/environment camera selection, animated target reticle, and hardware release on scan completion or unmount.
- **Rapid Stock Adjustment Card**: Verified item display after barcode scan enabling one-click stock updates (`SOLD` / `ADDED`) with quantity presets (+1, +5, +10).
- **Graceful Hardware & Error Handling**: Support for camera permission denials, missing video devices, unknown barcode states (404), and over-sell inventory validations.
- **Manual Input Fallback**: Built-in manual barcode lookup field and demo barcode test triggers ensuring complete testability in environments without active cameras.
- **Design System**: Curated Tailwind CSS design tokens (emerald primary, slate neutrals, semantic status badges).

---

## Tech Stack

| Layer | Technology | Version / Details |
|---|---|---|
| **Backend Framework** | FastAPI | `0.115.12` |
| **ASGI Server** | Uvicorn | `0.34.3` |
| **ORM & Migrations** | SQLAlchemy / Alembic | `2.0.41` / `1.15.2` |
| **Database** | PostgreSQL | `18.6` (Multi-tenant schema) |
| **Data Parsing & Validation** | Pydantic / Pandas | `2.11.4` / `2.2.3` |
| **Database Driver** | psycopg (v3 binary) | `3.2.9` |
| **Frontend Framework** | React + TypeScript + Vite | React `19.2.8`, Vite `8.2.2`, TS `6.0.2` |
| **Styling** | Tailwind CSS | `4.3.3` (`@tailwindcss/vite`) |
| **Barcode / QR Engine** | `@zxing/browser` | `0.2.1` |
| **HTTP Client** | Axios | `1.20.0` |
| **Linting & Testing** | Ruff, Oxlint, Pytest | Ruff `0.11.13`, Pytest `8.3.5` |

---

## Project Structure

```
FoodWMDapp/
├── Backend/
│   ├── alembic/                 # Migration environment and version scripts
│   │   ├── versions/            # 809e0fd791ae_initial_schema.py
│   │   └── env.py
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py          # Database session and tenant context dependencies
│   │   │   └── routes/          # Health, business, category, inventory, transactions
│   │   ├── core/                # Application config (pydantic-settings) & error handling
│   │   ├── db/                  # Session factory, declarative base, seed script
│   │   ├── models/              # SQLAlchemy ORM models (Business, Category, Inventory, etc.)
│   │   ├── repositories/        # Database access layer (CRUD, bulk create, barcode lookup)
│   │   ├── schemas/             # Pydantic request/response validation schemas
│   │   ├── services/            # Business logic (stock adjustments, CSV import, expiry calculations)
│   │   └── main.py              # FastAPI application factory and router mounting
│   ├── tests/                   # Pytest test suites (conftest, test_barcode.py, etc.)
│   ├── alembic.ini              # Alembic configuration
│   └── pyproject.toml           # Backend pinned dependencies and tooling configs
├── Frontend/
│   ├── src/
│   │   ├── components/          # Reusable components (BarcodeScanner.tsx)
│   │   ├── pages/               # Views (ScanPage.tsx with rapid stock adjustment)
│   │   ├── services/            # Axios API clients (api.ts, inventoryService.ts)
│   │   ├── types/               # TypeScript interfaces (inventory.ts)
│   │   ├── App.tsx              # Application shell and navigation layout
│   │   ├── App.css              # Custom scanner animation styles
│   │   ├── index.css            # Tailwind design tokens and base styles
│   │   └── main.tsx             # React entry point
│   ├── package.json             # Pinned frontend dependencies
│   └── vite.config.ts           # Vite configuration with Tailwind plugin & /api proxy
├── docs/                        # Specifications, architecture, implementation plans & build logs
│   ├── BUILD_LOG.md             # Running chronological record of completed phases
│   ├── BACKEND_STRUCTURE.md     # Architecture contract
│   ├── ENVIRONMENT.md           # Local system configuration
│   └── PRD.md                   # Product requirements document
└── README.md                    # Project documentation
```

---

## Getting Started

### Prerequisites
- **Python:** 3.12 or 3.13
- **Node.js:** 20+ (tested on Node 22.16.0 / npm 11.4.1)
- **PostgreSQL:** 15+ (tested on PostgreSQL 18.6 locally)

---

### Environment Configuration

Create a `.env` file in the `Backend/` folder:

```ini
# Backend/.env
APP_ENV=development

# PostgreSQL Connection Components
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD
DB_HOST=localhost
DB_PORT=5432
DB_NAME=food_rescue

# Frontend Cross-Origin Resource Sharing
CORS_ORIGINS=http://localhost:5173

# Inventory Configuration
EXPIRY_ALERT_DAYS=3

# Deterministic Demo Tenant ID (Milestone 1)
DEMO_BUSINESS_ID=a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

---

### Database Setup & Migrations

1. Ensure the PostgreSQL service is active and create the target database:
   ```sql
   CREATE DATABASE food_rescue;
   ```

2. From `Backend/`, apply the schema migration using Alembic:
   ```powershell
   .venv\Scripts\python.exe -m alembic upgrade head
   ```

3. Seed the database with the default business tenant and food categories:
   ```powershell
   .venv\Scripts\python.exe -m app.db.seed
   ```

---

### Backend Setup

1. Navigate to the `Backend/` directory:
   ```powershell
   cd Backend
   ```
2. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
3. Install pinned dependencies:
   ```powershell
   pip install -e .[dev]
   ```
4. Start the FastAPI development server:
   ```powershell
   uvicorn app.main:app --reload --port 8000
   ```
   * Swagger Documentation: `http://localhost:8000/api/docs`
   * Redoc Documentation: `http://localhost:8000/api/redoc`

---

### Frontend Setup

1. Navigate to the `Frontend/` directory:
   ```powershell
   cd Frontend
   ```
2. Install npm dependencies:
   ```powershell
   npm install
   ```
3. Run the development server (configured with dev proxy to port 8000):
   ```powershell
   npm run dev
   ```
4. Open your browser at `http://localhost:5173`.

---

## API Endpoints Summary

All routes are versioned under the `/api/v1` prefix.

| Method | Endpoint | Description |
|---|---|---|
| **Health** | | |
| `GET` | `/api/v1/health` | Health check reporting service status and database connectivity |
| **Businesses** | | |
| `GET` | `/api/v1/businesses` | List all registered business tenants |
| `GET` | `/api/v1/businesses/{id}` | Retrieve business by ID |
| `POST` | `/api/v1/businesses` | Register a new business tenant |
| `PUT` | `/api/v1/businesses/{id}` | Update business details |
| `DELETE` | `/api/v1/businesses/{id}` | Remove business tenant (cascades to inventory/transactions) |
| **Categories** | | |
| `GET` | `/api/v1/categories` | List all available food categories |
| `GET` | `/api/v1/categories/{id}` | Retrieve category by ID |
| `POST` | `/api/v1/categories` | Create category (validates perishability & storage constraints) |
| `PUT` | `/api/v1/categories/{id}` | Update category details |
| `DELETE` | `/api/v1/categories/{id}` | Remove category |
| **Inventory** | | |
| `GET` | `/api/v1/inventory` | Search & filter inventory (`search`, `category_id`, `expiry_before`) |
| `GET` | `/api/v1/inventory/barcode/{barcode}` | **Look up item by barcode within active tenant context** |
| `GET` | `/api/v1/inventory/expiring` | Retrieve items expiring within threshold (`threshold_days`, default 3) |
| `GET` | `/api/v1/inventory/expired` | Retrieve all items with expiry date earlier than today |
| `GET` | `/api/v1/inventory/{id}` | Retrieve specific item by UUID |
| `POST` | `/api/v1/inventory` | Create new inventory item (verifies non-negative quantity & unique barcode) |
| `PUT` | `/api/v1/inventory/{id}` | Update existing inventory item |
| `DELETE` | `/api/v1/inventory/{id}` | Remove item from inventory |
| `POST` | `/api/v1/inventory/upload-csv` | **Bulk import inventory via CSV file with duplicate handling** |
| **Transactions** | | |
| `GET` | `/api/v1/transactions` | List all historical stock adjustment transactions |
| `GET` | `/api/v1/transactions/inventory/{id}` | Retrieve complete audit trail for a specific inventory item |
| `POST` | `/api/v1/transactions` | **Execute rapid stock update** (`ADDED`, `SOLD`, `DONATED`, `EXPIRED`) |

---

## Core Workflows

### Barcode & QR Scanner Workflow
1. User clicks **"Scan Code"** on the web dashboard.
2. The scanner requests camera permission, enumerates media devices, and activates the rear/environment camera.
3. Upon barcode detection, `@zxing/browser` decodes the string and immediately halts camera streams to preserve battery and release hardware.
4. The frontend performs an automatic lookup via `GET /api/v1/inventory/barcode/{barcode}`.
5. If found, a verified item card displays real-time stock levels, product information, and expiry status.
6. The user selects an action (`SOLD` to deduct or `ADDED` to restock), enters a quantity, and submits.
7. The frontend dispatches a `POST /api/v1/transactions` mutation and automatically refreshes item data to display the new balance.

### CSV Bulk Ingestion Workflow
1. Client submits a CSV file containing inventory records via `POST /api/v1/inventory/upload-csv`.
2. Pandas validates file format, parses date fields, and verifies all required headers (`business_id`, `category_id`, `product_name`, `barcode`, `quantity`, `unit`, `purchase_date`, `expiry_date`).
3. The repository attempts bulk persistence; rows violating unique barcode constraints per tenant are skipped via atomic rollbacks without aborting valid rows.
4. The endpoint returns an ingestion summary:
   ```json
   {
     "filename": "inventory_batch.csv",
     "rows_found": 25,
     "rows_imported": 23,
     "rows_skipped": 2,
     "message": "CSV import completed."
   }
   ```

### Expiry Tracking Workflow
1. Inventory records store an authoritative `expiry_date` (Date format).
2. The `/api/v1/inventory/expiring?threshold_days=3` endpoint queries all items expiring between current server date and `today + 3 days`, returning calculated `days_remaining` and status `EXPIRING_SOON`.
3. The `/api/v1/inventory/expired` endpoint isolates inventory with `expiry_date < today` for waste audit reconciliation or disposal logging.

---

## Testing & Quality Verification

### Backend Tests (Pytest)
Run the automated test harness covering barcode lookup, stock adjustments, and inventory validation:
```powershell
cd Backend
.venv\Scripts\python.exe -m pytest tests/test_barcode.py -v
```
*Result:* 4 passed in 0.18s.

### Backend Linting (Ruff)
Validate Python code style and import ordering:
```powershell
cd Backend
.venv\Scripts\ruff.exe check app/repositories/inventory_repository.py app/services/inventory_service.py app/api/routes/inventory.py
```

### Frontend Build & Type Check
Verify TypeScript compilation, asset bundling, and lint checks:
```powershell
cd Frontend
npm run lint    # Oxlint static check (0 warnings, 0 errors)
npm run build   # TypeScript compilation & Vite production build
```

---

## Version Control & Release Status

* **Milestone 1:** Completed and verified against specification.
* **Release Tags:**
  * `v0.1.0` — Core Inventory CRUD, Category & Business APIs, Database Foundation.
  * `v0.2.0` — Transaction Audit System, Expiry Tracking Engine, CSV Bulk Upload, Barcode/QR Scanning Interface.

---
