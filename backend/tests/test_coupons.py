from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app

client = TestClient(app)
API_KEY = get_settings().api_key


def test_coupons_requires_key() -> None:
    response = client.get("/api/v1/coupons")
    assert response.status_code == 401


def test_coupons_filter() -> None:
    response = client.get(
        "/api/v1/coupons",
        params={"category": "accessory"},
        headers={"X-API-Key": API_KEY},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["results"]
    assert all(item["category"] == "accessory" for item in body["results"])
