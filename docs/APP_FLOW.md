# APP_FLOW — Milestone 1

## 1. Entry Points
- `/` → redirect to `/dashboard`
- `/dashboard`
- `/inventory`
- `/inventory/import`
- `/categories`
- `/inventory/scan` or modal-based scanner from inventory page

No public authentication flow is required for Milestone 1.

## 2. Core User Flow A — Inventory CRUD
1. User opens Dashboard.
2. Dashboard loads tenant-scoped inventory summary.
3. User opens Inventory.
4. User sees inventory table.
5. User can search, filter by category, and filter by expiry status.
6. User selects Add Inventory.
7. User enters product, category, quantity, unit, purchase date, expiry date, barcode.
8. Client validates obvious field errors.
9. Backend validates again.
10. Backend writes inventory item and an `ADDED` transaction.
11. UI refreshes the item list and summary.
12. Toast confirms success.

Failure paths:
- Invalid fields → inline validation.
- Duplicate barcode for same business → clear conflict message.
- Database error → generic safe error + retry action.

## 3. Core User Flow B — CSV Import
1. User opens Import.
2. User sees accepted file format and a downloadable sample CSV.
3. User chooses CSV.
4. Frontend sends multipart upload.
5. Backend parses and validates all rows.
6. Frontend receives a preview/validation summary.
7. User confirms import.
8. Backend persists valid import according to the selected atomicity policy.
9. UI shows successful and failed row counts.
10. Inventory page reflects imported items.

States:
- Idle
- File selected
- Parsing
- Validation errors
- Ready to import
- Importing
- Success
- Failure

## 4. Core User Flow C — Expiry Alerts
1. Dashboard requests expiry summary.
2. Backend calculates days-to-expiry using the current server date.
3. Items are grouped as:
   - Expired
   - Critical: 0–1 days remaining
   - Warning: 2–3 days remaining
   - Safe: >3 days remaining
4. Dashboard displays alert counts.
5. User can open the expiring list.
6. Inventory page can filter to expiring items.

## 5. Core User Flow D — Barcode / QR Scan
1. User opens scanner.
2. Browser requests camera access.
3. User points camera at a supported barcode/QR code.
4. Scanner returns decoded value.
5. Frontend searches inventory by the current business + barcode.
6. If found, open the item details/edit view.
7. If not found, show “No inventory item found” with actions to search or create.

Failure states:
- Camera permission denied
- Camera unavailable
- Unsupported code
- No matching inventory item

## 6. Core User Flow E — Mock POS Sale
1. A POS client sends a sale event to the REST endpoint.
2. Backend validates business/tenant and item reference.
3. Backend checks sufficient quantity.
4. Backend decrements stock.
5. Backend creates a `SOLD` inventory transaction.
6. Backend returns updated quantity.

Failure:
- Inventory item not found
- Wrong business
- Insufficient stock
- Invalid payload

## 7. Navigation Map
Home
├── Dashboard
├── Inventory
│   ├── All Inventory
│   ├── Add Item
│   ├── Edit Item
│   └── Scanner
├── Import CSV
└── Categories

## 8. Screen Inventory

### Dashboard
Route: `/dashboard`
Access: demo tenant in Milestone 1
Purpose: operational summary
Key elements:
- Total inventory items
- Total quantity
- Expiring soon
- Expired
- Recent inventory activity
- Quick actions

### Inventory
Route: `/inventory`
Key elements:
- Search
- Category filter
- Expiry filter
- Inventory table/cards
- Add/Edit/Delete
- Scan
- Pagination if needed

### Import
Route: `/inventory/import`
Key elements:
- Drop zone/file picker
- Format guidance
- Sample CSV
- Validation summary
- Import action
- Results

### Categories
Route: `/categories`
Key elements:
- Category list
- Add
- Edit
- Delete
- Perishability
- Storage type

## 9. Error Handling
Standard error response shape:
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed.",
    "details": [
      {"field": "expiry_date", "message": "Expiry date is required."}
    ]
  }
}

Map:
- 400 validation/business-rule issue
- 404 missing resource
- 409 conflict (e.g. duplicate barcode within tenant)
- 422 request validation where framework semantics require it
- 500 unexpected server error

Never expose stack traces to the client.

## 10. Responsive Behavior
Mobile:
- Table may become cards or horizontally scroll in a controlled container.
- Scanner action must be easy to access.
- Form fields should be one column.
Desktop:
- Two-column dashboard regions and full-width table.
