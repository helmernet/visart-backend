# tests/conftest.py
import pytest
import uuid
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.config import load_settings

# Configuración de base de datos de prueba
TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas de prueba
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def test_user(client):
    # Crear usuario de prueba con datos únicos
    unique_id = str(uuid.uuid4())[:8]
    user_data = {
        "username": f"testuser_{unique_id}",
        "email": f"test_{unique_id}@example.com",
        "password": "Testpassword123!"
    }
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 201
    return response.json()

@pytest.fixture(scope="function")
def auth_token(client, test_user):
    # Obtener token de autenticación
    login_data = {
        "username": test_user["username"],
        "password": "Testpassword123!"
    }
    response = client.post("/api/auth/token", data=login_data)
    assert response.status_code == 200
    return response.json()["access_token"]