import os
import sys

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.session import test_db_connection

if test_db_connection():
    print("✅ Conexión a PostgreSQL exitosa!")
else:
    print("❌ Error de conexión a la base de datos")