#!/usr/bin/env python
"""Script para ejecutar pruebas y generar reportes automáticamente."""

import subprocess
import sys
from pathlib import Path

def run_tests():
    """Ejecuta pytest con generación de reportes HTML y cobertura."""
    project_root = Path(__file__).parent
    reports_dir = project_root / 'reports'
    reports_dir.mkdir(exist_ok=True)
    
    cmd = [
        sys.executable, '-m', 'pytest',
        'myuser/tests/test_views.py',
        f'--html={reports_dir}/test_report.html',
        '--self-contained-html',
        f'--cov=myuser',
        f'--cov-report=html:{reports_dir}/coverage',
        f'--cov-report=term-missing',
        '-v'
    ]
    
    print(f"📊 Ejecutando pruebas unitarias...")
    print(f"📁 Reportes guardados en: {reports_dir}/")
    print(f"🔗 Abre 'reports/test_report.html' para ver resultados\n")
    
    result = subprocess.run(cmd, cwd=project_root)
    
    if result.returncode == 0:
        print("\n✅ Todas las pruebas pasaron correctamente!")
        print(f"📄 Reporte HTML: {reports_dir}/test_report.html")
        print(f"📊 Cobertura: {reports_dir}/coverage/index.html")
    else:
        print("\n❌ Algunas pruebas fallaron!")
        sys.exit(1)

if __name__ == '__main__':
    run_tests()
