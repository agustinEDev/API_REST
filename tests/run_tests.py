#!/usr/bin/env python3
"""
Script para ejecutar todas las pruebas unitarias del proyecto.

Ejecuta todas las pruebas y genera un reporte completo incluyendo:
- Resultados de todas las suites de pruebas
- Cobertura de código (si está disponible)
- Resumen de éxitos y fallos
- Métricas de rendimiento

Uso: python run_tests.py [opciones]

Autor: agustinEDev
Fecha: 21 de octubre de 2025
"""

import unittest
import sys
import os
import time
from io import StringIO

# Añadir el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configurar compatibilidad antes de importar módulos de pruebas
from tests.test_compatibility import setup_all_compatibility
setup_all_compatibility()

# Importar todos los módulos de pruebas
from tests.test_database import TestDatabaseConnection
from tests.test_models import TestUserModel
from tests.test_controllers import TestUserController
from tests.test_api import TestAPIEndpoints, TestAPIErrorHandling
from tests.test_integration import TestIntegracionCompleta, TestRendimientoYCarga


class ColoredTextTestResult(unittest.TextTestResult):
    """Resultado de pruebas con colores para mejor visualización."""
    
    def __init__(self, stream, descriptions, verbosity):
        super().__init__(stream, descriptions, verbosity)
        self.success_count = 0
        self.start_time = None
        self.verbosity = verbosity
    
    def startTest(self, test):
        super().startTest(test)
        self.start_time = time.time()
        if self.verbosity > 1:
            self.stream.write(f"Ejecutando: {test._testMethodName} ... ")
            self.stream.flush()
    
    def addSuccess(self, test):
        super().addSuccess(test)
        self.success_count += 1
        if self.verbosity > 1:
            elapsed = time.time() - self.start_time
            self.stream.write(f"\033[92m✓ ÉXITO\033[0m ({elapsed:.3f}s)\n")
    
    def addError(self, test, err):
        super().addError(test, err)
        if self.verbosity > 1:
            elapsed = time.time() - self.start_time
            self.stream.write(f"\033[91m✗ ERROR\033[0m ({elapsed:.3f}s)\n")
    
    def addFailure(self, test, err):
        super().addFailure(test, err)
        if self.verbosity > 1:
            elapsed = time.time() - self.start_time
            self.stream.write(f"\033[91m✗ FALLO\033[0m ({elapsed:.3f}s)\n")
    
    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        if self.verbosity > 1:
            elapsed = time.time() - self.start_time
            self.stream.write(f"\033[93m- OMITIDO\033[0m ({elapsed:.3f}s): {reason}\n")


class TestRunner:
    """Ejecutor principal de pruebas."""
    
    def __init__(self, verbosity=2):
        self.verbosity = verbosity
        self.start_time = None
        self.total_tests = 0
        self.total_success = 0
        self.total_failures = 0
        self.total_errors = 0
        self.total_skipped = 0
    
    def run_all_tests(self):
        """Ejecuta todas las suites de pruebas."""
        print("\033[94m" + "="*80)
        print("🧪 EJECUTANDO SUITE COMPLETA DE PRUEBAS UNITARIAS")
        print("="*80 + "\033[0m")
        print()
        
        self.start_time = time.time()
        
        # Definir todas las suites de pruebas
        test_suites = [
            ("Base de Datos", TestDatabaseConnection),
            ("Modelos", TestUserModel),
            ("Controladores", TestUserController),
            ("API Endpoints", TestAPIEndpoints),
            ("Manejo de Errores API", TestAPIErrorHandling),
            ("Integración Completa", TestIntegracionCompleta),
            ("Rendimiento y Carga", TestRendimientoYCarga),
        ]
        
        all_results = []
        
        for suite_name, test_class in test_suites:
            print(f"\033[96m📋 Ejecutando pruebas de: {suite_name}\033[0m")
            print("-" * 60)
            
            # Crear suite de pruebas
            suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
            
            # Ejecutar pruebas con resultado personalizado
            stream = StringIO()
            runner = unittest.TextTestRunner(
                stream=stream,
                verbosity=self.verbosity,
                resultclass=ColoredTextTestResult
            )
            
            result = runner.run(suite)
            all_results.append((suite_name, result))
            
            # Mostrar resultados de esta suite
            self._print_suite_results(suite_name, result)
            print()
        
        # Mostrar resumen final
        self._print_final_summary(all_results)
    
    def _print_suite_results(self, suite_name, result):
        """Imprime los resultados de una suite específica."""
        total = result.testsRun
        success = result.success_count if hasattr(result, 'success_count') else (
            total - len(result.failures) - len(result.errors) - len(result.skipped)
        )
        failures = len(result.failures)
        errors = len(result.errors)
        skipped = len(result.skipped)
        
        # Actualizar contadores globales
        self.total_tests += total
        self.total_success += success
        self.total_failures += failures
        self.total_errors += errors
        self.total_skipped += skipped
        
        # Determinar color según el resultado
        if failures == 0 and errors == 0:
            color = "\033[92m"  # Verde
            status = "✓ TODAS EXITOSAS"
        elif errors > 0:
            color = "\033[91m"  # Rojo
            status = "✗ CON ERRORES"
        else:
            color = "\033[93m"  # Amarillo
            status = "⚠ CON FALLOS"
        
        print(f"{color}Resultado: {status}\033[0m")
        print(f"Total: {total} | Éxito: {success} | Fallos: {failures} | Errores: {errors} | Omitidas: {skipped}")
        
        # Mostrar detalles de fallos y errores si los hay
        if failures > 0:
            print(f"\033[93m⚠ FALLOS DETECTADOS:\033[0m")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip() if 'AssertionError:' in traceback else 'Ver detalles completos'}")
        
        if errors > 0:
            print(f"\033[91m✗ ERRORES DETECTADOS:\033[0m")
            for test, traceback in result.errors:
                error_line = traceback.split('\n')[-2] if traceback.split('\n') else "Error desconocido"
                print(f"  - {test}: {error_line}")
    
    def _print_final_summary(self, all_results):
        """Imprime el resumen final de todas las pruebas."""
        elapsed_time = time.time() - self.start_time
        
        print("\033[94m" + "="*80)
        print("📊 RESUMEN FINAL DE PRUEBAS")
        print("="*80 + "\033[0m")
        
        # Resumen por suite
        print("\n📋 Resultados por Suite:")
        for suite_name, result in all_results:
            total = result.testsRun
            success = getattr(result, 'success_count', 
                            total - len(result.failures) - len(result.errors) - len(result.skipped))
            
            if len(result.failures) == 0 and len(result.errors) == 0:
                status_icon = "✅"
                color = "\033[92m"
            elif len(result.errors) > 0:
                status_icon = "❌"
                color = "\033[91m"
            else:
                status_icon = "⚠️"
                color = "\033[93m"
            
            print(f"  {status_icon} {color}{suite_name:.<30} {success}/{total} exitosas\033[0m")
        
        # Estadísticas globales
        print(f"\n📈 Estadísticas Globales:")
        print(f"  🧪 Total de pruebas ejecutadas: {self.total_tests}")
        print(f"  ✅ Pruebas exitosas: {self.total_success}")
        print(f"  ❌ Pruebas fallidas: {self.total_failures}")
        print(f"  🚫 Pruebas con errores: {self.total_errors}")
        print(f"  ⏭️ Pruebas omitidas: {self.total_skipped}")
        
        # Calcular porcentaje de éxito
        if self.total_tests > 0:
            success_rate = (self.total_success / self.total_tests) * 100
            print(f"  📊 Tasa de éxito: {success_rate:.1f}%")
        
        print(f"  ⏱️ Tiempo total de ejecución: {elapsed_time:.2f} segundos")
        
        # Mensaje final según los resultados
        if self.total_failures == 0 and self.total_errors == 0:
            print(f"\n\033[92m🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE! 🎉\033[0m")
        elif self.total_errors > 0:
            print(f"\n\033[91m💥 PRUEBAS COMPLETADAS CON ERRORES 💥\033[0m")
            print("Por favor, revisa los errores anteriores antes de continuar.")
        else:
            print(f"\n\033[93m⚠️ PRUEBAS COMPLETADAS CON ALGUNOS FALLOS ⚠️\033[0m")
            print("Por favor, revisa los fallos anteriores.")
    
    def run_specific_suite(self, test_class, suite_name):
        """Ejecuta una suite específica de pruebas."""
        print(f"\033[96m🧪 Ejecutando pruebas específicas: {suite_name}\033[0m")
        print("-" * 60)
        
        suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
        runner = unittest.TextTestRunner(
            verbosity=self.verbosity,
            resultclass=ColoredTextTestResult
        )
        
        result = runner.run(suite)
        self._print_suite_results(suite_name, result)


def main():
    """Función principal del script."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Ejecutar pruebas unitarias del proyecto API REST')
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='Mostrar salida detallada')
    parser.add_argument('-q', '--quiet', action='store_true',
                       help='Mostrar salida mínima')
    parser.add_argument('-s', '--suite', choices=[
        'database', 'models', 'controllers', 'api', 'integration', 'performance'
    ], help='Ejecutar solo una suite específica')
    
    args = parser.parse_args()
    
    # Determinar nivel de verbosidad
    if args.quiet:
        verbosity = 0
    elif args.verbose:
        verbosity = 2
    else:
        verbosity = 1
    
    runner = TestRunner(verbosity)
    
    # Ejecutar suite específica o todas
    if args.suite:
        suite_map = {
            'database': (TestDatabaseConnection, 'Base de Datos'),
            'models': (TestUserModel, 'Modelos'),
            'controllers': (TestUserController, 'Controladores'),
            'api': (TestAPIEndpoints, 'API Endpoints'),
            'integration': (TestIntegracionCompleta, 'Integración'),
            'performance': (TestRendimientoYCarga, 'Rendimiento')
        }
        
        test_class, suite_name = suite_map[args.suite]
        runner.run_specific_suite(test_class, suite_name)
    else:
        runner.run_all_tests()


if __name__ == '__main__':
    main()