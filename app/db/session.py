from app.db.base import Base
from app.config import load_settings  # ✅ Cambiado a load_settings
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

# Cargar configuración
settings = load_settings()  # ✅ Agregada esta línea

# Crear engine de SQLAlchemy usando la configuración de settings
engine = create_engine(
    str(settings.DATABASE_URL),
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    echo=settings.DEBUG
)

# Crear session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

# Función para obtener sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para testear conexión a la base de datos
def test_db_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return True
    except Exception as e:
        print(f"Error de conexión a la base de datos: {e}")
        return False