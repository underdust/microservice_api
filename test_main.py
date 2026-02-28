from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_multiply_by_10():
    response = client.get("/mul10/5")
    assert response.status_code == 200
    assert response.json() == {"result": 50}
    
    response = client.get("/mul10/0")
    assert response.status_code == 200
    assert response.json() == {"result": 0}