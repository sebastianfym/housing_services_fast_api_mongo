import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_apartments(test_app: TestClient):
    data = {
        "number": 1,
        "area": 22,
        "water_meters": []
    }
    response = test_app.post("/api/v1/house/apartment/", json=data)

    assert response.status_code == 200
    assert response.json().get("area") == 22

    response = test_app.get(f"/api/v1/house/apartments/{response.json().get('_id')}")
    assert response.status_code == 200
    assert response.json().get("water_meters") == []

    data = {
        "value": 945
    }
    response = test_app.post(f"/api/v1/house/apartments/{response.json().get('_id')}/water_meter", json=data)
    assert response.status_code == 200

