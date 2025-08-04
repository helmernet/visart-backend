import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()  # Carga las variables del archivo .env

DATABASE_URL = os.getenv("DATABASE_URL")
print("DEBUG DATABASE_URL:", repr(DATABASE_URL))  # <-- Línea para depuración

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()