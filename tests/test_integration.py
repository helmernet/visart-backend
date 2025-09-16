import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.db.base import Base

# Configurar base de datos de prueba
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Datos de prueba
post_data = {
    "title": "Test Post",
    "content": "Test content",
    "image_url": None,
    "is_published": True
}

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_post():
    response = client.post("/api/posts/", json=post_data)  # ✅ Cambiado a /api/posts/
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == post_data["title"]
    assert "id" in data

def test_get_posts():
    response = client.get("/api/posts/")  # ✅ Cambiado a /api/posts/
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_single_post():
    # Primero crear un post
    create_response = client.post("/api/posts/", json=post_data)  # ✅ Cambiado a /api/posts/
    post_id = create_response.json()["id"]
    
    response = client.get(f"/api/posts/{post_id}")  # ✅ Cambiado a /api/posts/
    assert response.status_code == 200
    assert response.json()["id"] == post_id

def test_update_post():
    create_response = client.post("/api/posts/", json=post_data)  # ✅ Cambiado a /api/posts/
    post_id = create_response.json()["id"]
    
    update_data = {"title": "Updated Title"}
    response = client.put(f"/api/posts/{post_id}", json=update_data)  # ✅ Cambiado a /api/posts/
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

def test_delete_post():
    create_response = client.post("/api/posts/", json=post_data)  # ✅ Cambiado a /api/posts/
    post_id = create_response.json()["id"]
    
    response = client.delete(f"/api/posts/{post_id}")  # ✅ Cambiado a /api/posts/
    assert response.status_code == 204
    
    # Verificar que fue eliminado
    get_response = client.get(f"/api/posts/{post_id}")  # ✅ Cambiado a /api/posts/
    assert get_response.status_code == 404