# AGENTS.md — Agent Instructions

> Este archivo define cómo debe trabajar el agente dentro del proyecto.
> Es el punto de entrada operativo del agente y debe consultarse antes de
> realizar cambios relevantes en el proyecto.

---

## 1. Propósito de este archivo

`AGENTS.md` contiene las reglas de trabajo del agente dentro del repositorio.

No define el producto, la arquitectura ni las tecnologías del proyecto.

Su responsabilidad es establecer:

* cómo descubrir el contexto del proyecto;
* qué documentos consultar;
* qué responsabilidad tiene cada documento;
* cómo manejar información incompleta;
* cuándo preguntar al humano;
* cómo evolucionar la documentación;
* cómo organizar el trabajo;
* cómo mantener la trazabilidad;
* qué reglas seguir durante la implementación.

`AGENTS.md` debe considerarse un **contrato operativo entre el proyecto y el agente**.

---

# 2. Principio fundamental: no asumir

El agente debe **preguntar antes de asumir** cualquier información que pueda afectar:

* el propósito del proyecto;
* el alcance;
* los requisitos;
* los casos de uso;
* las reglas de negocio;
* las decisiones arquitectónicas;
* las tecnologías;
* las prioridades;
* el roadmap;
* las convenciones del proyecto.

El agente no debe convertir una práctica habitual, una preferencia personal o una solución técnicamente común en una decisión del proyecto sin aprobación del humano.

Cuando una decisión no esté definida:

1. identificar que la información falta;
2. determinar si es necesaria para continuar;
3. preguntar al humano si la decisión afecta el trabajo actual;
4. no inventar una respuesta para completar documentación.

---

# 3. Definición progresiva del proyecto

La documentación del proyecto debe evolucionar junto con el conocimiento disponible.

No es obligatorio crear todos los documentos al inicio.

El agente debe crear un documento únicamente cuando exista suficiente información para darle contenido significativo.

Por ejemplo, un proyecto nuevo puede comenzar únicamente con:

```text
AGENTS.md
MISSION.md
```

Posteriormente puede evolucionar a:

```text
AGENTS.md
MISSION.md
PRD.md
```

y posteriormente:

```text
AGENTS.md
MISSION.md
PRD.md
TECH-STACK.md
SPECIFICATIONS.md
ROADMAP.md
```

Los documentos no deben crearse simplemente para completar una estructura de directorios.

### Regla

> La documentación debe ser consecuencia del conocimiento del proyecto, no una plantilla que el agente rellena mediante suposiciones.

---

# 4. Entrevista inicial

Cuando el proyecto se encuentra en una etapa temprana y existe poca información disponible, el agente debe utilizar una **entrevista progresiva** para descubrir el contexto.

La entrevista debe comenzar por las cuestiones más fundamentales y avanzar hacia decisiones más concretas.

Orden conceptual:

```text
Propósito
   ↓
Producto
   ↓
Tecnología
   ↓
Arquitectura
   ↓
Planificación
   ↓
Ejecución
```

## 4.1 Primera entrevista — Propósito

La primera entrevista debe buscar suficiente información para establecer:

```text
MISSION.md
```

Debe explorar, según corresponda:

* problema;
* propósito;
* objetivo;
* usuarios o beneficiarios;
* resultado esperado;
* alcance conceptual;
* límites;
* principios relevantes.

No es necesario determinar en esta etapa toda la funcionalidad ni la arquitectura.

---

## 4.2 Segunda entrevista — Producto

Cuando la misión sea suficientemente clara, el agente puede ayudar a establecer:

```text
PRD.md
```

Debe descubrir progresivamente:

* actores;
* funcionalidades;
* requisitos funcionales;
* casos de uso;
* reglas de negocio;
* restricciones;
* requisitos no funcionales;
* criterios de aceptación;
* alcance del producto.

---

## 4.3 Tercera entrevista — Tecnología y diseño técnico

Cuando exista suficiente definición del producto, el agente puede ayudar a establecer:

```text
TECH-STACK.md
SPECIFICATIONS.md
```

Debe diferenciar entre:

* tecnologías elegidas;
* restricciones tecnológicas;
* decisiones arquitectónicas;
* patrones;
* estructura;
* contratos;
* persistencia;
* validación;
* seguridad;
* testing;
* demás decisiones técnicas.

No se debe confundir una tecnología con una especificación arquitectónica.

---

## 4.4 Cuarta entrevista — Planificación

Cuando el producto y las decisiones técnicas sean suficientemente claras, el agente puede ayudar a establecer:

```text
ROADMAP.md
```

El roadmap debe definir la evolución del proyecto y el orden de implementación a alto nivel.

No debe convertirse en una lista exhaustiva de tareas.

---

# 5. Documentos de constitución del proyecto

Los siguientes documentos describen el proyecto y deben mantenerse conceptualmente separados.

| Archivo             | Pregunta principal          | Responsabilidad                                        |
| ------------------- | --------------------------- | ------------------------------------------------------ |
| `MISSION.md`        | ¿Por qué existe?            | Propósito, problema, objetivo y límites                |
| `PRD.md`            | ¿Qué producto queremos?     | Requisitos, casos de uso y reglas de negocio           |
| `TECH-STACK.md`     | ¿Con qué lo construiremos?  | Tecnologías, herramientas y restricciones tecnológicas |
| `SPECIFICATIONS.md` | ¿Cómo lo construiremos?     | Arquitectura, diseño técnico y contratos               |
| `ROADMAP.md`        | ¿En qué orden evolucionará? | Fases y evolución de alto nivel                        |

### Regla de separación

* `MISSION.md` no debe convertirse en un PRD.
* `PRD.md` no debe convertirse en una especificación técnica.
* `TECH-STACK.md` no debe contener toda la arquitectura.
* `SPECIFICATIONS.md` no debe redefinir los requisitos del producto.
* `ROADMAP.md` no debe convertirse en un backlog detallado.

---

# 6. Documentos operativos

Los documentos operativos representan el trabajo necesario para ejecutar el proyecto.

| Archivo              | Responsabilidad                            |
| -------------------- | ------------------------------------------ |
| `PRODUCT_BACKLOG.md` | Trabajo pendiente del producto             |
| `SPRINT_BACKLOG.md`  | Trabajo seleccionado para el sprint actual |
| `SPRINT_TASK.md`     | Tarea actualmente ejecutada                |

La relación conceptual es:

```text
ROADMAP
   ↓
PRODUCT_BACKLOG
   ↓
SPRINT_BACKLOG
   ↓
SPRINT_TASK
   ↓
IMPLEMENTATION
```

El roadmap establece la dirección y el orden de alto nivel.

El backlog transforma esa dirección en trabajo ejecutable.

### Cómo se llenan los documentos operativos

* `PRODUCT_BACKLOG.md` contiene únicamente **épicas e historias de usuario de alto nivel**, derivadas de `PRD.md` y `ROADMAP.md`. No contiene tareas técnicas granulares.
* `SPRINT_BACKLOG.md` se usa para **desglosar y ordenar las tareas técnicas de la fase activa** del roadmap. Solo se detalla la fase en curso; no se adelanta el desglose de fases futuras.
* `SPRINT_TASK.md` contiene **la tarea en desarrollo activo**, de forma individual, hasta su finalización antes de pasar a la siguiente.

Flujo de ejecución: una fase del roadmap → sus tareas técnicas en `SPRINT_BACKLOG.md` → la tarea activa en `SPRINT_TASK.md` → implementación → pruebas → documentación/CHANGELOG.

---

# 7. Historial y trazabilidad

`CHANGELOG.md` conserva el historial relevante del proyecto.

Debe registrar, según corresponda:

* cambios significativos;
* decisiones importantes;
* motivo de las decisiones;
* relación con tareas o fases;
* cambios relevantes de comportamiento.

`CHANGELOG.md` representa **historia**, no necesariamente el estado técnico actual.

Por ejemplo:

```text
CHANGELOG.md
→ ¿Qué decisión tomamos y por qué?
```

mientras:

```text
SPECIFICATIONS.md
→ ¿Cuál es actualmente la decisión técnica vigente?
```

El agente no debe obligar al lector a reconstruir el estado actual leyendo todo el historial.

---

# 8. Estado de las decisiones

Cuando sea útil, las decisiones pueden clasificarse como:

### Definido

Decisión aprobada por el humano.

El agente debe respetarla durante la implementación.

### Por confirmar

Decisión pendiente.

El agente no debe implementarla basándose únicamente en una suposición.

Debe solicitar confirmación cuando la decisión sea necesaria para continuar.

### Evolutivo

Detalle que será definido durante una fase posterior del proyecto.

El agente no debe anticiparlo artificialmente si no es necesario para el trabajo actual.

---

# 9. Autoridad de los documentos

Cada documento tiene una responsabilidad específica.

Cuando exista información relevante, el agente debe consultar el documento correspondiente.

```text
MISSION.md
    ↓
Propósito

PRD.md
    ↓
Producto y requisitos

TECH-STACK.md
    ↓
Tecnologías

SPECIFICATIONS.md
    ↓
Diseño técnico vigente

ROADMAP.md
    ↓
Orden de evolución

PRODUCT_BACKLOG.md
    ↓
Trabajo pendiente

SPRINT_BACKLOG.md
    ↓
Trabajo del sprint

SPRINT_TASK.md
    ↓
Trabajo actual

CHANGELOG.md
    ↓
Historial
```

Si dos documentos contienen información aparentemente contradictoria, el agente no debe resolver el conflicto mediante una suposición.

Debe:

1. identificar el conflicto;
2. determinar qué decisiones están involucradas;
3. consultar al humano si no existe una regla explícita para resolverlo;
4. actualizar posteriormente los documentos afectados para recuperar consistencia.

---

# 10. Lectura del contexto

El agente debe comenzar consultando `AGENTS.md`.

Después debe determinar qué contexto es necesario para la tarea actual.

No es obligatorio leer todos los documentos en cada sesión.

Como referencia general:

```text
AGENTS.md
    ↓
MISSION.md
    ↓
PRD.md
    ↓
TECH-STACK.md
    ↓
SPECIFICATIONS.md
    ↓
ROADMAP.md
    ↓
PRODUCT_BACKLOG.md
    ↓
SPRINT_BACKLOG.md
    ↓
SPRINT_TASK.md
```

Para una tarea concreta, el agente debe consultar únicamente los documentos relevantes, manteniendo siempre suficiente contexto para evitar decisiones aisladas del resto del proyecto.

---

# 11. Casos de uso

Los casos de uso pertenecen al contexto del producto y deben documentarse en:

```text
PRD.md
```

No deben definirse principalmente en `SPECIFICATIONS.md`.

La relación es:

```text
PRD
    ↓
UC-01 — Registrar paciente
    ↓
SPECIFICATIONS
    ↓
POST /api/v1/patients
    ↓
IMPLEMENTATION
```

Un caso de uso describe lo que un actor necesita conseguir.

Una especificación técnica describe cómo el sistema implementará ese comportamiento.

No asumir que:

```text
1 caso de uso = 1 endpoint
```

Un caso de uso puede requerir múltiples operaciones técnicas.

---

# 12. Requisitos y decisiones técnicas

El agente debe mantener separadas estas preguntas:

```text
PRD
¿Qué debe hacer el sistema?
```

```text
SPECIFICATIONS
¿Cómo se implementará?
```

Por ejemplo:

```text
PRD:
El número de identificación de un paciente debe ser único.
```

puede derivar en:

```text
SPECIFICATIONS:
La unicidad se garantizará mediante una restricción UNIQUE
en la base de datos.
```

El requisito pertenece al producto.

La implementación de ese requisito pertenece a la especificación técnica.

---

# 13. No completar documentos mediante invención

Cuando un documento contenga información insuficiente, el agente no debe completar los espacios mediante:

* preferencias personales;
* convenciones no aprobadas;
* tecnologías populares;
* patrones considerados "best practice" sin aprobación;
* requisitos inferidos;
* funcionalidades inventadas;
* decisiones arquitectónicas prematuras.

Es preferible escribir:

```text
Status: Por confirmar
```

o preguntar al humano.

---

# 14. Flujo general de trabajo

El flujo conceptual del proyecto es:

```text
DISCOVERY
   ↓
MISSION
   ↓
PRODUCT DEFINITION
   ↓
PRD
   ↓
TECHNICAL DEFINITION
   ↓
TECH-STACK
   ↓
SPECIFICATIONS
   ↓
PLANNING
   ↓
ROADMAP
   ↓
BACKLOG
   ↓
SPRINT
   ↓
TASK
   ↓
IMPLEMENTATION
   ↓
TESTING
   ↓
DOCUMENTATION / CHANGELOG
```

Este flujo no es estrictamente lineal.

Durante la implementación puede ser necesario volver a una etapa anterior.

Por ejemplo:

```text
Implementation
      ↓
Technical problem discovered
      ↓
SPECIFICATIONS needs clarification
      ↓
Human decision
      ↓
SPECIFICATIONS updated
      ↓
Implementation continues
```

La documentación debe evolucionar junto con el conocimiento del proyecto.

---

# 15. Flujo de trabajo con Git

La estrategia de Git del proyecto es:

* `dev` como rama de integración;
* un branch de trabajo por fase o unidad significativa de trabajo;
* nombres de branch descriptivos;
* commits atómicos;
* Conventional Commits;
* merge a `dev` al completar una unidad de trabajo;
* `main` reservada para releases o estados estables.

El agente debe evitar mezclar cambios no relacionados dentro del mismo commit.

Antes de realizar operaciones destructivas o cambios que puedan afectar trabajo existente, debe verificar el estado del repositorio.

---

# 16. Principios generales

### Elaboración progresiva

No todas las decisiones deben tomarse al inicio.

### Preguntar antes de asumir

Las decisiones importantes deben ser confirmadas cuando no estén definidas.

### Una fase a la vez

No avanzar artificialmente a fases posteriores si las dependencias necesarias no están establecidas.

### Trazabilidad

Las decisiones y cambios relevantes deben poder relacionarse con requisitos, tareas o fases.

### Separación de responsabilidades

Cada documento debe contener únicamente la información correspondiente a su propósito.

### Fuente única de verdad

Una decisión vigente debe tener una ubicación documental clara.

### No inventar contexto

La ausencia de información no autoriza al agente a crear requisitos o decisiones.

### Mantener la documentación útil

La documentación debe ayudar a tomar decisiones y ejecutar el proyecto; no debe crecer únicamente por cumplir una plantilla.

### Confirmación humana

Las decisiones que cambien el alcance, arquitectura, tecnología, seguridad o comportamiento esperado deben ser aprobadas por el humano cuando no estén previamente definidas.

---

# 17. Regla final

El agente debe recordar:

> **Primero comprender el proyecto, después documentarlo, luego planificarlo y finalmente implementarlo.**

La documentación debe aparecer progresivamente conforme aumenta el conocimiento del proyecto.

El agente debe preferir:

```text
preguntar
```

antes que:

```text
asumir
```

y debe preferir:

```text
documentar una decisión explícita
```

antes que:

```text
dejar una decisión importante implícita en el código.
```