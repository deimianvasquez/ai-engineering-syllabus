# Biblioteca Pública Riverside — Pipeline de actividad de préstamos (Ejemplo de clase)

> **Para instructores:** Escenario paralelo en aula para `designing-data-pipeline`. Mismo esqueleto (documento de diseño ETL, análisis de formato CSV, diagrama de flujo, deduplicación con actualizaciones como inserts, idempotencia, log de ejecución, criterios de robustez), distinto dominio. Los estudiantes siguen el brief completo de Veridian Logistics en el `README.md` de la raíz del proyecto.

_These instructions are also available in [English](./README.md)._

---

## El reto

La **Biblioteca Pública Riverside** usa un sistema de circulación legacy en tres sucursales. Cada noche exporta un CSV único de actividad de préstamos: nuevos préstamos, renovaciones, devoluciones y avisos de mora. Cuando un préstamo pasa de _prestado_ a _devuelto_, el sistema **añade una fila nueva** en lugar de actualizar la original — el mismo `loan_id` puede aparecer varias veces con distintos estados.

Operaciones quiere reportes semanales fiables (préstamos activos por sucursal, tasa de mora), pero cualquier pipeline que cargue filas sin procesar cuenta préstamos activos dos veces.

En una sesión, redacta un **mini `PIPELINE_DESIGN.md`** — sin código.

### Nota de alcance

| Proyecto evaluable (`designing-data-pipeline`)            | Este ejemplo de clase                              |
| --------------------------------------------------------- | -------------------------------------------------- |
| Veridian Logistics / cinco hubs / envíos                  | Riverside Library / tres sucursales / préstamos    |
| Brief completo de la CTO + todas las secciones del rubric | Mismos encabezados de sección, narrativa más corta |
| Métricas de carga multi-hub                               | KPIs de préstamos por sucursal                     |
| Repo del estudiante + commit                              | Solo markdown local                                |

---

## Qué construir

Crea `PIPELINE_DESIGN.md` (carpeta temporal o repo demo) con estas secciones:

### 1. Propósito

- [ ] Explica el problema de filas duplicadas (actualizaciones como inserts).
- [ ] Nombra salidas: p. ej. `reporting.fact_loans` (una fila por `loan_id`) y `reporting.daily_branch_metrics`.

### 2. Análisis del formato de datos

- [ ] ¿Cuándo basta CSV en origen? ¿Cuándo usarías Parquet o staging tipado?
- [ ] Una recomendación justificada por zona del pipeline (raw / staging / reporting).

### 3. Diagrama de flujo de datos

- [ ] Mermaid o ASCII: fuente → extracción → transformación (dedup aquí) → carga → destino.
- [ ] Indica dónde se aplica la idempotencia.

### 4. Estrategia de deduplicación

- [ ] Clave de negocio: `loan_id` (y `branch_id` si los préstamos pueden cambiar de sucursal).
- [ ] Regla: conservar la fila más reciente por `event_timestamp` en **todos los archivos del lote**.
- [ ] Menciona un caso límite (p. ej. renovación y devolución la misma noche).

### 5. Plan de idempotencia

- [ ] Describe fallo a mitad de carga y reintento seguro (tabla staging, merge transaccional o checkpoint con `run_id`).
- [ ] Explica por qué re-ejecutar no duplica filas en `fact_loans`.

### 6. Log de ejecución (mínimo cinco campos)

| Campo              | Por qué importa                        |
| ------------------ | -------------------------------------- |
| `run_id`           | Trazar una ejecución                   |
| `source_files`     | Auditar qué export nocturno se procesó |
| `rows_extracted`   | Detectar archivos vacíos o truncados   |
| `rows_after_dedup` | Medir presión de duplicados            |
| `status`           | Alertas                                |

Añade al menos un campo más con justificación.

### 7. Criterios de robustez

- [ ] Tres rasgos concretos (validación de esquema, cuarentena, alertas, retención raw, etc.) — no "buen código" genérico.

---

## Verificar juntos

- [ ] La dedup responde a actualizaciones-como-inserts, no solo `DISTINCT` en un archivo.
- [ ] El diagrama muestra dedup **antes** del merge a reporting.
- [ ] El mecanismo de idempotencia es específico (no solo "volver a ejecutar").
- [ ] La sección de formato incluye trade-offs, no solo definiciones.
- [ ] Sin archivos Python/SQL de implementación — solo documento de diseño.

---

## Preguntas de discusión

1. ¿Por qué la deduplicación debe ejecutarse sobre todo el lote nocturno y no por archivo CSV?
2. ¿Qué falla si usas `returned_at` para ordenar cuando algunas devoluciones no tienen ese campo?
3. ¿Cómo extenderías este diseño si la biblioteca añade eventos API en tiempo real además del CSV nocturno?
