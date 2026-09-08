from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_pos_sync_unknown_barcode():
    response = client.post(
        "/api/v1/pos/sync",
        json={
            "business_id": "72be0ef6-2e8d-487b-9bf6-d00208f4479a",
            "pos_name": "Test POS",
            "sales": [
                {
                    "barcode": "9999999999999",
                    "quantity": 1
                }
            ],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["failed"] == 1