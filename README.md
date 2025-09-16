# visart-backend

Repositorio para el backend del proyecto **Visart**.

## Estado actual (Septiembre 2025)

- **Último commit:** 5 de agosto de 2025.
- **Versión principal:** Estable, con integración de endpoints para autenticación, usuarios y posts.
- **Integración:** Probada con frontend local y documentación Swagger disponible.
- **Workflow de CI:** GitHub Actions configurado para pruebas automatizadas.
- **Base de datos:** Conexión PostgreSQL definida en `.env`.
- **Endpoints activos:** `/api/auth/register`, `/api/auth/login`, `/api/users/`, `/api/posts/`, `/api/health`
- **Documentación:** Swagger UI [http://localhost:8000/docs](http://localhost:8000/docs)
- **Configuración de entorno:** Archivo `.env` para credenciales y URL de base de datos.

---

## Descripción

Este proyecto contiene el backend desarrollado en Python para la aplicación Visart. Su objetivo es proveer servicios y API REST para la gestión de datos, autenticación de usuarios y funcionalidades principales de la plataforma.

## Características principales

- API RESTful desarrollada en Python.
- Manejo de autenticación y autorización de usuarios.
- Gestión de datos y recursos de la aplicación.
- Estructura preparada para despliegue y desarrollo colaborativo.

## Requisitos

- Python 3.8 o superior
- (Opcional) Entorno virtual: `venv` o similar

## Instalación

1. Clona el repositorio:
    ```bash
    git clone https://github.com/helmernet/visart-backend.git
    cd visart-backend
    ```

2. Crea y activa un entorno virtual:
    ```bash
    python -m venv venv
    source venv/bin/activate    # En Linux/Mac
    venv\Scripts\activate       # En Windows
    ```

3. Instala las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Configuración

Crea un archivo `.env` basado en `.env.example`:

```dotenv
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/visartdb
```

## Uso

```bash
python -m app.main
```

La documentación Swagger está disponible en [http://localhost:8000/docs](http://localhost:8000/docs).

## Estructura del proyecto

- `main.py`: Archivo principal de ejecución.
- `app/`: Código fuente principal de la aplicación.
- `requirements.txt`: Dependencias del proyecto.
- `.env`: Variables de entorno (no debe subirse al repo).
- `.gitignore`: Archivos y carpetas ignoradas por Git.

## Endpoints principales

- `/api/auth/register` – Registro de usuario
- `/api/auth/login` – Login y obtención del token JWT
- `/api/users/` – Listado de usuarios
- `/api/posts/` – Listado y gestión de posts
- `/api/health` – Verificación de estado del backend

## Integración con Frontend

Asegúrate de que el frontend apunte a la URL adecuada del backend (ejemplo: `VITE_API_URL=http://localhost:8000/api`).

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para discutir cambios o mejoras.

## Licencia

Este proyecto está bajo la licencia MIT.

```
