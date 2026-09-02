"""Test barcode lookup and stock update workflow."""

from decimal import Decimal

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_barcode_lookup_success():
    """Verify existing demo barcode lookup returns product details."""
    response = client.get("/api/v1/inventory/barcode/8901234567890")
    assert response.status_code == 200
    data = response.json()
    assert data["barcode"] == "8901234567890"
    assert data["product_name"] == "Fresh Milk"
    assert "quantity" in data
    assert "business_id" in data


def test_barcode_lookup_not_found():
    """Verify unknown barcode returns 404."""
    response = client.get("/api/v1/inventory/barcode/0000000000000")
    assert response.status_code == 404
    assert "detail" in response.json()


def test_rapid_stock_update_flow():
    """Test full flow: lookup item -> ADDED transaction -> SOLD transaction -> verify quantity."""
    # 1. Lookup item
    lookup_res = client.get("/api/v1/inventory/barcode/8901234567891")
    assert lookup_res.status_code == 200
    item = lookup_res.json()
    initial_qty = Decimal(str(item["quantity"]))

    # 2. Add Stock (ADDED)
    add_payload = {
        "business_id": item["business_id"],
        "inventory_id": item["inventory_id"],
        "transaction_type": "ADDED",
        "quantity": 5.0,
        "reference": "TEST-RESTOCK",
    }
    add_res = client.post("/api/v1/transactions", json=add_payload)
    assert add_res.status_code == 201

    # Verify increased quantity
    item_after_add = client.get("/api/v1/inventory/barcode/8901234567891").json()
    assert Decimal(str(item_after_add["quantity"])) == initial_qty + Decimal("5.0")

    # 3. Sell Stock (SOLD)
    sell_payload = {
        "business_id": item["business_id"],
        "inventory_id": item["inventory_id"],
        "transaction_type": "SOLD",
        "quantity": 2.0,
        "reference": "TEST-SALE",
    }
    sell_res = client.post("/api/v1/transactions", json=sell_payload)
    assert sell_res.status_code == 201

    # Verify decreased quantity
    item_after_sell = client.get("/api/v1/inventory/barcode/8901234567891").json()
    assert Decimal(str(item_after_sell["quantity"])) == initial_qty + Decimal("3.0")


def test_rapid_stock_insufficient_quantity():
    """Verify selling more than available quantity fails with 400 Bad Request."""
    lookup_res = client.get("/api/v1/inventory/barcode/8901234567891")
    assert lookup_res.status_code == 200
    item = lookup_res.json()
    current_qty = Decimal(str(item["quantity"]))

    sell_payload = {
        "business_id": item["business_id"],
        "inventory_id": item["inventory_id"],
        "transaction_type": "SOLD",
        "quantity": float(current_qty + Decimal("1000.0")),
        "reference": "OVER-SELL-TEST",
    }
    res = client.post("/api/v1/transactions", json=sell_payload)
    assert res.status_code == 400
    assert "Insufficient" in res.json().get("detail", "")
