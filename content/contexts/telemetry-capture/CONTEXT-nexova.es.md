# CONTEXT — Nexova · Telemetría Fase 2: Captura desde el Frontend

## Tu empresa

**Nexova** es una consultora de recursos humanos y adquisición de talento con oficinas en Valencia (España) y Miami (Florida). Formas parte del equipo interno de Ingeniería de IA. El backoffice lo usan a diario los operadores de RRHH y consultores para registrar entradas de activos (compras/entregas) y salidas de activos (asignaciones y consumos). Hoy instrumentas ese backoffice con los eventos que diseñaste en la Fase 1.

---

## Endpoint stub — Modelo TelemetryEvent para Nexova

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
    event_type: str        # Formato entidad_acción, ej: "asset_exit_created"
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
| `asset_entry_created` | Tras respuesta exitosa de la API en el formulario de creación de AssetEntry | Incluir `asset_id`, `quantity`, `office`, `supplier` |
| `asset_exit_created` | Tras respuesta exitosa de la API en el formulario de creación de AssetExit | Incluir `asset_id`, `quantity`, `office`, `exit_type` — nunca el nombre del empleado en telemetría |
| `asset_exit_failed` | En error de la API en el formulario de AssetExit (bloque catch) | Incluir `error_code`, `asset_id`, `office` |
| `asset_entry_failed` | En error de la API en el formulario de AssetEntry (bloque catch) | Incluir `error_code`, `office` |
| `asset_list_viewed` | Al montar el componente de listado de stock de activos | Incluir `office`, `item_count` |

---

## Flujo de autenticación — Dónde instrumentar (Actividad adicional)

| Evento | Dónde llamar a `track()` | Notas |
|---|---|---|
| `user_login_succeeded` | Tras respuesta exitosa de autenticación en TinyDB | Incluir `office` si es determinable en el momento del login — nunca incluir email ni contraseña |
| `user_login_failed` | En respuesta de auth fallida (bloque catch o estado de error) | Incluir `reason`: `invalid_credentials`, `session_expired` o `network_error` — nunca la contraseña ni el email introducidos |
| `session_expired` | Cuando se detecta la expiración del token (middleware o hook de auth) | Incluir `sessionId` de la sesión expirada |

---

## Allowlists de propiedades por evento

Cada llamada a `track()` para Nexova debe incluir solo estas propiedades. Nada más.

| Evento | Propiedades permitidas |
|---|---|
| `asset_entry_created` | `asset_id`, `quantity`, `office`, `supplier` |
| `asset_exit_created` | `asset_id`, `quantity`, `office`, `exit_type` |
| `asset_exit_failed` | `error_code`, `asset_id`, `office` |
| `asset_entry_failed` | `error_code`, `office` |
| `asset_list_viewed` | `office`, `item_count` |
| `user_login_succeeded` | `office` |
| `user_login_failed` | `reason` |
| `session_expired` | *(sin propiedades adicionales más allá del envelope)* |

---

## Restricciones de negocio para tu implementación

- **`office` es obligatorio** en todos los eventos de inventario (`"Valencia"` / `"Miami"`). Sin él, Sergio Molina (CTO) no puede segmentar los datos de uso por país.
- **`exit_type` en AssetExit** debe ser `allocation` o `consumption` — inclúyelo en `asset_exit_created`.
- **`assigned_to` nunca debe aparecer en telemetría** como nombre ni email. Las referencias a empleados pertenecen a los datos de negocio en Supabase, no a eventos de uso.
- **`userId` es siempre el UUID de TinyDB** del operador que realiza la acción — nunca el identificador del empleado asignado.

---

_Nexova AI Engineering Team — Documento interno para el AI Engineering Track de 4Geeks Academy_
