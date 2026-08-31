# PRD — AI-Powered Food Waste Management Platform
## Milestone 1: Inventory Management & Expiry Tracking

### 1. Product Overview
Project: AI-Powered Food Waste Management Platform for Surplus Identification and Redistribution Optimization.

Milestone 1 covers only the Weeks 1–2 module from the project brief:
- Inventory input
- Expiry tracking and alerts
- Food categorization
- Barcode/QR-ready inventory updates
- CSV bulk upload
- POS integration through REST API architecture
- Multi-tenant business inventory and transaction storage

### 2. Problem
Food service businesses, supermarkets, and similar organizations generate avoidable waste because of poor inventory management and inaccurate demand planning. The full platform will later use AI to predict waste and connect businesses with recipient organizations.

Milestone 1 establishes the reliable inventory foundation required by those later modules.

### 3. Users / Tenant Model
Milestone 1 is business-tenant focused.
- A business is a tenant.
- Inventory records belong to exactly one business.
- Every inventory query/write must be scoped to the current business/tenant.
- Do not leak records between businesses.
- Full user authentication/authorization is NOT part of Milestone 1; keep the data model and service layer ready to add it later.
- Use a seeded demo business/tenant for local development and demonstration.

### 4. Must-Have Features
#### Inventory
- Create inventory item
- Read/list inventory items
- Update inventory item
- Delete inventory item
- Search/filter/sort inventory
- Track quantity and unit
- Track purchase date and expiry date
- Store barcode/QR identifier
- Associate each item with a food category
- Associate each item with perishability and storage requirements through category metadata

#### CSV Bulk Upload
- Upload CSV from the frontend
- Parse/validate on backend
- Support at minimum:
  Product, Category, Quantity, Expiry
- Also support optional:
  Unit, Purchase Date, Barcode, Storage Type
- Show row-level validation errors
- Do not partially commit invalid rows in a way that leaves ambiguous state
- Return import summary: total rows, successful rows, failed rows
- Use Pandas only for parsing/transformation; persistence remains through the application data layer

#### Expiry Tracking
- Calculate days remaining until expiry
- Default alert threshold: 3 days
- Show expired items separately
- Show items approaching expiry
- Provide an expiry-alert API
- Alert data may be computed dynamically; persistent notification infrastructure is outside Milestone 1

#### Food Categorization
Use a small seeded taxonomy with examples:
- Dairy — High perishability — Cold
- Fruits — High perishability — Cold
- Bakery — Medium perishability — Dry
- Grains — Low perishability — Dry
- Frozen Foods — High perishability — Frozen
- Vegetables — High perishability — Cold

The taxonomy must be editable through category CRUD APIs, but do not build an elaborate taxonomy-management UI unless needed.

#### Barcode / QR
- Inventory model must support a barcode field.
- Implement a mobile-friendly scan interaction if practical with the local frontend.
- Prefer a browser-compatible scanner library such as @zxing/browser; pin the exact version used.
- Scanning should populate/search the inventory item rather than create duplicate records automatically.

#### POS REST Integration
The project brief requires POS integration through REST APIs.
Because no real POS vendor credentials are supplied for Milestone 1:
- Build a vendor-neutral POS ingestion endpoint/adapter interface.
- Provide a mock/local POS payload example.
- Demonstrate that a sale event can decrement inventory and create an inventory transaction.
- Do not integrate with a real external POS provider.

### 5. Out of Scope for Milestone 1
DO NOT implement:
- AI/ML waste prediction
- Prophet or LSTM
- Waste risk scoring model
- Smart reorder recommendations
- NGO registration/requirements
- Redistribution marketplace
- Donation matching
- Pickup scheduling
- Donation notifications
- Sustainability/CO2 analytics
- Cloud database deployment
- Real production POS vendor integration
- Email/SMS notification infrastructure
- Full authentication unless an existing project scaffold already requires it

Create clean extension points for future modules, but do not build them.

### 6. Acceptance Criteria
Milestone 1 is complete when:
1. App runs locally.
2. PostgreSQL is local and is the only database used.
3. FastAPI connects to PostgreSQL successfully.
4. Frontend communicates with backend over REST.
5. CRUD for inventory works end-to-end.
6. Inventory is tenant-scoped by business_id.
7. Categories work.
8. CSV upload validates and imports correctly.
9. Expiry alerts correctly classify items using the 3-day default threshold.
10. Barcode field and scan/search flow work.
11. Mock POS REST ingestion can record a sale and reduce stock.
12. Transactions are recorded for inventory changes.
13. Invalid requests produce consistent JSON errors.
14. No hardcoded secrets are committed.
15. A fresh clone can be run using the documented setup steps.
16. Backend tests cover core services and API behavior.
17. Frontend handles loading, empty, success, and error states.
18. The UI is responsive on desktop and mobile.

### 7. Success Metrics
- Zero cross-tenant inventory leakage in tests.
- Successful CRUD requests persist correctly.
- CSV importer reports row-level failures clearly.
- Expiry calculations use the server date and are deterministic in tests.
- Inventory transaction history remains consistent with stock-changing operations.

### 8. Non-Functional Requirements
- Maintainable modular code.
- Strong request/response validation.
- SQL constraints for data integrity.
- Database migrations are reproducible.
- Sensible indexes on tenant and expiry lookup paths.
- No silent exception swallowing.
- Accessible UI with keyboard focus states.
- Mobile-responsive inventory workflows.
- Clear documentation.
