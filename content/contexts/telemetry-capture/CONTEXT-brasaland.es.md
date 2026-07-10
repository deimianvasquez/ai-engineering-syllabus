# CONTEXT — Brasaland · Telemetría Fase 2: Captura desde el Frontend

## Tu empresa

**Brasaland** es una cadena de restaurantes de comida a la brasa con 14 locales en Colombia y Florida. Formas parte de **Brasaland Digital**, el equipo interno de tecnología. El backoffice lo usan a diario los gerentes de local y supervisores de operaciones para registrar entradas de ingredientes (entregas de proveedores) y salidas de ingredientes (consumo y merma). Hoy instrumentas ese backoffice con los eventos que diseñaste en la Fase 1.

---

## Endpoint stub — Modelo TelemetryEvent para Brasaland

Tu modelo Pydantic debe aceptar el envelope definido en tu plan de la Fase 1. El campo `properties` transporta el payload específico del evento — su contenido varía por evento pero debe respetar la allowlist definida en tu `event-schemas.json`.

```python
from pydantic import BaseModel
from typing import Any
from datetime import datetime

class TelemetryEvent(BaseModel):
    eventId: str           # UUID generado en el cliente
    timestamp: datetime    # ISO 8601, momento de captura
    sessionId: str         # Identificador de sesión (opaco)
    userId: str            # UUID TinyDB del usuario (nunca nombre ni email)
    event_type: str        # Formato entidad_acción, ej: "ingredient_entry_created"
    schemaVersion: str     # Ej: "1.0"
    requestId: str         # ID de correlación — generado por TelemetryService por batch
    properties: dict[str, Any] = {}
```

> **Nota:** `service` no forma parte del envelope de captura. La capa de almacenamiento de la Fase 3 establece la columna `service` al persistir (típicamente `backoffice`).

---

## Flujo de inventario — Dónde instrumentar

Estos son los puntos del backoffice donde deben vivir las llamadas a `track()`. Los nombres de componentes son referencias — adáptalos a tu implementación real.

| Evento | Dónde llamar a `track()` | Notas |
|---|---|---|
| `ingredient_entry_created` | Tras respuesta exitosa de la API en el formulario de creación de IngredientEntry | Incluir `ingredient_id`, `quantity`, `location_id`, `supplier_name` |
| `ingredient_exit_created` | Tras respuesta exitosa de la API en el formulario de creación de IngredientExit | Incluir `ingredient_id`, `quantity`, `reason`, `location_id` |
| `ingredient_exit_failed` | En error de la API en el formulario de IngredientExit (bloque catch) | Incluir `error_code`, `ingredient_id`, `location_id` — nunca el stack de error completo |
| `ingredient_entry_failed` | En error de la API en el formulario de IngredientEntry (bloque catch) | Incluir `error_code`, `location_id` |
| `ingredient_list_viewed` | Al montar el componente de listado de stock de ingredientes | Incluir `location_id`, `item_count` |

---

## Flujo de autenticación — Dónde instrumentar (Actividad adicional)

| Evento | Dónde llamar a `track()` | Notas |
|---|---|---|
| `user_login_succeeded` | Tras respuesta exitosa de autenticación en TinyDB | Incluir `location_id` si está disponible en el momento del login — nunca incluir email ni contraseña |
| `user_login_failed` | En respuesta de auth fallida (bloque catch o estado de error) | Incluir `reason`: `invalid_credentials`, `session_expired` o `network_error` — nunca la contraseña ni el email introducidos |
| `session_expired` | Cuando se detecta la expiración del token (middleware o hook de auth) | Incluir `sessionId` de la sesión expirada |

---

## Allowlists de propiedades por evento

Cada llamada a `track()` para Brasaland debe incluir solo estas propiedades. Nada más.

| Evento | Propiedades permitidas |
|---|---|
| `ingredient_entry_created` | `ingredient_id`, `quantity`, `location_id`, `supplier_name` |
| `ingredient_exit_created` | `ingredient_id`, `quantity`, `reason`, `location_id` |
| `ingredient_exit_failed` | `error_code`, `ingredient_id`, `location_id` |
| `ingredient_entry_failed` | `error_code`, `location_id` |
| `ingredient_list_viewed` | `location_id`, `item_count` |
| `user_login_succeeded` | `location_id` |
| `user_login_failed` | `reason` |
| `session_expired` | *(sin propiedades adicionales más allá del envelope)* |

---

## Restricciones de negocio para tu implementación

- **La doble moneda es metadato, no telemetría:** COP/USD es una propiedad de la entidad `Ingredient` en Supabase. No incluyas valores monetarios ni importes en eventos de telemetría — son datos de negocio, no datos de uso.
- **`location_id` es obligatorio** en todos los eventos de inventario (entero 1–14). Sin él, Nicolás Park (CTO) no puede segmentar los datos por Colombia vs. Florida en el dashboard.
- **`reason` en IngredientExit** (`consumption` o `waste`) debe incluirse en `ingredient_exit_created` — es lo que alimenta el KPI de ratio de merma.
- **`userId` es siempre el UUID de TinyDB** — nunca el nombre ni el email del gerente.

---

_Brasaland Digital — Documento interno para el AI Engineering Track de 4Geeks Academy_
