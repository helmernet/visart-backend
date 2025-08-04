from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    # Puedes ajustar según el contenido esperado en tu endpoint raíz
    body = response.json()
    assert "message" in body
    assert "Visart Backend" in body["message"] or "funcionando" in body["message"]