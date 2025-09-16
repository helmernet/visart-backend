# find_duplicates.py
import sys
sys.path.insert(0, '.')

from main import app

print("🔍 BUSCANDO FUENTE DE DUPLICADOS...")

# Buscar todos los routers que están siendo incluidos
for route in app.routes:
    if hasattr(route, 'path') and 'users/users' in route.path:
        print(f"❌ RUTA DUPLICADA: {route.path}")
        print(f"   Métodos: {list(route.methods)}")
        if hasattr(route, 'endpoint'):
            print(f"   Endpoint: {route.endpoint}")
        print("---")

print("\n📋 LISTA COMPLETA DE RUTAS:")
for i, route in enumerate(app.routes):
    if hasattr(route, 'path'):
        print(f"{i:2d}. {route.path}")