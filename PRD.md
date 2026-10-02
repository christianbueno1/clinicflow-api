# ClinicFlow — Product Requirements Document (PRD)

> **Estado:** Borrador v0.1
> **Fecha:** 2026-10-01
> **Proyecto:** ClinicFlow
> **Tipo:** API REST para práctica de desarrollo backend
> **Documento relacionado:** `MISSION.md`

---

## 1. Resumen del producto

ClinicFlow es una API REST desarrollada como proyecto práctico para aprender, ejercitar y mejorar habilidades de programación y desarrollo de software mediante la construcción progresiva de un sistema CRUD.

El proyecto utilizará el dominio de un centro médico como contexto de negocio. La primera entidad será `Patient` (paciente), sobre la cual se implementarán las operaciones fundamentales de persistencia, consulta, actualización y eliminación.

El desarrollo seguirá un enfoque incremental: cada funcionalidad se implementará, probará y documentará antes de avanzar a la siguiente. Las decisiones técnicas y las convenciones adoptadas deberán quedar registradas para facilitar su comprensión y reutilización en otros dominios.

ClinicFlow no pretende ser un sistema clínico real ni una solución destinada a gestionar información médica de personas reales.

## 2. Problema y oportunidad

Aprender programación y desarrollo backend requiere algo más que conocer la sintaxis de un lenguaje o framework. Es necesario practicar el proceso completo de construcción de software:

* Interpretar requisitos.
* Diseñar modelos de datos.
* Organizar un proyecto.
* Implementar funcionalidades.
* Validar entradas y manejar errores.
* Escribir y ejecutar pruebas.
* Aplicar convenciones y buenas prácticas.
* Comprender las decisiones técnicas.
* Explicar y defender una solución.

Los ejercicios aislados permiten practicar conceptos específicos, pero no siempre muestran cómo se relacionan dentro de un proyecto.

ClinicFlow busca proporcionar un entorno progresivo y replicable para ejercitar ese proceso mediante un caso CRUD concreto.

## 3. Público objetivo

ClinicFlow está dirigido a:

1. **Estudiantes de programación y desarrollo de software:** personas que necesitan practicar los fundamentos mediante un proyecto estructurado.
2. **Desarrolladores en formación:** personas que desean mejorar sus habilidades técnicas y sus hábitos de desarrollo.
3. **Candidatos a pruebas técnicas:** personas que necesitan practicar ejercicios de programación, especialmente aquellos que involucran operaciones CRUD, modelos de datos y construcción de APIs.
4. **Personas autodidactas:** quienes buscan un proyecto de referencia para estudiar, experimentar y evaluar su propio progreso.

El producto deberá favorecer la comprensión y la práctica progresiva, evitando introducir complejidad que no aporte valor al objetivo de aprendizaje.

## 4. Objetivos del producto

### 4.1 Objetivos principales

* Construir una API REST funcional mediante un proceso incremental.
* Practicar operaciones CRUD de principio a fin.
* Mejorar la velocidad de desarrollo mediante herramientas, convenciones y flujos de trabajo repetibles.
* Aplicar buenas prácticas de programación y organización del código.
* Comprender las decisiones de arquitectura y diseño adoptadas.
* Desarrollar hábitos de validación y verificación mediante pruebas.
* Documentar convenciones, decisiones y criterios de aceptación.
* Crear una base de conocimiento que pueda aplicarse a proyectos de otros dominios.
* Facilitar la preparación para pruebas técnicas que involucren operaciones CRUD.

### 4.2 Objetivos de aprendizaje

Al finalizar el proyecto, el desarrollador debería poder:

* Explicar la estructura general de una API REST.
* Describir el recorrido de una solicitud desde el endpoint hasta la persistencia.
* Crear y modificar modelos de dominio.
* Implementar operaciones CRUD.
* Comprender la validación de datos y el manejo de errores.
* Interpretar y aplicar convenciones de código.
* Ejecutar pruebas para verificar el comportamiento de la API.
* Justificar las principales decisiones técnicas.
* Adaptar los conocimientos adquiridos a otro dominio sin depender de copiar el código de ClinicFlow.

## 5. Alcance del producto

### 5.1 Incluido en la primera versión

* API REST backend.
* Desarrollo local.
* Dominio de centro médico ficticio.
* Entidad inicial `Patient`.
* Operaciones CRUD para pacientes.
* Persistencia de datos.
* Validación de entradas.
* Respuestas HTTP coherentes.
* Manejo de errores.
* Pruebas de las funcionalidades implementadas.
* Documentación técnica y de aprendizaje.
* Registro de decisiones y convenciones.
* Implementación por tareas pequeñas y verificables.

### 5.2 Posibles ampliaciones

Las siguientes entidades podrán incorporarse en fases posteriores, según lo establecido en `ROADMAP.md`:

* `Doctor`
* `Appointment`

Su incorporación no se considera requisito de la primera entrega. Antes de implementarlas se deberán definir sus responsabilidades, relaciones y criterios de aceptación.

### 5.3 Fuera del alcance

La primera versión no incluirá:

* Interfaz frontend.
* Pagos o facturación.
* Notificaciones.
* Telemedicina.
* Despliegue en producción.
* Gestión de usuarios, autenticación y roles (excluido de v1).
* Integraciones con sistemas médicos externos.
* Datos clínicos reales.
* Implementación de observabilidad avanzada, caché o pruebas de carga.

Los temas excluidos podrán documentarse como oportunidades de aprendizaje, pero no se implementarán salvo que se apruebe expresamente una ampliación del alcance.

## 6. Usuarios y actores

### 6.1 Desarrollador

Es el usuario principal del proyecto desde la perspectiva de aprendizaje. Utiliza ClinicFlow para implementar funcionalidades, ejecutar pruebas, estudiar decisiones técnicas y mejorar sus habilidades.

### 6.2 Consumidor de la API

Durante el desarrollo, las solicitudes se realizarán mediante herramientas de prueba de APIs o mecanismos equivalentes.

No se contempla un usuario final de negocio en la primera versión.

### 6.3 Paciente

`Patient` representa la primera entidad del dominio. Los registros serán ficticios y se utilizarán exclusivamente para practicar operaciones de persistencia y consulta.

No se definirán permisos diferenciados ni flujos de interacción para pacientes reales.

## 7. Requisitos funcionales

Los requisitos se organizan por capacidad. Los detalles de implementación y el orden de ejecución se definirán en `ROADMAP.md` y en las tareas de cada fase.

### RF-01 — Crear paciente

**Descripción:** La API deberá permitir registrar un paciente mediante una solicitud HTTP.

**Criterios de aceptación:**

* La solicitud deberá contener los campos obligatorios definidos para el modelo `Patient`.
* Los datos deberán validarse antes de persistirse.
* Una solicitud válida deberá crear un registro.
* La respuesta deberá indicar que la operación fue exitosa.
* La respuesta deberá permitir identificar el recurso creado.
* Una solicitud inválida deberá producir un error controlado y comprensible.
* No se deberán persistir registros cuando la validación falle.

### RF-02 — Consultar pacientes

**Descripción:** La API deberá permitir recuperar los pacientes registrados.

**Criterios de aceptación:**

* Deberá existir una operación para consultar la colección de pacientes.
* Deberá existir una operación para consultar un paciente individual mediante su identificador.
* La consulta de un registro existente deberá devolver sus datos.
* La consulta de un identificador inexistente deberá producir una respuesta de recurso no encontrado.
* La respuesta deberá mantener una estructura consistente.

### RF-03 — Actualizar paciente

**Descripción:** La API deberá permitir modificar los datos de un paciente existente.

**Criterios de aceptación:**

* La API deberá identificar el paciente que se desea modificar.
* Los datos recibidos deberán validarse.
* Una actualización válida deberá persistir los cambios.
* La respuesta deberá reflejar el resultado de la operación.
* Una solicitud inválida no deberá modificar el registro.
* La actualización de un identificador inexistente deberá producir una respuesta de recurso no encontrado.

**Decisión:** Se utilizará `PATCH` para la actualización parcial de pacientes. `PUT` queda descartado.

### RF-04 — Eliminar paciente

**Descripción:** La API deberá permitir eliminar un paciente existente.

**Criterios de aceptación:**

* La API deberá identificar el registro que se desea eliminar.
* La eliminación deberá reflejarse en la persistencia.
* La respuesta deberá comunicar correctamente el resultado.
* La eliminación de un identificador inexistente deberá producir una respuesta de recurso no encontrado.
* El comportamiento deberá verificarse mediante pruebas.

**Decisión:** Se utilizará eliminación lógica mediante el campo `deleted_at`.

### RF-05 — Validar datos de entrada

**Descripción:** La API deberá verificar que los datos recibidos cumplan las reglas definidas para el modelo.

**Criterios de aceptación:**

* Los campos obligatorios deberán ser identificados.
* Los tipos de datos deberán ser correctos.
* Los valores inválidos deberán rechazarse.
* Los errores de validación deberán ser controlados.
* Las reglas deberán estar documentadas y probadas.

### RF-06 — Manejar errores

**Descripción:** La API deberá proporcionar respuestas consistentes ante errores previsibles.

**Criterios de aceptación:**

* Los errores de validación deberán distinguirse de los errores de recurso inexistente.
* Los errores no deberán exponer información sensible ni detalles internos innecesarios.
* Las respuestas deberán utilizar códigos HTTP apropiados.
* El comportamiento deberá verificarse mediante pruebas.

### RF-07 — Documentar la API

**Descripción:** La API deberá contar con documentación que permita comprender y probar sus operaciones.

**Criterios de aceptación:**

* Los endpoints deberán estar documentados.
* Se deberán identificar los parámetros y cuerpos de solicitud.
* Se deberán describir las respuestas esperadas.
* Se deberán documentar los errores relevantes.
* La documentación deberá mantenerse alineada con la implementación.

### RF-08 — Verificar funcionalidades

**Descripción:** Cada funcionalidad implementada deberá contar con un mecanismo de verificación.

**Criterios de aceptación:**

* Las operaciones CRUD deberán probarse.
* Se deberán contemplar escenarios exitosos y errores previsibles.
* Las pruebas deberán poder ejecutarse de manera reproducible.
* Una fase no se considerará terminada mientras sus criterios de aceptación no hayan sido verificados.

## 8. Requisitos no funcionales

### RNF-01 — Mantenibilidad

El código deberá organizarse de forma que las responsabilidades sean claras y los cambios puedan realizarse sin introducir dependencias innecesarias.

### RNF-02 — Legibilidad

Los nombres, estructuras y convenciones deberán facilitar la comprensión del código por parte de otro desarrollador.

### RNF-03 — Seguridad básica

La API deberá aplicar validación de entradas, manejo controlado de errores y protección de información sensible. Las medidas de seguridad se incorporarán progresivamente, según el alcance de cada fase.

### RNF-04 — Consistencia

Los endpoints, modelos, respuestas y errores deberán seguir convenciones coherentes a lo largo del proyecto.

### RNF-05 — Reproducibilidad

El entorno de desarrollo y los procedimientos de ejecución y prueba deberán estar documentados para que el proyecto pueda configurarse y verificarse de manera consistente.

### RNF-06 — Aprendizaje progresivo

Las decisiones técnicas deberán ser proporcionales al problema y estar acompañadas de una explicación que permita comprender su propósito.

### RNF-07 — Transferibilidad

Las convenciones y decisiones deberán documentarse de forma que puedan adaptarse a otros dominios, sin asumir que la estructura de ClinicFlow es universal.

## 9. Datos y dominio

### 9.1 Entidad inicial

La primera entidad será `Patient`.

Los atributos definitivos, sus tipos, restricciones y relaciones se especificarán durante la fase de modelado y se documentarán en la especificación técnica.

No se deberán asumir campos clínicos ni datos personales reales.

### 9.2 Datos de prueba

Se utilizarán registros ficticios. Los datos de prueba podrán inspirarse en personajes o situaciones ficticias, como las asociadas a Dr. House, siempre que no se utilice información personal real.

### 9.3 Persistencia

La API deberá almacenar los registros de manera que puedan recuperarse y modificarse mediante las operaciones definidas.

La tecnología y las decisiones específicas de persistencia deberán estar documentadas en `TECH-STACK.md` y en la especificación técnica correspondiente.

## 10. Experiencia de desarrollo

Aunque ClinicFlow no incluye una interfaz de usuario, la experiencia del desarrollador forma parte de los objetivos del producto.

El proyecto deberá facilitar:

* Configuración clara del entorno.
* Ejecución sencilla de la API.
* Acceso a la documentación de endpoints.
* Ejecución reproducible de pruebas.
* Comprensión del flujo de trabajo.
* Identificación de las tareas pendientes.
* Consulta de decisiones técnicas anteriores.

Las instrucciones necesarias deberán mantenerse en la documentación del repositorio.

## 11. Metodología de implementación

El desarrollo seguirá estas reglas:

1. Dividir el trabajo en fases pequeñas, preferentemente de una a dos horas.
2. Implementar una entidad de principio a fin antes de ampliar el dominio.
3. Definir criterios de aceptación antes de considerar terminada una tarea.
4. Verificar cada funcionalidad mediante pruebas.
5. Documentar las convenciones y decisiones relevantes.
6. Separar las nuevas preocupaciones técnicas en fases específicas cuando sea conveniente.
7. Revisar las prácticas y capacidades actuales del framework antes de iniciar fases relevantes.
8. Revisar y comprender el código generado con asistencia de IA antes de incorporarlo como definitivo.

## 12. Criterios de finalización del producto

La primera versión de ClinicFlow se considerará terminada cuando:

* Las operaciones CRUD de `Patient` estén implementadas y verificadas.
* La API pueda ejecutarse en el entorno local documentado.
* Las validaciones y los errores principales estén controlados.
* Las pruebas definidas para la primera versión puedan ejecutarse.
* La documentación de la API esté disponible y actualizada.
* Las decisiones técnicas relevantes estén registradas.
* Las convenciones adoptadas estén documentadas.
* El desarrollador pueda explicar el funcionamiento general y las decisiones principales.
* El conocimiento adquirido pueda adaptarse a otro ejercicio CRUD sin depender de copiar el código.

El criterio de éxito no será únicamente que la API funcione, sino que el desarrollador pueda afirmar:

**«Lo terminé, lo comprendí y puedo replicarlo».**

## 13. Riesgos y consideraciones

| Riesgo                                             | Consideración                                                           |
| -------------------------------------------------- | ----------------------------------------------------------------------- |
| Introducir demasiada complejidad                   | Priorizar los fundamentos CRUD y justificar cada abstracción.           |
| Avanzar sin comprender el código                   | Revisar y explicar las implementaciones antes de continuar.             |
| Acumular decisiones sin documentar                 | Registrar las decisiones relevantes durante cada fase.                  |
| Ampliar el alcance prematuramente                  | Evaluar cada nueva funcionalidad frente a los objetivos de aprendizaje. |
| Depender de prácticas obsoletas                    | Revisar la documentación vigente del framework y sus herramientas.      |
| Confundir el ejercicio con un producto médico real | Utilizar datos ficticios y mantener explícito el propósito educativo.   |

## 14. Decisiones pendientes

Los siguientes puntos requieren definición antes de que afecten a la implementación:

* [ ] (Ninguno por ahora. Ver sección 15 — Decisiones registradas.)

Las decisiones deberán registrarse y aprobarse antes de considerarse requisitos definitivos.

---

## 15. Decisiones registradas

El registro de decisiones vive en `CHANGELOG.md`. Este PRD conserva únicamente el alcance del producto.

---

**Fin del documento.**
