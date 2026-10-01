# ClinicFlow — Misión

> Estado: **borrador v0.2** (2026-10-01). Lo marcado como *(por confirmar)* aún no está decidido.

## 1. Propósito

ClinicFlow es una **API REST CRUD de práctica**. No es un producto comercial ni una pieza de portafolio: es un campo de entrenamiento para mejorar las habilidades de desarrollo de software y construir un conjunto de **convenciones, patrones y decisiones documentadas** que puedan aplicarse a otras áreas de negocio.

El proyecto busca ofrecer una experiencia práctica de desarrollo backend que permita aprender, experimentar y comprender el proceso de construcción de una API, desde el diseño de los modelos de datos hasta la implementación y verificación de sus operaciones.

## 2. Público objetivo (Target Audience)

ClinicFlow está dirigido a:

* **Estudiantes de programación y desarrollo de software:** personas que están aprendiendo a construir aplicaciones backend y necesitan un proyecto práctico para aplicar sus conocimientos.
* **Desarrolladores en formación:** personas que desean fortalecer sus competencias en programación, diseño de software, bases de datos, APIs REST y buenas prácticas de desarrollo.
* **Candidatos a pruebas técnicas:** desarrolladores que se preparan para entrevistas laborales, evaluaciones técnicas o pruebas prácticas basadas en operaciones CRUD.
* **Desarrolladores autodidactas:** personas que buscan un proyecto de referencia para experimentar con tecnologías, patrones de diseño, convenciones y herramientas de desarrollo.

El proyecto debe proporcionar una base comprensible, progresiva y replicable que permita a estos perfiles estudiar las decisiones de diseño, implementar funcionalidades y evaluar sus conocimientos mediante ejercicios prácticos.

ClinicFlow no pretende ser una solución médica comercial ni un producto destinado a usuarios finales reales.

## 3. Qué queremos mejorar (en orden de prioridad)

1. **Velocidad de desarrollo:** flujo de trabajo, herramientas y patrones repetibles que reduzcan el tiempo entre "idea" y "endpoint funcionando".
2. **Buenas prácticas y convenciones:** estructura de proyecto, nombres, manejo de errores, validación, migraciones y configuración.
3. **Arquitecturas y patrones de diseño:** aplicarlos de forma consciente y entender por qué se elige cada uno. *(Cuáles practicar primero: por confirmar).*

Estos objetivos deben abordarse de manera progresiva, priorizando la comprensión de los fundamentos antes de introducir complejidad adicional.

## 4. Alcance

### Dentro (v1)

* API REST con operaciones CRUD, enfocada solo en el backend.
* Primera entidad: **Paciente**. Después, si se decide, Médico y Cita (ver `roadmap.md`).
* Datos **simulados**: personajes y casos de la serie *Dr. House*. Nunca datos reales de personas.
* Un solo entorno: desarrollo local.
* Documentación de convenciones, decisiones técnicas y criterios de implementación que puedan reutilizarse en otros proyectos.
* Desarrollo progresivo mediante tareas pequeñas con resultados verificables.

### Fuera (por ahora)

* Frontend, pagos, notificaciones y telemedicina.
* Despliegue (deployment) de cualquier tipo.
* Autenticación y roles de usuario: excluidos de v1.
* Observabilidad, caché y pruebas de carga: solo explicadas, no implementadas.
* Cualquier funcionalidad adicional que no contribuya directamente a los objetivos de aprendizaje o al alcance CRUD.

## 5. Usuarios

ClinicFlow no contempla usuarios finales reales en su versión inicial. Su público objetivo está compuesto por personas que desarrollan y aprenden.

El dominio inicial solo modela pacientes; no hay roles diferenciados en v1.

Los datos utilizados son exclusivamente simulados y tienen fines de práctica.

## 6. Replicabilidad

El entregable más valioso no es únicamente el código, sino el conocimiento que se construye durante su desarrollo y que queda documentado en:

* Una **guía de convenciones**: cómo estructuramos, nombramos, validamos, migramos y probamos.
* Un **registro de decisiones**: qué se decidió, cuándo, qué alternativas se consideraron y por qué.
* Una **especificación técnica**: cómo se organiza y diseña la solución, y cuáles son sus criterios de implementación.

La meta es poder abrir un proyecto de otro dominio (inventario, escuela, consultorio, etc.) y aplicar los conocimientos y convenciones adquiridos sin necesidad de copiar código.

La documentación debe permitir comprender no solo cómo se implementó una solución, sino también el razonamiento detrás de las decisiones.

## 7. Principios de trabajo

* **Fases pequeñas:** tareas de 1–2 horas con un resultado verificable al final de cada una.
* **Una entidad completa de punta a punta:** antes de ampliar el alcance.
* **Seguridad, pruebas y CI:** se introducen después de tener la primera entidad funcionando, cada una como sus propias fases.
* **Nada se asume:** lo no decidido se pregunta y se registra.
* **Actualidad:** antes de cada fase se revisan las novedades de los frameworks usados y se aplican las prácticas vigentes.
* **Aprendizaje progresivo:** cada nueva técnica o patrón debe introducirse con un propósito claro y un nivel de complejidad adecuado.
* **Comprensión sobre automatización:** el código generado por herramientas de IA debe ser revisado, comprendido y validado por el desarrollador.
* **Abierto a crecer:** el proyecto debe poder seguir iterando y sumando características sin perder claridad ni coherencia.

## 8. Criterio de éxito

**"Lo terminé, lo comprendí y puedo replicarlo."**

El proyecto será exitoso cuando:

* Las operaciones CRUD de la primera entidad funcionen correctamente y cumplan sus criterios de aceptación.
* El desarrollador comprenda las decisiones técnicas y pueda explicar las razones detrás de ellas.
* Cada fase cierre con un resultado verificable y la documentación correspondiente actualizada.
* Las convenciones y patrones documentados puedan aplicarse a un proyecto de otro dominio sin copiar código.
* El proyecto sirva como material de estudio y referencia para estudiantes y desarrolladores que se preparan para pruebas técnicas basadas en CRUD.

## 9. Forma de colaboración

El código lo escribe Claude siguiendo las convenciones acordadas y aprovechando las novedades vigentes de cada framework.

El desarrollador dirige las decisiones, revisa y aprende de cada fase. Las propuestas técnicas que impliquen nuevas decisiones deben ser presentadas para su evaluación y aprobación antes de incorporarse como acuerdos definitivos.

El uso de herramientas de IA debe acelerar el desarrollo sin sustituir la comprensión del código, el razonamiento técnico ni la responsabilidad del desarrollador sobre el resultado.
