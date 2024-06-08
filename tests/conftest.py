import pytest
from fastapi.testclient import TestClient
from app import app


@pytest.fixture(scope="module")
def test_app():
    return TestClient(app)

