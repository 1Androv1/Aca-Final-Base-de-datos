# Reportes de Pruebas Unitarias - Django Pytest Tutorial

## 📊 Ubicación de Reportes

Los reportes de pruebas se guardan en la carpeta `reports/` del proyecto:

```
django_pytest_tutorial/
└── reports/
    ├── test_report.html          # Reporte principal de pruebas
    └── coverage/
        └── index.html            # Reporte de cobertura de código
```

## 🎯 Cómo Acceder a los Reportes

### 1. Reporte de Pruebas (`test_report.html`)
- Abre: `reports/test_report.html` en un navegador
- Muestra: Resultado de cada test (PASSED/FAILED), duración, errores
- Interactivo: Puedes filtrar y buscar dentro del HTML

### 2. Reporte de Cobertura (`coverage/index.html`)
- Abre: `reports/coverage/index.html` en un navegador
- Muestra: Porcentaje de líneas cubiertas, módulos, detalles por archivo
- Interactivo: Clickea en archivos para ver líneas cubiertas/no cubiertas

## 🚀 Comando para Generar Reportes

Ejecuta desde la raíz del proyecto:

```bash
python -m pytest myuser/tests/test_views.py --html=reports/test_report.html --self-contained-html --cov=myuser --cov-report=html:reports/coverage -v
```

O usa el alias simplificado:

```bash
pytest
```

(Usa la configuración de `pytest.ini` que ya está en el proyecto)

## 📋 Últimas Pruebas Ejecutadas

### Fecha: 09/05/2026

#### Resumen:
- **Total de pruebas**: 12
- **Passed**: 12 ✅
- **Failed**: 0
- **Cobertura**: 90%

#### Tests ejecutados:
1. ✅ test_render_views[home] - Renderiza página de inicio
2. ✅ test_render_views[user_signup] - Renderiza formulario de registro
3. ✅ test_render_views[user_login] - Renderiza formulario de login
4. ✅ test_user_signup - Usuario se registra correctamente
5. ✅ test_user_login - Usuario inicia sesión correctamente
6. ✅ test_user_login_invalid_password - Rechaza contraseña incorrecta
7. ✅ test_user_logout - Usuario cierra sesión
8. ✅ test_first_user_is_admin - Primer usuario es administrador
9. ✅ test_second_user_is_not_admin - Segundo usuario NO es admin
10. ✅ test_user_update - Usuario puede actualizar perfil
11. ✅ test_admin_can_delete_user - Admin puede eliminar usuarios
12. ✅ test_non_admin_cannot_delete_user - Usuario común NO puede eliminar

## 🔐 Funcionalidades Probadas

### Autenticación
- ✅ Registro de usuarios
- ✅ Validación de credenciales
- ✅ Cierre de sesión

### Autorización
- ✅ Primer usuario = administrador automático
- ✅ Solo admin puede eliminar usuarios
- ✅ Usuario común solo actualiza su perfil

### Permisos
- ✅ Acceso a endpoints requiere login
- ✅ Operaciones destructivas requieren permisos admin

## 📈 Cobertura de Código

| Módulo | Cobertura |
|--------|-----------|
| models.py | 100% |
| views.py | 87% |
| urls.py | 100% |
| migrations | 80% |
| **TOTAL** | **90%** |

## 🔄 Cómo Ejecutar Manualmente

```bash
# Desde la raíz del proyecto
cd c:\Users\andro\OneDrive\Documentos\PruebasUnitarias\django_pytest_tutorial

# Opción 1: Con reportes HTML
python -m pytest -v --html=reports/test_report.html --self-contained-html

# Opción 2: Solo en terminal
python -m pytest -v

# Opción 3: Con cobertura detallada
python -m pytest --cov=myuser --cov-report=term-missing

# Opción 4: Un test específico
python -m pytest myuser/tests/test_views.py::test_first_user_is_admin -v
```

## 📝 Notas

- Los reportes se regeneran cada vez que ejecutas pytest
- El archivo `test_report.html` es autónomo (no requiere servidor web)
- Los reportes mantienen historial en la carpeta `reports/`
- La cobertura se actualiza automáticamente con cada ejecución
