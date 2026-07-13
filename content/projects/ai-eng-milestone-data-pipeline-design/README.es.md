# Hito 6 — Diseño del pipeline de datos de la compañía (1/3)

<!-- hide -->

Por [@marcogonzalo](https://github.com/marcogonzalo) y [otros colaboradores](https://github.com/4GeeksAcademy/ai-engineering-company-project-monorepo/graphs/contributors) en [4Geeks Academy](https://4geeksacademy.com/)

[![build by developers](https://img.shields.io/badge/build_by-Developers-blue)](https://4geeks.com)
[![4Geeks Academy](https://img.shields.io/twitter/follow/4geeksacademy?style=social&logo=x)](https://x.com/4geeksacademy)

_These instructions are [available in English](./README.md)._

<!-- endhide -->

## 🎯 El Reto

> 📌 Estás construyendo sobre **tu copia** del **[monorepo](https://github.com/4GeeksAcademy/ai-engineering-company-project-monorepo)** de la empresa seleccionada al inicio del curso — no en un repositorio nuevo.

Has pasado las últimas semanas capturando eventos de telemetría, almacenándolos en base de datos y generando informes básicos con Pandas. Ahora tu tech lead quiere algo más: un pipeline de datos que sea robusto, auditable y que tu equipo pueda ejecutar con confianza en producción.

Tu CTO te ha enviado este brief a través del gestor de tareas del equipo:

> > **Brief técnico — Pipeline de datos (Diseño)**
> >
> > Antes de escribir una sola línea de código de orquestación, necesito que documentes el diseño del pipeline de datos de nuestra plataforma. El equipo de datos ha recibido una RFP interna del área de operaciones: quieren saber exactamente cómo fluyen los datos desde que se capturan en la aplicación hasta que llegan a los dashboards. También quieren garantías sobre idempotencia y auditabilidad antes de aprobar el paso a producción.
> >
> > Entregable: un documento de diseño en Markdown dentro del monorepo. Sin código de orquestación todavía — primero el diseño, luego la implementación.

### ¿Qué es un pipeline de datos robusto?

Un pipeline de datos no es simplemente un script que mueve información de un sitio a otro. Un pipeline de producción tiene etapas bien definidas, maneja fallos de forma predecible y puede ser auditado. Los tres atributos clave que distinguen un pipeline robusto de uno que "simplemente funciona" son:

- **Idempotencia**: ejecutar el pipeline dos veces sobre los mismos datos produce el mismo resultado, sin duplicados ni corrupción.
- **Observabilidad**: cada ejecución deja trazas suficientes para saber qué pasó, cuándo y por qué.
- **Recuperabilidad**: cuando el pipeline falla a mitad de camino, la siguiente ejecución sabe exactamente desde dónde retomar.

Estos tres atributos son los que tu documento de diseño debe demostrar que has pensado en profundidad.

### Construye el pipeline en torno a un objetivo de negocio

Un pipeline de datos no existe por sí mismo. Existe para lograr un **objetivo de negocio concreto**: una decisión que la empresa debe tomar, o una métrica que debe seguir de forma fiable en el tiempo.

Antes de diseñar extracción, transformación o carga, pregúntate: _¿qué pregunta debe responder este pipeline y quién actuará con la respuesta?_ Objetivos vagos producen pipelines vagos. Objetivos concretos definen cada decisión de diseño: qué eventos extraer, con qué frecuencia ejecutar el flujo, a qué granularidad agregar y qué significa "terminado" en cada ejecución.

**Ejemplos de objetivos específicos:**

- Entender el **comportamiento del usuario en el backoffice** (qué flujos usa, dónde abandonan los operadores) para **aumentar la tasa de conversión o ventas**.
- Medir la **frecuencia de consumo** y los **patrones de reposición entrante** para **anticipar roturas de stock** y priorizar el reabastecimiento.

Ya definiste esta dirección en hitos anteriores. Tu **plan de telemetría** identificó los KPIs principales de la empresa; tu **informe de telemetría** los convirtió en métricas calculables a partir de eventos almacenados. El diseño del pipeline debe **continuar ese hilo**: debe producir de forma fiable los datos que esos KPIs necesitan — con la frescura, granularidad y trazabilidad adecuadas — no solo mover filas entre tablas.

Cuando escribas el propósito del pipeline en la Fase 2, vincúlalo directamente con al menos un KPI de tu monorepo. Si una etapa del diseño no apoya un KPI ni una decisión operativa concreta, cuestiona si debe estar en la v1.

### Preguntas que te ayudan a diseñar el pipeline

Antes de escribir `PIPELINE_DESIGN.md`, responde por escrito — aunque sea en borrador — cómo abordarías cada caso en **tu** monorepo.

#### Idempotencia

1. **Duplicados en origen** — ¿Cómo evitas contar dos veces la misma acción en `telemetry_events` y en los agregados de KPI? ¿Qué campo del envelope usas como clave y en qué capa deduplicas?

   <details>
   <summary>Ver ejemplo y pista</summary>

   Un operador confirma `outbound_order_submitted` dos veces en 300 ms; llegan dos filas con el mismo `eventId` pero distinto timestamp de recepción.

   **Pista:** upsert por `eventId` en ingestión.

   </details>

2. **Re-ejecución tras fallo** — Si el pipeline muere en la fase de carga con datos parcialmente insertados, ¿qué pasa al relanzarlo? ¿Cómo garantizas el mismo resultado que en una ejecución limpia?

   <details>
   <summary>Ver ejemplo y pista</summary>

   El run de las 02:00 cargó 847 de 1.412 filas en `reporting.daily_outbound_metrics` y falló por timeout de Supabase.

   **Pista:** upsert por clave de partición diaria.

   </details>

3. **Eventos tardíos** — ¿Cómo recomputas un KPI diario ya publicado cuando llega un evento retrasado, sin inflar métricas ni perder trazabilidad?

   <details>
   <summary>Ver ejemplo y pista</summary>

   A las 23:50 se registra un `checkout_validation_failed` con `timestamp` del mediodía; el agregado del día ya está en el dashboard.

   **Pista:** recomputar ventana; registrar run invalidante.

   </details>

#### Observabilidad

4. **Silencio vs. ausencia real** — ¿Cómo distingues "cero actividad" de "captura caída" o "pipeline que no corrió"? ¿Qué señales mínimas registrarías?

   <details>
   <summary>Ver ejemplo y pista</summary>

   Entre 14:00 y 15:00 no hay `login_failed` ni `order_submitted`, pero el almacén siguió operando con normalidad.

   **Pista:** heartbeat más alerta por silencio.

   </details>

5. **Trazabilidad de recolección** — ¿Qué trazas reconstruyen el camino evento → dashboard y detectan huecos, ráfagas o desfases en los intervalos?

   <details>
   <summary>Ver ejemplo y pista</summary>

   Un KPI pica a las 09:00 y queda plano a las 09:15; no está claro si fue demanda real o un batch que procesó dos ventanas juntas.

   **Pista:** correlacionar `requestId` y `run_id`.

   </details>

6. **Crecimiento vs. pérdida de datos** — Si el volumen de eventos varía mucho entre días, ¿cómo sabes si la app crece o si hay mediciones perdidas o duplicadas?

   <details>
   <summary>Ver ejemplo y pista</summary>

   Lunes: 12.000 eventos; domingo: 800 — ¿turnos de operadores o fallos intermitentes en `POST /telemetry`?

   **Pista:** contrastar eventos con sesiones activas.

   </details>

#### Recuperabilidad

7. **Caída de base de datos** — ¿Desde qué fase retomas si la conexión cae a mitad del pipeline? ¿Qué checkpoint persistes?

   <details>
   <summary>Ver ejemplo y pista</summary>

   Pandas terminó de agrupar por `product_id`, pero Supabase cayó al hacer `INSERT` en la tabla de reporting.

   **Pista:** checkpoint de fase en `pipeline_runs`.

   </details>

8. **Buffer en el frontend** — ¿Tiene sentido acumular eventos offline en el navegador? ¿Qué riesgos introduce y qué capa debe resolverlos?

   <details>
   <summary>Ver ejemplo y pista</summary>

   Un operador pierde WiFi 20 minutos; el navegador guarda 45 eventos en `localStorage` y los envía al reconectar en un solo lote.

   **Pista:** buffer cliente; dedup en servidor.

   </details>

9. **Retry de transmisión** — ¿Cómo diseñas reintentos en `POST /telemetry` sin romper idempotencia? ¿Qué respuesta del servidor confirma "ya guardado" vs. "reintenta"?

   <details>
   <summary>Ver ejemplo y pista</summary>

   El cliente recibe timeout, reintenta, pero el servidor ya persistió el evento en la petición lenta original.

   **Pista:** `Idempotency-Key`; devolver 200 si existe.

   </details>

#### Cruce de principios

10. **Ejecuciones simultáneas** — ¿Qué observas, cómo evitas condiciones de carrera y cómo recuperas si el cron y un trigger manual desde `services/` corren a la vez?

    <details>
    <summary>Ver ejemplo y pista</summary>

    A las 02:00 arranca el flow programado y a las 02:05 alguien pulsa "Run pipeline now" en el backoffice de operaciones.

    **Pista:** lock por ventana; `run_id` único.

    </details>

---

## 🌱 Cómo Empezar

1. Haz un `git pull` en tu fork del monorepo para asegurarte de tener el estado más reciente.
2. Explora la carpeta [`data/`](https://github.com/4GeeksAcademy/ai-engineering-company-project-monorepo/tree/main/data) del monorepo — contiene las subcarpetas `raw/`, `process/`, `pipelines/` y `eval/` que usarás a lo largo de este módulo. El código de orquestación vivirá en `data/pipelines/`; los scripts de transformación reutilizables en `data/process/`; los endpoints HTTP que consulten o disparen el pipeline vivirán en `services/` e importarán desde `data/pipelines/` — no al revés.
3. Crea el archivo `data/pipelines/PIPELINE_DESIGN.md` — ahí va tu documento de diseño.
4. Revisa los eventos de telemetría, KPIs y entidades de dominio que ya tienes en el monorepo para identificar qué datos debe procesar tu pipeline.

> **Nota sobre las herramientas:** Hoy introduces **Prefect** como framework de orquestación — flows, tasks, estados y bloques de configuración. Tu documento de diseño debe reflejar cómo organizarías tu pipeline usando estos conceptos, aunque la implementación en código llega en los próximos días.

---

## 💻 Qué Debes Hacer

### Fase 1 — Análisis del estado actual

- [ ] Documenta en una sección "Estado actual" los datos que ya tienes: qué eventos de telemetría has capturado, dónde están almacenados y qué informes ya generas con Pandas.
- [ ] Identifica las limitaciones de tu implementación actual: ¿qué pasa si el script falla a mitad de ejecución? ¿puedes saber si los datos ya fueron procesados?

### Fase 2 — Diseño del pipeline

- [ ] Define el **propósito** del pipeline en una frase concreta: qué problema resuelve y qué valor entrega a tu empresa.
- [ ] Especifica el **formato de extracción**: de dónde vienen los datos (tabla, endpoint, fichero), en qué formato llegan y con qué frecuencia se actualizan.
- [ ] Diseña el **flujo de datos** con un diagrama en texto o Mermaid con al menos tres etapas claramente separadas: extracción, transformación y carga.
- [ ] Describe cómo manejarías una fuente que **actualiza registros existentes** en lugar de insertar siempre nuevos — explica la estrategia concreta para evitar duplicados en tu caso.

### Fase 3 — Resiliencia e idempotencia

- [ ] Define la estrategia de **idempotencia**: si el pipeline falla durante la fase de carga y se vuelve a ejecutar, explica exactamente cómo garantizas que los datos ya cargados no se corrompen ni se duplican.
- [ ] Diseña el **log de ejecución**: especifica los campos mínimos que registrarías en cada ejecución (inicio, fin, registros procesados, estado, errores) y explica por qué cada campo es necesario para auditar el pipeline en producción.

### Fase 4 — Mapa a Prefect

- [ ] Mapea tu diseño a los conceptos de Prefect: identifica cuáles serían tus **flows**, cuáles serían tus **tasks** y qué **estados** (Running, Completed, Failed) son relevantes para tu pipeline.
- [ ] Indica qué configuración o credenciales gestionarías como **bloques de Prefect** (por ejemplo, la conexión a Supabase).

### Fase 5 — Integración con la aplicación (solo diseño)

- [ ] Esboza qué **endpoints en `services/`** usará el equipo de operaciones para consultar el estado/metadatos de la última ejecución y para disparar una ejecución manual del flow.
- [ ] Para cada endpoint, indica qué **función o flow de `data/pipelines/`** llamará — la lógica ETL no pertenece a `services/`.

⚠️ **IMPORTANTE:** El diseño debe ser específico para los datos de tu empresa. Los nombres de eventos, KPIs, tablas y entidades deben coincidir con el vocabulario de dominio de tu monorepo. Un diseño genérico que ignore el modelo de datos de tu empresa no será aceptado.

---

## ✅ Qué Evaluaremos

- [ ] El documento `data/pipelines/PIPELINE_DESIGN.md` existe en el monorepo y está escrito en Markdown legible.
- [ ] El propósito del pipeline está definido en una frase concreta que menciona el negocio de la empresa, no solo la tecnología.
- [ ] El diagrama de flujo muestra al menos tres etapas diferenciadas (extracción, transformación, carga) con el nombre de las entidades o tablas reales de la empresa.
- [ ] La estrategia para manejar actualizaciones de registros existentes está documentada con un mecanismo concreto (ej.: upsert por clave primaria, marca de tiempo de última modificación, tabla de control).
- [ ] La estrategia de idempotencia es explícita: describe qué ocurre en la segunda ejecución tras un fallo en la carga, no solo qué sería deseable.
- [ ] El log de ejecución especifica al menos cinco campos con el nombre del campo, el tipo de dato y la justificación de por qué ese campo es necesario para auditoría.
- [ ] El mapa a Prefect identifica al menos dos flows y tres tasks con nombres concretos alineados con las etapas del pipeline.
- [ ] El diseño documenta al menos dos endpoints planificados en `services/` (consulta de estado y disparo manual) y nombra las funciones de `data/pipelines/` que cada uno importará.
- [ ] El diseño es coherente con los eventos de telemetría y KPIs ya capturados en tu monorepo.

---

## 📦 Cómo Entregar

1. Asegúrate de que `data/pipelines/PIPELINE_DESIGN.md` está en tu fork del monorepo.
2. Haz commit con el mensaje: `feat: add pipeline design document`.
3. Sube los cambios a tu repositorio en GitHub y comparte la URL con tu tech lead.

---

Este y muchos otros proyectos son construidos por estudiantes como parte de los [Coding Bootcamps](https://4geeksacademy.com/) de 4Geeks Academy. Encuentra más acerca de los [cursos](https://4geeksacademy.com/es/comparar-programas) de [Full-Stack Software Developer](https://4geeksacademy.com/es/programas-de-carrera/desarrollo-full-stack), [Data Science & Machine Learning](https://4geeksacademy.com/es/programas-de-carrera/ciencia-de-datos-ml), [Ciberseguridad](https://4geeksacademy.com/es/programas-de-carrera/ciberseguridad) e [Ingeniería de IA](https://4geeksacademy.com/es/programas-de-carrera/ingenieria-ia).
