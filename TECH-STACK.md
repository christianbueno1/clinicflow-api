# ClinicFlow — Stack tecnológico

> Estado: **v0.2** (2026-10-01). Fuente única de verdad del stack.
> Las versiones se verificaron en la web el 2026-09-29; al instalar, confirmar siempre la última con `uv add` / notas de versión.
>
> Leyenda: **[Decidido]** lo indicaste tú · **[Verificado]** dato revisado en la web.

## 1. Entorno de desarrollo

| Tema | Decisión |
|---|---|
| Sistema operativo | **[Decidido]** Fedora 44 Workstation (Linux) |
| Ejecución | **[Decidido]** Solo local. La app corre en el host; **solo la base de datos corre en Podman** |
| Despliegue | **[Decidido]** Fuera de alcance por ahora |
| Versión de Python | **[Decidido]** Python 3.14, fijada con uv (`.python-version`, `requires-python = ">=3.14"`) |
| Idioma del código (modelos, tablas, endpoints, variables) | **[Decidido]** Inglés |

## 2. Aplicación

| Tema | Decisión |
|---|---|
| Framework | **[Decidido]** FastAPI, con `async`. Instalado: `fastapi[standard]>=0.142.0` |
| Gestor de proyecto y paquetes | **[Decidido]** uv (`pyproject.toml` + `uv.lock`) |
| Validación y esquemas | **[Decidido]** Pydantic v2 vía FastAPI |
| Configuración | **[Decidido]** variables de entorno con `pydantic-settings` (`.env.example` versionado, `.env` ignorado por git) |
| Documentación de la API | **[Decidido]** la que trae FastAPI por defecto (OpenAPI, Swagger UI, ReDoc) |
| Servidor de desarrollo | `fastapi dev` (FastAPI CLI) |

## 3. Datos

| Tema | Decisión |
|---|---|
| Base de datos | **[Decidido]** PostgreSQL 18.6 en Podman (`docker.io/library/postgres:18.6-trixie`) |
| Orquestación local | **[Decidido]** red, pod, volumen y contenedor de Podman, automatizados con scripts de shell (`scripts/podman/setup-db.sh` y `teardown-db.sh`) |
| ORM | **[Decidido]** SQLAlchemy 2.1.x async (`sqlalchemy[asyncio]>=2.1.1`) con modelos y sesión async |
| Driver async de PostgreSQL | **[Decidido]** `psycopg` 3 (`psycopg[binary]>=3.3.6`, URL `postgresql+psycopg`) |
| Migraciones | **[Decidido]** Alembic (serie 1.18.x), con plantilla async |
| Separación de capas de datos | **[Decidido]** modelos (SQLAlchemy) distintos de esquemas (Pydantic) |

## 4. Seguridad (fase actual)

- **[Decidido]** Solo **validación de datos de entrada** con Pydantic.
- Excluido de v1: autenticación, autorización por roles. También diferido: límites de tasa, cabeceras, gestión de secretos avanzada.

## 5. Calidad y proceso

- **[Decidido]** Pruebas unitarias y de integración con `pytest` + `pytest-asyncio`, cobertura objetivo 80%.
- **[Decidido]** Lint y formato con `ruff`; verificación de tipos con `mypy`.
- **[Decidido]** CI/CD y hooks de git: se introducen después de la primera entidad, como fase propia.

## 6. Diferido (solo explicado, no implementado)

Observabilidad y rendimiento: logs estructurados, métricas, trazas, health checks, caché y benchmarks.
Se retoma cuando exista algo que medir.

## 7. Regla de actualidad

Antes de empezar cada fase que toque un framework, se revisan sus novedades (notas de versión de
FastAPI, Pydantic, SQLAlchemy, Alembic, uv) y se aplican las prácticas vigentes. Si una novedad cambia
una decisión de este documento, se actualiza aquí y en el registro de decisiones.

### Uso obligatorio de CLI tools

Toda configuración o scaffolding se genera **siempre con la CLI oficial** de la herramienta
correspondiente (`uv`, `alembic`, `podman`, `fastapi`, etc.; en otros proyectos: `ng`, `vite`, `pnpm`, `dotnet`...), nunca creando los archivos de configuración a mano desde memoria. Motivo: las CLIs emiten la estructura vigente según la versión instalada y evitan archivos desactualizados. Si una herramienta no tiene CLI para una configuración, se documenta la excepción y se genera a partir de la documentación oficial vigente.

## 8. Decisiones de arquitectura

- **[Decidido]** Arquitectura de capas simples: router → servicio → acceso a datos con la sesión async. Sin Repository ni Unit of Work por ahora; se reevalúa si la complejidad lo justifica.
- **[Decidido]** Borrado lógico (soft delete) de pacientes mediante `deleted_at`.
- **[Decidido]** Listado con paginación `limit`/`offset` y filtros (ver `SPECIFICATIONS.md`).
- **[Decidido]** Inyección de dependencias estándar de FastAPI (`Depends`) para sesión de BD y settings.
