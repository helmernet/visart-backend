# visart-backend

Repositorio para el backend del proyecto **Visart**.

## Descripción

Este proyecto contiene el backend desarrollado en Python para la aplicación Visart. Su objetivo es proveer servicios y API REST para la gestión de datos, autenticación de usuarios y funcionalidades relacionadas con la aplicación principal.

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

3. Instala las dependencias (agrega requirements.txt si existe):
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Inicia el servidor de desarrollo:
   ```bash
   python main.py
   ```

2. Accede a la API o servicios según la configuración de tu proyecto.

## Estructura del proyecto

- `main.py`: Archivo principal de ejecución.
- `app/`: Código fuente principal de la aplicación.
- `requirements.txt`: Dependencias del proyecto.
- `.env`: Variables de entorno (no debe subirse al repo).
- `.gitignore`: Archivos y carpetas ignoradas por Git.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para discutir cambios o mejoras.

## Licencia

Este proyecto está bajo la licencia MIT.
