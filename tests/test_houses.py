import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_house(test_app: TestClient):
    data = {
        "address": "Test house",
        "apartments": [
        ]
    }
    response = test_app.post("/api/v1/house/houses/", json=data)

    assert response.status_code == 200
    assert response.json().get("address") == "Test house"

    response = test_app.get(f"/api/v1/house/houses/{response.json().get('_id')}")
    assert response.status_code == 200
    assert response.json().get("apartments") == []