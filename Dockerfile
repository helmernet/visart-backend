FROM python:3.11-slim

WORKDIR /app

# Instala las dependencias del sistema necesarias (por ejemplo, para psycopg2)
RUN apt-get update && apt-get install -y build-essential libpq-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Copia el archivo de dependencias
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código fuente del proyecto
COPY . .

# Expone el puerto para FastAPI/Uvicorn
EXPOSE 8000

# Comando por defecto para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]