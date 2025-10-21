#!/usr/bin/env python3
"""
Script de desarrollo para el proyecto API REST.

Este script automatiza tareas comunes de desarrollo incluyendo:
- Limpieza de archivos temporales
- Instalación/actualización de dependencias
- Ejecución de pruebas unitarias
- Validación de código
- Preparación para deployment

Modos disponibles:
- dev: Modo desarrollo completo (limpia + instala + tests)
- test: Solo ejecuta las pruebas unitarias
- clean: Solo limpia archivos temporales
- install: Solo instala/actualiza dependencias
- lint: Solo validación de código

Uso: python scripts/dev.py [modo]

Autor: agustinEDev
Fecha: 21 de octubre de 2025
"""

import sys
import os
import subprocess
import shutil
import argparse
from pathlib import Path


class DevScript:
    """Clase principal para el script de desarrollo."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.venv_paths = [
            self.project_root / ".venv",
            self.project_root / "venv", 
            self.project_root / ".my_venv"
        ]
        self.python_cmd = self._get_python_command()
        
    def _get_python_command(self):
        """Determina el comando Python a usar."""
        # Verificar si ya estamos en un entorno virtual activo
        if os.environ.get('VIRTUAL_ENV'):
            venv_python = Path(os.environ['VIRTUAL_ENV']) / "bin" / "python"
            if venv_python.exists():
                print(f"🐍 Usando entorno virtual activo: {os.environ['VIRTUAL_ENV']}")
                return str(venv_python)
        
        # Buscar en entornos virtuales del proyecto
        for venv_path in self.venv_paths:
            if venv_path.exists():
                python_exe = venv_path / "bin" / "python"
                if python_exe.exists():
                    print(f"🐍 Encontrado entorno virtual: {venv_path}")
                    return str(python_exe)
        
        # Usar Python del sistema como fallback
        if shutil.which("python3"):
            print("⚠️  Usando Python3 del sistema (no hay entorno virtual)")
            return "python3"
        elif shutil.which("python"):
            print("⚠️  Usando Python del sistema (no hay entorno virtual)")
            return "python"
        else:
            raise RuntimeError("❌ Python no encontrado en el sistema")
    
    def _run_command(self, cmd, description, cwd=None, check=True):
        """Ejecuta un comando y maneja errores."""
        print(f"▶️  {description}...")
        
        if cwd is None:
            cwd = self.project_root
            
        try:
            if isinstance(cmd, str):
                result = subprocess.run(
                    cmd, shell=True, cwd=cwd, check=check,
                    capture_output=False, text=True
                )
            else:
                result = subprocess.run(
                    cmd, cwd=cwd, check=check,
                    capture_output=False, text=True
                )
            
            if result.returncode == 0:
                print(f"✅ {description} completado exitosamente")
            return result.returncode == 0
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error en {description}: {e}")
            return False
        except Exception as e:
            print(f"❌ Error inesperado en {description}: {e}")
            return False
    
    def clean(self):
        """Limpia archivos temporales y cache.""" 
        print("\n🧹 Iniciando limpieza de archivos temporales...")
        
        # Directorios a excluir de la limpieza (entornos virtuales)
        exclude_dirs = {'.venv', 'venv', '.my_venv', 'env', '.env_dir'}
        
        # Patrones de archivos/directorios a limpiar (solo en código del proyecto)
        patterns_to_clean = [
            "__pycache__",
            "*.pyc", 
            "*.pyo",
            "*.pyd",
            ".pytest_cache",
            ".coverage",
            "htmlcov",
            "*.egg-info",
            "build",
            "dist",
            ".mypy_cache",
            ".tox"
        ]
        
        cleaned_count = 0
        
        # Limpiar solo en directorios del proyecto (excluyendo entornos virtuales)
        for item in self.project_root.iterdir():
            if item.name in exclude_dirs:
                continue  # Saltar entornos virtuales
                
            if item.is_dir():
                # Buscar patrones en subdirectorios del proyecto
                for pattern in patterns_to_clean:
                    for path in item.glob(f"**/{pattern}"):
                        try:
                            # Verificar que no esté dentro de un entorno virtual
                            path_parts = path.parts
                            if any(part in exclude_dirs for part in path_parts):
                                continue
                                
                            if path.is_file():
                                path.unlink()
                                cleaned_count += 1
                                print(f"🗑️  Eliminado archivo: {path.relative_to(self.project_root)}")
                            elif path.is_dir():
                                shutil.rmtree(path)
                                cleaned_count += 1
                                print(f"🗑️  Eliminado directorio: {path.relative_to(self.project_root)}")
                        except Exception as e:
                            print(f"⚠️  No se pudo eliminar {path}: {e}")
            
            # También buscar archivos en el nivel raíz
            for pattern in patterns_to_clean:
                for path in self.project_root.glob(pattern):
                    try:
                        if path.name in exclude_dirs:
                            continue
                            
                        if path.is_file():
                            path.unlink()
                            cleaned_count += 1
                            print(f"🗑️  Eliminado archivo: {path.relative_to(self.project_root)}")
                        elif path.is_dir():
                            shutil.rmtree(path)
                            cleaned_count += 1
                            print(f"🗑️  Eliminado directorio: {path.relative_to(self.project_root)}")
                    except Exception as e:
                        print(f"⚠️  No se pudo eliminar {path}: {e}")
        
        print(f"✅ Limpieza completada - {cleaned_count} elementos eliminados")
        return True
    
    def install_dependencies(self):
        """Instala o actualiza las dependencias."""
        print("\n📦 Instalando/actualizando dependencias...")
        
        # Verificar que estamos en un entorno virtual
        if not os.environ.get('VIRTUAL_ENV') and not any(p.exists() for p in self.venv_paths):
            print("⚠️  ¡ADVERTENCIA! No se detectó un entorno virtual activo")
            print("   Se recomienda activar un entorno virtual antes de instalar dependencias")
            print("   ¿Continuar de todas formas? (y/N)")
            # En modo automatizado, continuamos sin preguntar
        
        requirements_file = self.project_root / "requirements.txt"
        
        if not requirements_file.exists():
            print("⚠️  Archivo requirements.txt no encontrado")
            return True
        
        print(f"📄 Usando archivo: {requirements_file}")
        print(f"🐍 Python ejecutable: {self.python_cmd}")
            
        # Actualizar pip primero
        success = self._run_command(
            f"{self.python_cmd} -m pip install --upgrade pip",
            "Actualizando pip"
        )
        
        if not success:
            return False
        
        # Instalar dependencias
        success = self._run_command(
            f"{self.python_cmd} -m pip install -r requirements.txt",
            "Instalando dependencias del proyecto"
        )
        
        return success
    
    def run_tests(self):
        """Ejecuta las pruebas unitarias."""
        print("\n🧪 Ejecutando pruebas unitarias...")
        
        # Verificar que existe el directorio de tests
        tests_dir = self.project_root / "tests"
        if not tests_dir.exists():
            print("❌ Directorio 'tests' no encontrado")
            return False
        
        # Ejecutar el script de pruebas personalizado
        test_runner = tests_dir / "run_tests.py"
        if test_runner.exists():
            success = self._run_command(
                f"{self.python_cmd} tests/run_tests.py",
                "Ejecutando suite completa de pruebas"
            )
        else:
            # Fallback a unittest discovery
            success = self._run_command(
                f"{self.python_cmd} -m unittest discover -s tests -p 'test_*.py' -v",
                "Ejecutando pruebas con unittest discovery"
            )
        
        return success
    
    def lint_code(self):
        """Ejecuta validación de código."""
        print("\n🔍 Ejecutando validación de código...")
        
        # Verificar si hay archivos Python para analizar
        python_files = list(self.project_root.glob("**/*.py"))
        if not python_files:
            print("⚠️  No se encontraron archivos Python para analizar")
            return True
        
        print(f"📄 Analizando {len(python_files)} archivos Python...")
        
        # Validación básica de sintaxis
        for py_file in python_files:
            if any(part.startswith('.') for part in py_file.parts):
                continue  # Saltar archivos/directorios ocultos
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    compile(f.read(), py_file, 'exec')
            except SyntaxError as e:
                print(f"❌ Error de sintaxis en {py_file}: {e}")
                return False
            except Exception as e:
                print(f"⚠️  No se pudo validar {py_file}: {e}")
        
        print("✅ Validación de sintaxis completada")
        return True
    
    def dev_mode(self):
        """Ejecuta el modo desarrollo completo."""
        print("🛠️  Iniciando modo desarrollo completo...")
        print("=" * 60)
        
        steps = [
            ("Limpieza", self.clean),
            ("Instalación de dependencias", self.install_dependencies), 
            ("Validación de código", self.lint_code),
            ("Pruebas unitarias", self.run_tests)
        ]
        
        for step_name, step_func in steps:
            print(f"\n📋 Paso: {step_name}")
            print("-" * 40)
            
            success = step_func()
            if not success:
                print(f"❌ Error en el paso: {step_name}")
                print(f"❌ Modo desarrollo fallido")
                return False
                
        print("\n" + "=" * 60)
        print("🎉 ¡Modo desarrollo completado exitosamente!")
        print("✅ El proyecto está listo para commit/push")
        return True
    
    def show_help(self):
        """Muestra la ayuda del script."""
        print("""
🛠️  Script de Desarrollo - API REST Project

Modos disponibles:
    dev     - Modo desarrollo completo (limpia + instala + lint + tests)
    test    - Solo ejecuta las pruebas unitarias  
    clean   - Solo limpia archivos temporales
    install - Solo instala/actualiza dependencias
    lint    - Solo validación de código
    help    - Muestra esta ayuda

Ejemplos:
    python scripts/dev.py dev      # Modo completo
    python scripts/dev.py test     # Solo tests
    python scripts/dev.py clean    # Solo limpieza

Configuración detectada:
    📁 Directorio raíz: {root}
    🐍 Python comando: {python}
    📦 Entorno virtual activo: {active_venv}
    📦 Entornos disponibles: {available_venvs}

Para uso con Warp workflows:
    wf-dev-push-unitest   # Ejecuta 'dev' antes del push

Recomendación:
    Ejecuta desde un entorno virtual activado:
    source .venv/bin/activate && python scripts/dev.py dev
""".format(
            root=self.project_root,
            python=self.python_cmd,
            active_venv=os.environ.get('VIRTUAL_ENV', 'Ninguno'),
            available_venvs=", ".join([p.name for p in self.venv_paths if p.exists()]) or "Ninguno encontrado"
        ))


def main():
    """Función principal del script."""
    parser = argparse.ArgumentParser(
        description='Script de desarrollo para API REST',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'mode',
        nargs='?',
        default='help',
        choices=['dev', 'test', 'clean', 'install', 'lint', 'help'],
        help='Modo de ejecución'
    )
    
    args = parser.parse_args()
    
    try:
        dev_script = DevScript()
        
        if args.mode == 'help':
            dev_script.show_help()
        elif args.mode == 'dev':
            success = dev_script.dev_mode()
            sys.exit(0 if success else 1)
        elif args.mode == 'test':
            success = dev_script.run_tests()
            sys.exit(0 if success else 1)
        elif args.mode == 'clean':
            success = dev_script.clean()
            sys.exit(0 if success else 1)
        elif args.mode == 'install':
            success = dev_script.install_dependencies()
            sys.exit(0 if success else 1)
        elif args.mode == 'lint':
            success = dev_script.lint_code()
            sys.exit(0 if success else 1)
            
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()