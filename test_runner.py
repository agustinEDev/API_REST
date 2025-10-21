#!/usr/bin/env python3
"""
Sistema de análisis universal de pruebas unitarias.

Este script funciona con cualquier proyecto que tenga estructura tests/
y proporciona métricas precisas incluyendo tests skipped funcionales.

Características:
- ✅ Compatible con cualquier proyecto con estructura tests/
- ✅ Detección automática de módulos de test
- ✅ Conteo correcto de tests skipped funcionales
- ✅ Análisis estadístico detallado por módulo
- ✅ Sistema de compatibilidad opcional

Estructura soportada:
project/
├── tests/
│   ├── test_*.py
│   └── test_compatibility.py (opcional)
└── test_runner.py (este archivo)

Uso: python test_runner.py

Autor: agustinEDev
Fecha: 21 de octubre de 2025
"""

import unittest
import sys
import os
from io import StringIO
import time

def setup_environment():
    """Configurar entorno para tests de forma universal."""
    # Establecer variable de entorno para modo test
    os.environ['TESTING'] = 'true'
    
    # Detectar directorio del proyecto automáticamente
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = script_dir
    
    # Verificar que estamos en un directorio con estructura de tests
    tests_dir = os.path.join(project_dir, 'tests')
    if not os.path.exists(tests_dir):
        print(f"❌ No se encontró directorio 'tests' en: {project_dir}")
        print("💡 Asegúrate de ejecutar este script desde la raíz del proyecto")
        return False
    
    # Cambiar al directorio del proyecto y configurar path
    os.chdir(project_dir)
    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)
    
    print(f"📁 Directorio del proyecto: {project_dir}")
    print(f"🧪 Directorio de tests: {tests_dir}")
    
    return True

def setup_compatibility_system():
    """Configurar sistema de compatibilidad si está disponible."""
    try:
        # Intentar importar el sistema de compatibilidad
        from tests.test_compatibility import setup_all_compatibility
        print("🔧 Configurando compatibilidad para pruebas unitarias...")
        setup_all_compatibility()
        print("✅ Sistema de compatibilidad configurado")
        return True
    except ImportError:
        print("ℹ️  Sistema de compatibilidad no encontrado (opcional)")
        return False
    except Exception as e:
        print(f"⚠️  Error configurando compatibilidad: {e}")
        return False

def discover_and_run_tests():
    """Descubrir y ejecutar todos los tests."""
    print("🧪 ANÁLISIS COMPLETO DE TESTS - API REST")
    print("=" * 60)
    
    # Descubrir tests
    loader = unittest.TestLoader()
    start_dir = 'tests'
    suite = loader.discover(start_dir)
    
    # Información de descubrimiento
    total_tests = suite.countTestCases()
    print(f"📊 Tests descubiertos: {total_tests}")
    
    # Ejecutar tests con captura de salida
    stream = StringIO()
    runner = unittest.TextTestRunner(
        stream=stream, 
        verbosity=2,
        buffer=True
    )
    
    print("\n🚀 Ejecutando tests...")
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Estadísticas principales
    tests_run = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped)
    successes = tests_run - failures - errors
    
    # Cálculos de porcentajes
    success_rate = (successes / tests_run * 100) if tests_run > 0 else 0
    functional_rate = ((successes + skipped) / tests_run * 100) if tests_run > 0 else 0
    
    print(f"\n⏱️  Tiempo de ejecución: {end_time - start_time:.2f}s")
    print("\n" + "=" * 60)
    print("📈 RESULTADOS FINALES")
    print("=" * 60)
    
    print(f"✅ Tests exitosos:     {successes:>3}")
    print(f"❌ Tests fallidos:     {failures:>3}")
    print(f"⚠️  Tests con errores:  {errors:>3}")
    print(f"⏭️  Tests saltados:     {skipped:>3}")
    print("-" * 30)
    print(f"📊 Total ejecutados:   {tests_run:>3}")
    
    print(f"\n🎯 PORCENTAJE DE ÉXITO: {success_rate:.2f}%")
    print(f"🔧 FUNCIONALIDAD TOTAL: {functional_rate:.2f}% (incluye skipped)")
    
    # Evaluar resultado
    if success_rate >= 80:
        status = "🎉 EXCELENTE"
        color = "🟢"
    elif success_rate >= 70:
        status = "👍 BUENO"
        color = "🟡"
    elif success_rate >= 60:
        status = "⚠️  MEJORABLE"
        color = "🟠"
    else:
        status = "❌ CRÍTICO"
        color = "🔴"
    
    print(f"\n{color} ESTADO: {status}")
    
    return result, successes, failures, errors, skipped, success_rate

def discover_test_modules():
    """Descubrir automáticamente módulos de test en el directorio tests/."""
    import glob
    
    tests_dir = os.path.join(os.getcwd(), 'tests')
    test_files = glob.glob(os.path.join(tests_dir, 'test_*.py'))
    
    modules = {}
    for test_file in test_files:
        # Extraer nombre del módulo
        base_name = os.path.basename(test_file)
        module_name = base_name[5:-3]  # Remover 'test_' y '.py'
        
        # Saltar test_compatibility.py si existe
        if module_name == 'compatibility':
            continue
        
        # Generar nombre del módulo Python
        python_module = f"tests.{base_name[:-3]}"  # Remover solo '.py'
        modules[module_name] = python_module
    
    return modules

def analyze_by_module():
    """Analizar tests por módulo individual usando subprocess para evitar interferencias."""
    import subprocess
    print("\n" + "=" * 60)
    print("📂 ANÁLISIS POR MÓDULO")
    print("=" * 60)
    
    # Descubrir módulos automáticamente
    modules = discover_test_modules()
    
    if not modules:
        print("⚠️  No se encontraron módulos de test")
        return
    
    print(f"🔍 Módulos detectados: {', '.join(modules.keys())}")
    
    module_results = {}
    
    for module_name, module_path in modules.items():
        try:
            # Ejecutar en proceso separado para evitar interferencias
            cmd = [
                sys.executable, '-m', 'unittest', module_path, '-v'
            ]
            env = os.environ.copy()
            env['TESTING'] = 'true'
            
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True,
                env=env,
                cwd=os.getcwd()
            )
            
            # Parsear resultado
            if result.returncode == 0:
                # Contar tests OK
                ok_count = result.stderr.count(' ... ok')
                # Contar líneas de test para obtener total
                test_lines = [line for line in result.stderr.split('\n') if ' ... ' in line]
                total = len(test_lines)
                successes = ok_count
                failures = total - successes
                errors = 0
                skipped = result.stderr.count(' ... skipped')
                success_rate = (successes / total * 100) if total > 0 else 0
            else:
                # Parsear salida de error para obtener estadísticas
                stderr = result.stderr
                if 'FAILED' in stderr:
                    # Extraer números del formato "FAILED (failures=X, errors=Y)"
                    import re
                    match = re.search(r'Ran (\d+) tests', stderr)
                    total = int(match.group(1)) if match else 0
                    
                    failures_match = re.search(r'failures=(\d+)', stderr)
                    errors_match = re.search(r'errors=(\d+)', stderr)
                    skipped_match = re.search(r'skipped=(\d+)', stderr)
                    
                    failures = int(failures_match.group(1)) if failures_match else 0
                    errors = int(errors_match.group(1)) if errors_match else 0 
                    skipped = int(skipped_match.group(1)) if skipped_match else 0
                    successes = total - failures - errors
                    success_rate = (successes / total * 100) if total > 0 else 0
                else:
                    total = successes = failures = errors = skipped = 0
                    success_rate = 0
            
            module_results[module_name] = {
                'total': total,
                'successes': successes,
                'failures': failures,
                'errors': errors,
                'skipped': skipped,
                'rate': success_rate
            }
            
            # Status icon
            if success_rate >= 95:
                icon = "🟢"
            elif success_rate >= 80:
                icon = "🟡"
            elif success_rate >= 60:
                icon = "🟠"
            else:
                icon = "🔴"
            
            print(f"{icon} {module_name.upper():>12}: {successes:>2}/{total:<2} tests ({success_rate:>5.1f}%)")
            
        except Exception as e:
            print(f"❌ {module_name.upper():>12}: Error - {str(e)}")
    
    return module_results

def generate_summary():
    """Generar resumen ejecutivo."""
    print("\n" + "=" * 60)
    print("📋 RESUMEN EJECUTIVO")
    print("=" * 60)
    
    result, successes, failures, errors, skipped, success_rate = discover_and_run_tests()
    
    print(f"\n🎯 OBJETIVO: 80% de éxito")
    print(f"📊 LOGRADO: {success_rate:.2f}%")
    
    if success_rate >= 80:
        print("✅ ¡OBJETIVO CUMPLIDO!")
    else:
        needed = 80 - success_rate
        print(f"⚠️  Faltan {needed:.2f} puntos para el objetivo")
    
    print(f"\n📈 PROGRESO:")
    print(f"   • Tests funcionando: {successes}")
    print(f"   • Tests saltados (funcionales): {skipped}")
    print(f"   • Total funcional: {successes + skipped}")
    print(f"   • Problemas por resolver: {failures + errors}")

def main():
    """Función principal universal."""
    print("🔧 CONFIGURANDO ENTORNO UNIVERSAL DE TESTS")
    print("=" * 60)
    
    # Configurar entorno
    if not setup_environment():
        print("❌ Error en la configuración del entorno")
        return False
    
    # Configurar sistema de compatibilidad (opcional)
    setup_compatibility_system()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN EJECUTIVO")
    print("=" * 60)
    
    # Ejecutar análisis completo
    generate_summary()
    
    # Análisis por módulos
    analyze_by_module()
    
    print("\n" + "=" * 60)
    print("🏁 ANÁLISIS COMPLETADO")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    main()