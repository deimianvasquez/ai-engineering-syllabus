# Huerto Comunitario Riverside — Plan de Telemetría (Ejemplo de Clase)

> **Para instructores:** Escenario paralelo en aula para `ai-eng-telemetry-plan`. Misma columna vertebral (KPIs desde contexto, event envelope, eventos `entidad_acción`, allowlists de propiedades, stream/batch, `telemetry-plan.md` + `event-schemas.json`), dominio distinto. Los estudiantes siguen el enunciado completo del monorepo en el `README.md` raíz del proyecto.

_These instructions are also available in [English](./README.md)._

---

## El reto

**GreenPatch Co-op** gestiona una app de préstamo de herramientas para huertos comunitarios: los socios reservan equipo compartido (carretillas, mangueras, composteras), lo recogen y lo devuelven. El stock nunca se edita directamente — solo mediante registros de **checkout** y **devolución** vinculados a un socio. El equipo de operaciones no puede responder preguntas básicas: qué herramientas se estropean más, quién abandona reservas o cuándo hay picos de recogida.

En una sesión, redacta un **mini plan de telemetría** antes de escribir código de instrumentación.

### Nota de alcance

| Proyecto evaluable (`ai-eng-telemetry-plan`)     | Este ejemplo de clase                     |
| ------------------------------------------------ | ----------------------------------------- |
| CONTEXT de empresa + monorepo de inventario      | CONTEXT ficticio GreenPatch (abajo)       |
| ≥5 puntos en flujo de inventario + ≥2 backoffice | 3 puntos en flujo de checkout + 1 de auth |
| ≥5 eventos diseñados por completo                | 4 eventos con envelope                    |
| Rúbrica completa de riesgos/exclusiones          | Párrafo corto de exclusiones              |
| PR al monorepo del estudiante                    | Solo `docs/telemetry/` local              |

---

## Mini contexto (usar en lugar de CONTEXT-company.md)

**KPIs a instrumentar:**

1. **Tasa de utilización de herramientas** — % de herramientas con al menos un checkout por semana.
2. **Tasa de abandono de reservas** — reservas iniciadas sin checkout en 24h.
3. **Cumplimiento de devoluciones** — devoluciones a tiempo vs. retrasadas.

**Entidades:** `Tool`, `Reservation`, `Checkout`, `Member`.  
**Regla:** `Tool.availableCount` solo cambia vía `Checkout` / `Return`, nunca edición directa.

---

## Qué construir

Crear en carpeta de demo o repo desechable:

- `docs/telemetry/telemetry-plan.md`
- `docs/telemetry/event-schemas.json`

### 1. KPI → mapeo de datos

- [ ] Por cada KPI: ¿qué dato lo compone? ¿Qué acción de API lo genera?
- [ ] Mapea el **flujo de checkout**: login → listar herramientas → crear reserva → confirmar checkout → devolución. Marca **3 puntos de instrumentación** (p. ej. reserva abandonada, validación de checkout fallida, devolución retrasada).

### 2. Event Envelope

- [ ] Documenta campos obligatorios: `eventId`, `timestamp` (ISO 8601), `sessionId`, `userId`, `eventName`, `schemaVersion`, `requestId`, `properties`.
- [ ] Indica que `properties` es solo allowlist por evento.

### 3. Diseña cuatro eventos

| Evento                       | Procesamiento sugerido | Notas                                   |
| ---------------------------- | ---------------------- | --------------------------------------- |
| `reservation_created`        | batch                  | Tendencias de volumen                   |
| `checkout_validation_failed` | batch                  | Patrones de error por herramienta       |
| `tool_threshold_low`         | stream                 | Alerta ops cuando `availableCount` bajo |
| `login_failed`               | stream                 | Seguridad / fricción                    |

Por cada evento:

- [ ] Frase de la regla de oro: _"Captamos `[evento]` porque necesitamos saber `[hipótesis]`, lo que nos permite tomar la decisión `[decisión]`."_
- [ ] Tabla de allowlist (nombre, tipo, obligatorio).
- [ ] Stream vs batch con justificación de **urgencia de negocio**.

### 4. Esquemas JSON

- [ ] Exporta los cuatro eventos a `event-schemas.json` (draft-07 o estructura propia documentada).
- [ ] `additionalProperties: false` en objetos `properties`.

### 5. Exclusiones (breve)

- [ ] Un evento considerado y descartado (con motivo).
- [ ] Un campo que **no** capturarás (p. ej. email del socio en `properties`).

---

## Verificar juntos

- [ ] Cada evento tiene hipótesis + decisión; ninguno es "por si acaso".
- [ ] Campos del envelope consistentes en los cuatro eventos.
- [ ] JSON válido y alineado con nombres/propiedades del Markdown.
- [ ] Al menos un stream y un batch con justificación no técnica.
- [ ] Sin contraseñas ni tokens en ninguna allowlist.

---

## Preguntas de discusión

1. ¿Por qué `tool_threshold_low` encaja mejor en stream que `reservation_created`?
2. ¿Qué problema hay si `userId` se duplica en `properties` además del envelope?
3. ¿Cómo ampliarías el plan a eventos de navegación sin disparar el volumen?
