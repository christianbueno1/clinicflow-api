# ClinicFlow — Actualización del roadmap

**Fecha:** 30 de septiembre de 2026  
**Rama de trabajo:** `feat/task-5-patient-model`  
**Estado:** Tarea 5 en progreso

## Resumen

Se completaron los primeros hitos técnicos de la Tarea 5, orientada a definir e implementar el modelo ORM `Patient`. La base declarativa de SQLAlchemy está creada, Ruff quedó configurado como dependencia de desarrollo y el modelo de paciente fue implementado y validado estructuralmente.

## Cambios aplicados

### 1. Base declarativa y calidad de código

- Creado `src/clinicflow_api/models/base.py` con una clase `Base` que hereda de `sqlalchemy.orm.DeclarativeBase`.
- Creado el paquete `src/clinicflow_api/models/`.
- Añadido Ruff como dependencia de desarrollo en `pyproject.toml`.
- Actualizado `uv.lock` para registrar la dependencia.
- Verificados los comandos `ruff check` y `ruff format --check`.

**Commit:** `c8ef3d7 feat(db): add declarative base`

### 2. Modelo ORM Patient

Se implementó el modelo `Patient` en `src/clinicflow_api/models/patient.py` y se registró desde `models/__init__.py`.

| Campo | Tipo / configuración | Nulable |
|---|---|---|
| `id` | UUID, clave primaria, generado con `uuid4` | No |
| `first_name` | `String(100)` | No |
| `last_name` | `String(100)` | No |
| `date_of_birth` | `Date` | No |
| `phone` | `String(30)` | No |
| `identification_number` | `String(50)`, único | No |
| `email` | `String(254)`, único | Sí |
| `address` | `Text` | Sí |
| `created_at` | `DateTime(timezone=True)`, `server_default=func.now()` | No |
| `updated_at` | `DateTime(timezone=True)`, `server_default=func.now()` y `onupdate=func.now()` | No |
| `deleted_at` | `DateTime(timezone=True)` | Sí |

Las restricciones de unicidad de identificación y correo son globales, incluso para pacientes eliminados lógicamente. El correo es opcional; PostgreSQL permite múltiples valores `NULL` en una restricción `UNIQUE` convencional.

### 3. Normalización acordada e implementada

- Nombres y teléfono: eliminar espacios al inicio y al final.
- Número de identificación: eliminar espacios externos y convertir a mayúsculas.
- Correo: eliminar espacios externos y convertir a minúsculas.
- La normalización se implementa con validadores ORM (`@validates`). La validación formal de entradas queda para una capa posterior.

## Verificaciones realizadas

- Ruff: `All checks passed!`
- Ruff formatter: `3 files already formatted`.
- Metadata SQLAlchemy: se confirmó el registro de la tabla `patients`.
- Columnas: se verificaron las 11 columnas, sus tipos y nulabilidad.
- Restricciones únicas: se confirmaron para `identification_number` y `email`.

## Estado del roadmap

| Hito | Estado |
|---|---|
| Crear base declarativa de SQLAlchemy | Completado |
| Incorporar Ruff como herramienta de desarrollo | Completado |
| Implementar modelo ORM `Patient` | Implementado y validado estructuralmente |
| Confirmar metadata y restricciones | Completado |
| Crear pruebas automatizadas del modelo | Pendiente |
| Ejecutar pruebas de comportamiento y normalización | Pendiente |
| Revisar y registrar el commit del modelo | Pendiente de confirmar en el historial |
| Integrar la rama de la Tarea 5 en `dev` | Pendiente |
| Promover `dev` a `main` tras validación | Pendiente |

## Próximas actividades

1. Añadir pruebas automatizadas para normalización, UUID, valores opcionales y restricciones.
2. Ejecutar la suite de pruebas y corregir cualquier hallazgo.
3. Revisar los cambios y crear el commit del modelo `Patient`.
4. Completar la Tarea 5 y fusionar la rama a `dev` siguiendo el flujo Git del proyecto.
5. Promover `dev` a `main` cuando la integración esté validada.

## Fuera del alcance de este avance

Todavía no se implementaron endpoints CRUD, esquemas Pydantic, repositorios, servicios, migraciones Alembic, paginación, autenticación, citas ni expedientes médicos.
