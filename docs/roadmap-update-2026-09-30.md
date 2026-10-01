# ClinicFlow — Propuesta de actualización del roadmap (v0.1 → v0.2)

> Fecha: 2026-09-30 · Rama: `feat/task-5-patient-model` · Base: `specs/roadmap.md` (borrador v0.1, 2026-09-29)
> Estado: **propuesta. Nada de esto se ha aplicado todavía a `specs/roadmap.md`.**

## 1. Cómo leer este documento

Cada punto lleva una etiqueta de origen para no confundir lo que decidiste con lo que se propuso:

- **[DECIDIDO]**: lo indicaste tú de forma explícita.
- **[PROPUESTA]**: sugerencia mía que aún no has confirmado.
- **[PENDIENTE]**: tema sin decidir.

---

## 2. Estado de las fases

| Bloque / fase | Estado | Evidencia |
|---|---|---|
| A (fases 1 a 4) | Completado | `7d24d42 merge: task 4 async database` en `main` y `dev` |
| 5. Modelo de Paciente y convenciones de nombres | **En curso** | Commits `c8ef3d7` (declarative base) y `5b099ff` (patient model) en la rama |
| 6 en adelante | Sin empezar | — |

**Falta para cerrar la fase 5:** convención de nombres en `Base`, ajustes al modelo (sección 3), los dos documentos y el PR hacia `dev`.

---

## 3. Decisiones tomadas

| # | Tema | Decisión | Estado |
|---|---|---|---|
| 1 | Estructura de directorios | Plana. Interpretación: sin subcarpetas por funcionalidad, módulos directamente bajo `clinicflow_api/` | [DECIDIDO]; interpretación por confirmar |
| 2 | Driver de PostgreSQL | `psycopg[binary]` | [DECIDIDO] |
| 3 | Identificador y marcas de tiempo | `id` UUID; `created_at` y `updated_at` | [DECIDIDO] |
| 4 | Tipo de borrado | Lógico (`deleted_at`) | [DECIDIDO] |
| 5 | Unicidad | Global en cédula y correo, también frente a pacientes con borrado lógico | [DECIDIDO] |
| 6 | Identificación | Cédula ecuatoriana. En Pydantic solo se valida que sean 10 dígitos (sin dígito verificador) | [DECIDIDO] |
| 7 | Campos obligatorios | Cédula, nombres, apellidos, fecha de nacimiento, teléfono y sexo (valores M/F) | [DECIDIDO] |
| 8 | Campos opcionales | Correo y dirección | [DECIDIDO] |
| 9 | Fecha de nacimiento no futura | Solo validación en Pydantic (sin restricción en BD) | [DECIDIDO] |
| 10 | Normalización | En el modelo y en Pydantic. Los validadores del modelo rechazan cadenas vacías en campos obligatorios | [DECIDIDO] |
| 11 | Contraseña en Alembic | Usar `render_as_string(hide_password=False)` para pasar la contraseña real | [DECIDIDO] como idea; refinamiento en la sección 6 |
| 12 | Configuración de la base | Pasar a una función (patrón factory) en `database.py`, pensando en el despliegue y en separar recursos | [DECIDIDO] en intención; momento por definir |
| 13 | `api_base_url` | Se mantiene en `Settings`, para uso futuro en el despliegue | [DECIDIDO] |
| 14 | Documentación de la fase | Dos archivos: guía de convenciones y registro de decisiones | [DECIDIDO]; nombres en la sección 6 |
| 15 | Ritmo | Revisar los demás temas progresivamente, a medida que crece el proyecto | [DECIDIDO] |

---

## 4. Cambios propuestos al roadmap, fase por fase

| Sección | Hoy dice | Propuesta | Origen |
|---|---|---|---|
| Encabezado | "borrador v0.1 (2026-09-29)" | "borrador v0.2 (2026-09-30)" | [PROPUESTA] |
| Fase 5 | "Modelo SQLAlchemy de Paciente y convenciones de nombres" · hecho cuando "el modelo existe y está documentado en la guía" | Explicitar que incluye `naming_convention` en `Base`, el campo `sex` y los dos documentos. Hecho cuando el modelo, las convenciones y las decisiones están documentadas | [PROPUESTA] a partir de las decisiones 7, 10 y 14 |
| Fase 6 (Alembic) | "Alembic (plantilla async) y primera migración" | Añadir a la fase: agregar `alembic` a las dependencias (hoy no está en `pyproject.toml`) y leer la URL desde `Settings`. Antes de empezarla, revisar novedades de SQLAlchemy 2.1, según el encabezado del roadmap | [PROPUESTA] |
| Fase 7 (Pydantic) | "Datos inválidos se rechazan con error 422 claro" | Concretar: cédula con patrón `^\d{10}$`, `sex` como enum M/F, fecha de nacimiento no futura, normalización de correo y cédula, correo y dirección opcionales | Derivado de las decisiones 6 a 10 |
| Fases 8 y 9 | Dependen de "arquitectura y patrones" | Se mantienen pendientes. Ya está decidida la estructura plana. Falta decidir dónde se hace `commit` | [PENDIENTE] |
| Fase 10 | "Listado, actualización y borrado" | `DELETE` pasa a ser borrado lógico (rellena `deleted_at`). Definir si los pacientes borrados aparecen en `GET` y en el listado, y la paginación | Decisión 4; el resto [PENDIENTE] |
| Fase 11 | "404, 409, 422" | El 409 debe cubrir el choque con pacientes con borrado lógico, porque la unicidad es global | Derivado de la decisión 5 |
| Fase 12 | Datos de ejemplo de *Dr. House* | Los datos deben cumplir las reglas: cédulas de 10 dígitos y sexo M/F | Derivado de las decisiones 6 y 7 |
| Bloque C | Pruebas en fases 13 a 16 | Sin cambios. La verificación de normalización y UUID se hace antes con el REPL o un script descartable | Roadmap original |
| "Cierre de cada fase" | "guía de convenciones y/o registro de decisiones *(por confirmar)*" | Quitar "(por confirmar)": son dos archivos | Decisión 14 |

---

## 5. Texto propuesto para `specs/roadmap.md`

Reemplazaría la sección **"Pendientes que afectan al roadmap"** por estas dos:

```markdown
## Decisiones tomadas

- Estructura plana; `psycopg[binary]`; id UUID; `created_at` y `updated_at`
- Borrado lógico (`deleted_at`); unicidad global de cédula y correo
  (un paciente borrado sigue bloqueándolos)
- Cédula ecuatoriana; en Pydantic solo se valida que tenga 10 dígitos
- Obligatorios: cédula, nombres, apellidos, fecha de nacimiento, teléfono, sexo (M/F)
- Opcionales: correo y dirección
- Fecha de nacimiento no futura: solo validación en Pydantic
- Normalización en modelo y en Pydantic; el modelo rechaza cadenas vacías
  en campos obligatorios
- Documentación por fase: guía de convenciones y registro de decisiones (dos archivos)

## Pendientes que afectan al roadmap

- Patrones de la capa de datos y lugar del `commit` (fases 8 y 9)
- Visibilidad de pacientes con borrado lógico en `GET` y listado, y paginación (fase 10)
- Herramientas de calidad y CI (Bloque C)
```

---

## 6. Propuestas técnicas por confirmar

| # | Propuesta | Motivo |
|---|---|---|
| 1 | Cédula como `String(10)` en lugar de `String(50)`, y quitar `.upper()` | La cédula son solo dígitos y aún no existe migración |
| 2 | `email` vacío (`""`) se convierte en `None` en lugar de rechazarse | Con `unique=True`, dos pacientes con `""` chocarían entre sí |
| 3 | `sex` como `StrEnum` con `Enum(native_enum=False, create_constraint=True)` | Evita el `ENUM` nativo de PostgreSQL y simplifica las migraciones |
| 4 | `naming_convention` en `Base`; el constraint de `sex` queda como `ck_patients_sex` | Parte de la fase 5 según el roadmap; los constraints hoy tienen nombre `None` |
| 5 | `eager_defaults` en el mapper (`__mapper_args__`), no en la sesión, y verificarlo con un script | `async_sessionmaker` no acepta esa opción; en async, leer `updated_at` tras un UPDATE puede lanzar `MissingGreenlet` |
| 6 | Alembic: no guardar la URL con contraseña en `alembic.ini`; fijarla en `env.py`, escapando `%` como `%%` si se usa `set_main_option`. En modo online, pasar el objeto `URL` a `create_async_engine`; reservar `render_as_string(hide_password=False)` para el modo offline | Evitar contraseñas en archivos versionados |
| 7 | Nombres: `docs/conventions.md` (modelo y convenciones) y `docs/decisions.md` (registro) | Hoy `docs/` ya contiene `draf-notes.md` |
| 8 | Hacer el refactor de `database.py` a factory en su propio commit, cuando Alembic o las pruebas lo necesiten | No pertenece a la fase 5 |

---

## 7. Fuera del roadmap (aviso)

- **Cambios sin commitear en `database.py`:** hay dos `print` de depuración que imprimen la contraseña real de la base en cada arranque, y la segunda línea usa `unicode_string()`, que no existe en el `URL` de SQLAlchemy y rompe la importación. Descartar con `git restore src/clinicflow_api/database.py`.
- **`eager_defaults`:** no está aplicado en ningún archivo mostrado.
- **`pyproject.toml`:** declara SQLAlchemy `>=2.1.1`; verificar el comportamiento en vez de asumir el de 2.0.

---

## 8. Orden para cerrar la fase 5

- [ ] Restaurar `database.py` (`git restore`)
- [ ] Commit: `feat(db): add constraint naming conventions` (`models/base.py`)
- [ ] Commit: ajustes de `patient.py` (validadores, `sex`, cédula, `eager_defaults`)
- [ ] Verificación en REPL o script: normalización, `None` en correo, UUID, nombres de constraints, `updated_at` tras UPDATE
- [ ] Crear `docs/conventions.md` y `docs/decisions.md`
- [ ] Aplicar los cambios de este documento a `specs/roadmap.md`
- [ ] PR hacia `dev`

---

## 9. Preguntas abiertas

1. ¿Se confirma `String(10)` para la cédula? (sección 6, punto 1)
2. ¿`email` vacío pasa a `None`? (sección 6, punto 2)
3. ¿Los pacientes con borrado lógico aparecen en `GET` por id y en el listado?
4. Paginación: tipo (offset/limit u otra) y tamaño por defecto.
5. ¿Dónde se hace `commit`: capa de lógica, capa de datos o la dependencia de sesión?
