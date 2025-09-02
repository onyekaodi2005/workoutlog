from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_index():
    r = client.get('/')
    assert r.status_code == 200
