# ClinicFlow — Misión

> Estado: **borrador v0.1** (2026-09-29). Lo marcado como *(por confirmar)* aún no está decidido.

## 1. Propósito

ClinicFlow es una **API REST CRUD de práctica**. No es un producto ni una pieza de portafolio: es un
campo de entrenamiento para mejorar como desarrollador y para dejar, al final, un conjunto de
**convenciones y decisiones documentadas** que se puedan aplicar a otras áreas de negocio.

## 2. Qué queremos mejorar (en orden de prioridad)

1. **Velocidad propia al escribir código**: flujo de trabajo, herramientas y patrones repetibles que
   reduzcan el tiempo entre "idea" y "endpoint funcionando".
2. **Buenas prácticas y convenciones**: estructura de proyecto, nombres, manejo de errores,
   validación, migraciones, configuración.
3. **Arquitecturas y patrones de diseño**: aplicarlos de forma consciente y entender por qué se elige
   cada uno. *(cuáles practicar primero: por confirmar)*

## 3. Alcance

### Dentro (v1)
- API REST con operaciones CRUD, enfocada solo en el backend.
- Primera entidad: **Paciente**. Después, si se decide, Médico y Cita (ver `roadmap.md`).
- Datos **simulados**: personajes y casos de la serie *Dr. House*. Nunca datos reales de personas.
- Un solo entorno: desarrollo local.

### Fuera (por ahora)
- Frontend, pagos, notificaciones, telemedicina.
- Despliegue (deployment) de cualquier tipo.
- Autenticación y roles de usuario *(por confirmar que se quedan fuera de v1)*.
- Observabilidad, caché y pruebas de carga: solo explicadas, no implementadas.
- Cualquier "extra" que no sea CRUD.

## 4. Usuarios

No hay usuarios finales reales. El único usuario es quien desarrolla y aprende. El dominio inicial
solo modela pacientes; no hay roles diferenciados en v1.

## 5. Replicabilidad

El entregable más valioso no es el código, sino:
- Una **guía de convenciones** (cómo estructuramos, nombramos, validamos, migramos, probamos).
- Un **registro de decisiones** (qué se decidió, alternativas consideradas y por qué).

La meta es poder abrir un proyecto de otro dominio (inventario, escuela, etc.) y seguir la guía sin
copiar código.

## 6. Principios de trabajo

- **Fases pequeñas** (1–2 horas) con un resultado verificable al final de cada una.
- **Una entidad completa de punta a punta** antes de ampliar el alcance.
- **Seguridad, pruebas y CI se introducen después** de tener la primera entidad funcionando, cada una
  como sus propias fases.
- **Nada se asume**: lo no decidido se pregunta y se registra.
- **Actualidad**: antes de cada fase se revisan las novedades de los frameworks usados y se aplican
  las prácticas vigentes.
- **Abierto a crecer**: el proyecto debe poder seguir iterando y sumando características.

## 7. Criterio de éxito

"Lo terminé y aprendí." Cada fase cierra con su criterio de "hecho" (ver `roadmap.md`) y con una
actualización de la guía de convenciones o del registro de decisiones *(por confirmar)*.

## 8. Forma de colaboración

El código lo escribe Claude siguiendo las convenciones acordadas y aprovechando las novedades vigentes
de cada framework. El desarrollador dirige las decisiones, revisa y aprende de cada fase.
