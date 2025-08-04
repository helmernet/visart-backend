import psycopg2
import os
from dotenv import load_dotenv

# Carga el archivo .env desde el mismo directorio del backend
load_dotenv()

dsn = os.getenv("DATABASE_URL")
print("DEBUG DSN:", repr(dsn))

try:
    conn = psycopg2.connect(dsn)
    print("¡Conexión exitosa a PostgreSQL!")
    conn.close()
except Exception as e:
    print("ERROR al conectar:", e)