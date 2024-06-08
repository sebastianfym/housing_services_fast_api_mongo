import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_tariffs(test_app: TestClient):
    data = {
        "name": "maintenance",
        "rate": 150,
        "unit": "cub"
    }
    response = test_app.post("/api/v1/house/tariffs/", json=data)
    assert response.status_code == 200

    data = {
        "name": "water",
        "rate": 50,
        "unit": "cub"
    }
    response = test_app.post("/api/v1/house/tariffs/", json=data)
    assert response.status_code == 200

    response = test_app.get(f"/api/v1/house/tariffs/{response.json().get('_id')}")
    assert response.status_code == 200
