from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_mul10_with_positive_number():
    response = client.get("/mul10/5")
    assert response.status_code == 200
    assert response.json() == {"result": 50}

def test_mul10_with_zero():
    response = client.get("/mul10/0")
    assert response.status_code == 200
    assert response.json() == {"result": 0}

def test_mul10_with_large_number():
    response = client.get("/mul10/100")
    assert response.status_code == 200
    assert response.json() == {"result": 1000}

def test_mul10_with_negative_number():
    response = client.get("/mul10/-3")
    assert response.status_code == 200
    assert response.json() == {"result": -30}