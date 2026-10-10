from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.main import app

client = TestClient(app)
API_KEY = get_settings().api_key


def test_try_on() -> None:
    response = client.post(
        "api/v1/try-on",
        json={"page_url": "https://shop.example/jacket", "category": "apparel"},
        headers={"X-API-Key": API_KEY},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["category"] == "apparel"
    assert body["anchors"]
