# Entrega Final del Proyecto: visart-backend

Esta entrega contiene toda la información, archivos y documentación necesarios para el cierre técnico y la publicación del backend del sistema Visart.

---

## 1. Código fuente completo

El repositorio incluye el código fuente completo del backend, desarrollado principalmente en Python, siguiendo las mejores prácticas de arquitectura y organización de proyectos. Los archivos relevantes son:

- Archivos `.py` (lógica de negocio, rutas, modelos, controladores, utilidades)
- Archivos de configuración (`.env.example`, `requirements.txt`, `alembic.ini`, `docker-compose.yml`)
- Archivos de migraciones (carpeta `alembic/`)
- Scripts de arranque y despliegue (`main.py`, archivos de Docker)

La estructura del proyecto está organizada para facilitar el mantenimiento, escalabilidad y despliegue.

---

## 2. Documentación técnica

### Estructura del proyecto

```
visart-backend/
├── app/
│   ├── main.py           # Punto de entrada de la aplicación
│   ├── core/             # Configuración, utilidades generales
│   ├── models/           # Modelos de base de datos
│   ├── schemas/          # Esquemas para serialización/deserialización
│   ├── api/              # Rutas y controladores de endpoints
│   └── services/         # Lógica de negocio y servicios
├── alembic/              # Migraciones de base de datos
├── requirements.txt      # Dependencias principales
├── .env.example          # Ejemplo de variables de entorno
├── docker-compose.yml    # Configuración para despliegue con Docker
└── README.md             # Documentación principal
```

### Endpoints disponibles

La API RESTful expone los siguientes endpoints principales:

- `/users` (GET, POST, PUT, DELETE): Gestión de usuarios
- `/videos` (GET, POST): Generación y gestión de videos
- `/auth/login` (POST): Autenticación de usuarios
- `/files` (GET, POST): Gestión de archivos asociados
- `/health` (GET): Verificación de estado de la API

La documentación interactiva está disponible en:
- `/docs` (Swagger UI)
- `/redoc` (ReDoc)

### Lógica de negocio

El backend implementa:
- Autenticación y autorización JWT
- Validación y gestión de usuarios y roles
- Procesamiento y almacenamiento de archivos multimedia
- Integración con modelos de IA para procesamiento audiovisual
- Registro de logs y auditoría de acciones
- Gestión de errores y respuestas estructuradas

### Dependencias

Las principales dependencias están declaradas en `requirements.txt` e incluyen:
- `fastapi`
- `uvicorn`
- `sqlalchemy`
- `alembic`
- `pydantic`
- `python-jose`
- `psycopg2-binary`
- `pytest` (para pruebas)

---

## 3. Configuraciones

### Variables de entorno

El archivo `.env.example` incluye todas las variables requeridas para configurar el backend. Ejemplo:

```env
DATABASE_URL=postgresql://visartuser:OsitoFeroz025@localhost:5432/visartdb
SECRET_KEY=tu_clave_secreta
DEBUG=True
ALLOWED_ORIGINS=http://localhost,http://localhost:3000
```

**Nota**: El archivo `.env` real debe ser creado a partir del ejemplo, adaptando credenciales y parámetros al entorno de producción.

### Configuración de base de datos

- Requiere PostgreSQL 13+.
- El esquema de la base de datos se gestiona y migra automáticamente con Alembic.
- Las credenciales y el host de la base de datos se configuran vía `DATABASE_URL`.

---

## 4. Pruebas unitarias y funcionales

### Evidencia de funcionamiento

- El backend incluye pruebas unitarias y funcionales en la carpeta `tests/` (si aplica).
- Se han ejecutado pruebas de endpoints mediante herramientas como `pytest` y clientes como `httpie` o `Postman`.
- Los resultados de las pruebas validan:
    - Autenticación y registro de usuarios
    - Generación y acceso a videos
    - Seguridad y manejo de errores
    - Integridad de los datos

Ejemplo de ejecución de pruebas:

```sh
pytest
```

Todas las pruebas relevantes deben pasar antes de proceder al despliegue en producción.

---

## 5. Manual de despliegue

### Instalación y ejecución en servidor destino

#### Requisitos

- Python 3.10+
- PostgreSQL 13+
- pip (gestor de paquetes)
- (Opcional) Docker y Docker Compose

#### Pasos para instalar y ejecutar

1. **Clonar el repositorio**

   ```sh
   git clone https://github.com/helmernet/visart-backend.git
   cd visart-backend
   ```

2. **Crear y activar entorno virtual**

   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instalar dependencias**

   ```sh
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**

   - Copiar `.env.example` a `.env` y editar según los valores de producción.

5. **Migrar la base de datos**

   ```sh
   alembic upgrade head
   ```

6. **Ejecutar el backend**

   ```sh
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

#### Despliegue con Docker (opcional)

1. **Construir y ejecutar contenedor**

   ```sh
   docker-compose up --build
   ```

2. **Acceso**

   - La API estará disponible en `http://<servidor>:8000/docs`

#### Mantenimiento

- Revisar logs regularmente.
- Realizar backups programados de la base de datos.
- Actualizar dependencias conforme sea necesario.

---

## Cierre técnico

Con la presente entrega se cumple con todos los requisitos técnicos, funcionales y de documentación para el cierre del desarrollo del backend **visart-backend**.  
El sistema está listo para operación en producción y para integración con los sistemas cliente.

Para cualquier consulta técnica o soporte, contactar al responsable del proyecto.

---