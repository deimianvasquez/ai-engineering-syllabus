# CONTEXT — TrackFlow · Telemetría Fase 2: Captura desde el Frontend

## Tu empresa

**TrackFlow** es una empresa de gestión de almacenes y entrega de última milla con operaciones en Los Ángeles (EE. UU.) y Zaragoza (España). Formas parte de **TrackFlow Tech**, el equipo interno de tecnología. El backoffice lo usan a diario los operarios de almacén y coordinadores para registrar entradas de stock (recepciones de mercancía) y salidas de stock (despachos y pérdidas). Hoy instrumentas ese backoffice con los eventos que diseñaste en la Fase 1.

---

## Endpoint stub — Modelo TelemetryEvent para TrackFlow

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
    event_type: str        # Formato entidad_acción, ej: "stock_exit_created"
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
| `stock_entry_created` | Tras respuesta exitosa de la API en el formulario de creación de StockEntry | Incluir `sku_id`, `quantity`, `warehouse`, `reference` |
| `stock_exit_created` | Tras respuesta exitosa de la API en el formulario de creación de StockExit | Incluir `sku_id`, `quantity`, `warehouse`, `exit_type` |
| `stock_exit_failed` | En error de la API en el formulario de StockExit (bloque catch) | Incluir `error_code`, `sku_id`, `warehouse`, `exit_type` |
| `stock_entry_failed` | En error de la API en el formulario de StockEntry (bloque catch) | Incluir `error_code`, `warehouse` |
| `sku_list_viewed` | Al montar el componente de listado de stock de SKUs | Incluir `warehouse`, `item_count` |

---

## Flujo de autenticación — Dónde instrumentar (Actividad adicional)

| Evento | Dónde llamar a `track()` | Notas |
|---|---|---|
| `user_login_succeeded` | Tras respuesta exitosa de autenticación en TinyDB | Incluir `warehouse` si es determinable en el momento del login — nunca incluir email ni contraseña |
| `user_login_failed` | En respuesta de auth fallida (bloque catch o estado de error) | Incluir `reason`: `invalid_credentials`, `session_expired` o `network_error` — nunca la contraseña ni el email introducidos |
| `session_expired` | Cuando se detecta la expiración del token (middleware o hook de auth) | Incluir `sessionId` de la sesión expirada |

---

## Allowlists de propiedades por evento

Cada llamada a `track()` para TrackFlow debe incluir solo estas propiedades. Nada más.

| Evento | Propiedades permitidas |
|---|---|
| `stock_entry_created` | `sku_id`, `quantity`, `warehouse`, `reference` |
| `stock_exit_created` | `sku_id`, `quantity`, `warehouse`, `exit_type` |
| `stock_exit_failed` | `error_code`, `sku_id`, `warehouse`, `exit_type` |
| `stock_entry_failed` | `error_code`, `warehouse` |
| `sku_list_viewed` | `warehouse`, `item_count` |
| `user_login_succeeded` | `warehouse` |
| `user_login_failed` | `reason` |
| `session_expired` | *(sin propiedades adicionales más allá del envelope)* |

---

## Restricciones de negocio para tu implementación

- **`warehouse` es obligatorio** en todos los eventos de inventario (`"LA"` / `"ZGZ"`). Thomas Harry (CEO) exige segmentación por almacén en toda vista del dashboard — un evento sin este campo es inútil para decisiones operativas.
- **`exit_type` en StockExit** debe ser `dispatch` o `loss` — inclúyelo en `stock_exit_created` y en eventos de fallo.
- **`reference` en StockEntry** es la referencia de despacho del cliente — inclúyela en eventos de entrada exitosos cuando esté disponible en la respuesta de la API.
- **`userId` es siempre el UUID de TinyDB** del operario que realiza la acción — nunca su nombre ni email.
- **Sin datos del cliente final en telemetría:** los eventos de salida de stock registran la acción del operario, no la del destinatario. Nunca incluyas nombre, dirección ni teléfono del destinatario en ninguna propiedad de telemetría.

---

_TrackFlow Tech — Documento interno para el AI Engineering Track de 4Geeks Academy_
