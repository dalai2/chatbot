from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello from FastAPI!"}

def test_echo_message():
    response = client.post("/echo/", json={"text": "test message"})
    assert response.status_code == 200
    assert response.json() == {"echoed": "test message"}

def test_get_env_default():
    response = client.get("/env/")
    assert response.status_code == 200
    assert response.json() == {"environment": "default"}