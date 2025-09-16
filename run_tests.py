# run_tests.py
import subprocess
import sys

def run_tests():
    """Ejecutar todas las pruebas de integración y regresión"""
    print("🔧 Ejecutando pruebas de integración y regresión...")
    
    # Ejecutar pruebas con pytest
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "-v", 
        "--tb=short",
        "tests/test_integration.py",
        "tests/test_regression.py"
    ], capture_output=True, text=True)
    
    # Mostrar resultados
    print(result.stdout)
    if result.stderr:
        print("❌ Errores:", result.stderr)
    
    print(f"✅ Pruebas completadas. Código de salida: {result.returncode}")
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests())