import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Datos de prueba
post_data = {
    "title": "Test Post",
    "content": "Test content",
    "image_url": None,
    "is_published": True
}

def test_post_validation():
    # Test con datos inválidos
    invalid_data = {"title": ""}
    response = client.post("/api/posts/", json=invalid_data)  # ✅ Cambiado a /api/posts/
    assert response.status_code == 422

def test_nonexistent_post():
    response = client.get("/api/posts/9999")  # ✅ Cambiado a /api/posts/
    assert response.status_code == 404

def test_duplicate_post_creation():
    # Crear el mismo post dos veces
    client.post("/api/posts/", json=post_data)  # ✅ Cambiado a /api/posts/
    response = client.post("/api/posts/", json=post_data)  # ✅ Cambiado a /api/posts/
    assert response.status_code == 201  # Asumiendo que se permiten posts duplicados

def test_update_nonexistent_post():
    update_data = {"title": "Updated Title"}
    response = client.put("/api/posts/9999", json=update_data)  # ✅ Cambiado a /api/posts/
    assert response.status_code == 404

def test_delete_nonexistent_post():
    response = client.delete("/api/posts/9999")  # ✅ Cambiado a /api/posts/
    assert response.status_code == 404