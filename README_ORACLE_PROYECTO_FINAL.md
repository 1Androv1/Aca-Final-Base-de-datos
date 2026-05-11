# Proyecto final Oracle 18c XE + Django

## Tema elegido

Gestión académica de una institución educativa.

## Qué incluye

- Modelo relacional con estudiantes, docentes, cursos, matrículas y auditoría.
- Relaciones PK y FK.
- Tablespace y datafile.
- Roles y usuarios.
- Índices.
- Vistas.
- Secuencias.
- 10 registros por tabla principal.
- Consultas SELECT, JOIN, GROUP BY y ORDER BY.
- Procedimiento almacenado.
- Función.
- Trigger de auditoría.
- Simulación de política de respaldo.
- Proyecto Django conectado a Oracle.

## Usuario SYS

El usuario SYS se usa para crear la estructura inicial:

```bash
sqlplus sys/Oracle123@//localhost:1521/XEPDB1 as sysdba
```

Después se ejecuta:

```sql
@scripts/01_crear_base_oracle_academico.sql
```

## Usuario de la aplicación

La aplicación Django usa este usuario:

```text
Usuario: SISTEMA_ACADEMICO_APP
Contraseña: Academico123
Servicio: localhost:1521/XEPDB1
```

## Usuario restringido

Para demostrar seguridad y permisos restringidos:

```text
Usuario: SISTEMA_ACADEMICO_CONSULTA
Contraseña: Consulta123
```

Este usuario solo puede consultar las vistas autorizadas.

## Ejecutar Django

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Archivos principales modificados

- `django_pytest_tutorial/settings.py`
- `myuser/models.py`
- `myuser/admin.py`
- `myuser/views.py`
- `myuser/urls.py`
- `templates/base.html`
- `templates/myuser/home.html`
- `requirements.txt`
- `scripts/01_crear_base_oracle_academico.sql`
- `scripts/02_comandos_django.txt`
