# BACKEND_STRUCTURE — Milestone 1

## 1. Architecture
Pattern:
REST API → Router → Service → Repository/ORM → PostgreSQL

Keep business logic out of route handlers where practical.

Suggested data flow:
Client → Router → Pydantic validation → Service → SQLAlchemy → PostgreSQL

## 2. Project Structure
backend/
  app/
    main.py
    core/
      config.py
      errors.py
    db/
      session.py
      base.py
    models/
      business.py
      category.py
      inventory.py
      inventory_transaction.py
    schemas/
      inventory.py
      category.py
      csv_import.py
      common.py
    api/
      deps.py
      routes/
        health.py
        inventory.py
        categories.py
        imports.py
        pos.py
        dashboard.py
    services/
      inventory_service.py
      expiry_service.py
      import_service.py
      pos_service.py
      dashboard_service.py
    repositories/
      inventory_repository.py
      category_repository.py
      transaction_repository.py
    utils/
      dates.py
  alembic/
  tests/

## 3. Database Schema

### businesses
Purpose: tenant/business record.

Columns:
- business_id UUID PK
- name VARCHAR NOT NULL
- email VARCHAR UNIQUE NOT NULL
- phone VARCHAR NULL
- address TEXT NULL
- created_at TIMESTAMPTZ NOT NULL DEFAULT now()
- updated_at TIMESTAMPTZ NOT NULL DEFAULT now()

### categories
Purpose: food taxonomy.

Columns:
- category_id UUID PK
- name VARCHAR(80) UNIQUE NOT NULL
- perishability VARCHAR(20) NOT NULL
- storage_type VARCHAR(20) NOT NULL
- created_at TIMESTAMPTZ NOT NULL DEFAULT now()
- updated_at TIMESTAMPTZ NOT NULL DEFAULT now()

Constraints:
- perishability ∈ {HIGH, MEDIUM, LOW}
- storage_type ∈ {COLD, DRY, FROZEN}

### inventory_items
Purpose: tenant-owned food inventory.

Columns:
- inventory_id UUID PK
- business_id UUID FK → businesses.business_id ON DELETE CASCADE
- category_id UUID FK → categories.category_id
- product_name VARCHAR(150) NOT NULL
- barcode VARCHAR(100) NULL
- quantity NUMERIC(12,3) NOT NULL CHECK quantity >= 0
- unit VARCHAR(20) NOT NULL
- purchase_date DATE NULL
- expiry_date DATE NOT NULL
- created_at TIMESTAMPTZ NOT NULL DEFAULT now()
- updated_at TIMESTAMPTZ NOT NULL DEFAULT now()

Indexes:
- (business_id)
- (business_id, expiry_date)
- (business_id, category_id)
- unique/business-scoped barcode where barcode IS NOT NULL

### inventory_transactions
Purpose: immutable audit trail for stock changes.

Columns:
- transaction_id UUID PK
- business_id UUID FK → businesses.business_id ON DELETE CASCADE
- inventory_id UUID FK → inventory_items.inventory_id ON DELETE CASCADE
- transaction_type VARCHAR(20) NOT NULL
- quantity NUMERIC(12,3) NOT NULL CHECK quantity > 0
- reference VARCHAR(100) NULL
- created_at TIMESTAMPTZ NOT NULL DEFAULT now()

Allowed transaction_type:
ADDED
UPDATED
SOLD
EXPIRED
DONATED (reserved for later; do not create donation workflows in M1)

Rules:
- Inventory-changing operations create corresponding transactions.
- Transaction rows are never edited through normal API.
- A transaction must always use the same business_id as the inventory item.

## 4. Multi-Tenant Rules
- Business is the tenant.
- Every business-owned table includes business_id where practical.
- Every query on inventory/transactions includes a business filter.
- Never accept an arbitrary business_id from the client if a future authenticated context exists.
- For M1 demo mode, use a single deterministic demo business ID injected by configuration/dependency.
- Add tests for cross-tenant access denial.

## 5. API Base
Use:
`/api/v1`

## 6. Required Endpoints

### Health
GET `/api/v1/health`
Response: service/database health summary.

### Dashboard
GET `/api/v1/dashboard/summary`
Returns:
- total_items
- total_quantity
- expiring_soon_count
- expired_count
- recent_activity

### Inventory
POST `/api/v1/inventory`
GET `/api/v1/inventory`
GET `/api/v1/inventory/{inventory_id}`
PUT `/api/v1/inventory/{inventory_id}`
DELETE `/api/v1/inventory/{inventory_id}`

Query parameters:
- search
- category_id
- expiry_status
- page
- page_size
- sort_by
- sort_order

### Expiry
GET `/api/v1/inventory/expiry-alerts`
Query:
- threshold_days default 3

Return:
- inventory_id
- product_name
- expiry_date
- days_to_expiry
- status

### Categories
POST `/api/v1/categories`
GET `/api/v1/categories`
GET `/api/v1/categories/{category_id}`
PUT `/api/v1/categories/{category_id}`
DELETE `/api/v1/categories/{category_id}`

### CSV Import
POST `/api/v1/inventory/import/validate`
POST `/api/v1/inventory/import/commit`

Validate:
- file type
- row limits
- required headers
- date formats
- numeric quantity
- category existence/normalization
- duplicate barcode within tenant
- expiry date validity

### POS
POST `/api/v1/integrations/pos/sales`
Example conceptual payload:
{
  "business_id": "...",
  "barcode": "...",
  "quantity_sold": 2,
  "reference": "POS-ORDER-123"
}

For demo mode, business_id must match the active demo tenant.

## 7. Request / Response Rules
- Use Pydantic schemas for all external payloads.
- Use UTC timestamps for server timestamps.
- Use ISO-8601 date strings in API responses.
- Return consistent JSON structures.
- Use snake_case in API JSON.
- Never return SQLAlchemy objects directly.

## 8. Error Model
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed.",
    "details": [
      {"field": "quantity", "message": "Quantity must be greater than or equal to 0."}
    ]
  }
}

## 9. Expiry Rules
Let `days_to_expiry = expiry_date - current_server_date`.

Statuses:
- EXPIRED: < 0
- CRITICAL: 0–1
- WARNING: 2–3
- SAFE: > 3

Default threshold = 3 days.
Do not store days_to_expiry because it is derived.

## 10. CSV Rules
Required:
Product, Category, Quantity, Expiry

Optional:
Unit, Purchase Date, Barcode, Storage Type

Map category names case-insensitively after trimming whitespace.

Do not silently discard malformed rows.
Provide row number and exact error.

## 11. POS Behavior
For a sale:
1. Locate inventory item within business by ID or barcode.
2. Validate sufficient stock.
3. Decrement quantity transactionally.
4. Create SOLD transaction.
5. Commit both operations atomically.
6. Return updated quantity.

## 12. Migration Strategy
Use Alembic.
- No ad-hoc `CREATE TABLE` execution from application startup.
- Migrations are the source of truth.
- Provide initial migration.
- Provide a command in README to migrate a fresh local database.
- Provide rollback instructions.

Optional convenience:
Generate/export `database/schema.sql` for inspection/documentation, but do not maintain two independent schema sources.

## 13. Testing
Use pytest + httpx.
Cover:
- CRUD
- validation
- expiry classification
- CSV validation
- CSV commit
- barcode uniqueness
- tenant isolation
- POS sale transactionality
- dashboard counts
- database health check

## 14. Database Integrity
Prefer database constraints for:
- non-negative quantities
- required fields
- valid enum values
- foreign keys
- unique tenant-scoped barcode

Do not rely only on frontend validation.
