# ClinicFlow — Stack tecnológico

> Estado: **borrador v0.1** (2026-09-29). Las versiones se verificaron en la web el 2026-09-29; al
> instalar, confirmar siempre la última con `uv add` / notas de versión.
>
> Leyenda: **[Decidido]** lo indicaste tú · **[Verificado]** dato revisado en la web · **[Por confirmar]** pendiente de tu decisión.

## 1. Entorno de desarrollo

| Tema | Decisión |
|---|---|
| Sistema operativo | **[Decidido]** Fedora 44 Workstation (Linux) |
| Ejecución | **[Decidido]** Solo local. La app corre en el host; **solo la base de datos corre en Podman** |
| Despliegue | **[Decidido]** Fuera de alcance por ahora |
| Versión de Python | **[Por confirmar]** Fedora 44 empaqueta Python 3.14 **[Verificado]**; propuesta: fijar la versión con uv |
| Idioma del código (nombres, endpoints, tablas) | **[Por confirmar]** inglés o español |

## 2. Aplicación

| Tema | Decisión |
|---|---|
| Framework | **[Decidido]** FastAPI, con `async` |
| Versión FastAPI | **[Verificado]** la última entrada que vi en las notas de versión es 0.141.1 (2026-07-29); puede haber una más nueva |
| Gestor de proyecto y paquetes | **[Decidido]** uv (`pyproject.toml` + `uv.lock`). La documentación de FastAPI ya usa proyectos uv por defecto **[Verificado]** |
| Validación y esquemas | **[Decidido]** Pydantic v2. FastAPI marcó como obsoleto el soporte de Pydantic v1 **[Verificado]**; Pydantic 2.13.x visto en abril 2026 |
| Configuración | **[Decidido]** variables de entorno; `.env.example` versionado, `.env` local (ignorado por git). Propuesta **[Por confirmar]**: `pydantic-settings` para leerlas |
| Documentación de la API | **[Decidido]** la que trae FastAPI por defecto (OpenAPI, Swagger UI, ReDoc) |
| Servidor de desarrollo | `fastapi dev` (FastAPI CLI) |

## 3. Datos

| Tema | Decisión |
|---|---|
| Base de datos | **[Decidido]** PostgreSQL en Podman. Última menor vista: 18.6 (ago 2026) **[Verificado]**; versión a fijar: **[Por confirmar]** |
| Orquestación local | **[Decidido]** red, pod, volumen y contenedor de Podman, automatizados con scripts de shell (`setup` y `teardown`) que usan variables |
| ORM | **[Decidido]** SQLAlchemy con modelos y sesión async |
| Versión SQLAlchemy | **[Por confirmar]** serie estable 2.0.x, o 2.1 (en RC: 2.1.0rc2 del 2026-09-08) **[Verificado]**. Nota: en 2.1 `greenlet` ya no viene por defecto; hay que instalar `sqlalchemy[asyncio]` |
| Driver async de PostgreSQL | **[Por confirmar]** `asyncpg` o `psycopg` 3 |
| Migraciones | **[Decidido]** Alembic (serie 1.18.x vista **[Verificado]**), con plantilla async |
| Separación de capas de datos | **[Decidido]** modelos (SQLAlchemy) distintos de esquemas (Pydantic) |

## 4. Seguridad (fase actual)

- **[Decidido]** Solo **validación de datos de entrada** con Pydantic.
- Diferido: autenticación, autorización por roles, límites de tasa, cabeceras, gestión de secretos avanzada.

## 5. Calidad y proceso (se introduce después de la primera entidad)

- **[Decidido]** Pruebas unitarias y de integración, CI/CD y hooks de git.
- **[Por confirmar]** Herramientas concretas (runner de pruebas, linter/formateador, verificador de tipos, plataforma de CI, gestor de hooks). Se decide en la fase correspondiente.

## 6. Diferido (solo explicado, no implementado)

Observabilidad y rendimiento: logs estructurados, métricas, trazas, health checks, caché y benchmarks.
Se retoma cuando exista algo que medir.

## 7. Regla de actualidad

Antes de empezar cada fase que toque un framework, se revisan sus novedades (notas de versión de
FastAPI, Pydantic, SQLAlchemy, Alembic, uv) y se aplican las prácticas vigentes. Si una novedad cambia
una decisión de este documento, se actualiza aquí y en el registro de decisiones.

## 8. Decisiones abiertas de arquitectura

- **[Por confirmar]** Patrones y arquitectura a practicar (por ejemplo: capas router → servicio → repositorio, patrón Repository, Unit of Work, inyección de dependencias, arquitectura hexagonal/limpia).
- **[Por confirmar]** Borrado físico o lógico (soft delete) de pacientes.
- **[Por confirmar]** Paginación y filtros en el listado, o listado simple.
