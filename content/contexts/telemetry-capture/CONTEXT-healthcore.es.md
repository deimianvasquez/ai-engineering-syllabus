# CONTEXT — HealthCore · Telemetría Fase 2: Captura desde el Frontend

## Tu empresa

**HealthCore** es una empresa de servicios sanitarios ambulatorios con 12 clínicas en EE. UU. y Reino Unido. Formas parte de **HealthCore Digital**, el equipo interno de tecnología. El backoffice lo usan a diario los administradores y gestores de clínica para registrar entregas de suministros y consumos de suministros. Hoy instrumentas ese backoffice con los eventos que diseñaste en la Fase 1.

Esta es la instrumentación de mayor riesgo del programa. Los datos fluyen por un entorno regulado — HIPAA en EE. UU., UK GDPR en Reino Unido. Cada propiedad que incluyas en un evento de telemetría debe haber superado la pregunta: *"¿Podría vincularse, directa o indirectamente, a un paciente?"* Si la respuesta es sí, no va en telemetría.

---

## Endpoint stub — Modelo TelemetryEvent para HealthCore

Tu modelo Pydantic debe aceptar el envelope definido en tu plan de la Fase 1. El campo `properties` transporta el payload específico del evento — su contenido varía por evento pero debe respetar la allowlist definida en tu `event-schemas.json`.

```python
from pydantic import BaseModel
from typing import Any
from datetime import datetime

class TelemetryEvent(BaseModel):
    eventId: str           # UUID generado en el cliente
    timestamp: datetime    # ISO 8601, momento de captura
    sessionId: str         # Identificador de sesión (opaco)
    userId: str            # UUID TinyDB del usuario (nunca nombre ni email del personal)
    event_type: str        # Formato entidad_acción, ej: "supply_consumption_created"
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
| `supply_delivery_created` | Tras respuesta exitosa de la API en el formulario de creación de SupplyDelivery | Incluir `supply_id`, `quantity`, `clinic_id`, `country` |
| `supply_consumption_created` | Tras respuesta exitosa de la API en el formulario de creación de SupplyConsumption | Incluir `supply_id`, `quantity`, `consumption_type`, `clinic_id`, `country` — nunca identificadores de paciente |
| `supply_consumption_failed` | En error de la API en el formulario de SupplyConsumption (bloque catch) | Incluir `error_code`, `supply_id`, `clinic_id`, `country` |
| `supply_list_viewed` | Al montar el componente de listado de material médico | Incluir `clinic_id`, `country`, `item_count` |

---

## Flujo de autenticación — Dónde instrumentar (Actividad adicional)

| Evento | Dónde llamar a `track()` | Notas |
|---|---|---|
| `user_login_succeeded` | Tras respuesta exitosa de autenticación en TinyDB | Incluir `country` si es determinable en el momento del login — nunca incluir email ni contraseña |
| `user_login_failed` | En respuesta de auth fallida (bloque catch o estado de error) | Incluir `reason`: `invalid_credentials`, `session_expired` o `network_error` — nunca la contraseña ni el email introducidos |
| `session_expired` | Cuando se detecta la expiración del token (middleware o hook de auth) | Incluir `sessionId` de la sesión expirada — Claire Whitfield (CCO) requiere el seguimiento de expiración de sesiones para los registros de auditoría de acceso |

---

## Allowlists de propiedades por evento

Cada llamada a `track()` para HealthCore debe incluir solo estas propiedades. Nada más.

| Evento | Propiedades permitidas |
|---|---|
| `supply_delivery_created` | `supply_id`, `quantity`, `clinic_id`, `country` |
| `supply_consumption_created` | `supply_id`, `quantity`, `consumption_type`, `clinic_id`, `country` |
| `supply_consumption_failed` | `error_code`, `supply_id`, `clinic_id`, `country` |
| `supply_list_viewed` | `clinic_id`, `country`, `item_count` |
| `user_login_succeeded` | `country` |
| `user_login_failed` | `reason` |
| `session_expired` | *(sin propiedades adicionales más allá del envelope)* |

---

## Restricciones de negocio para tu implementación

- **`country` es obligatorio** en todos los eventos de inventario (`"US"` / `"UK"`). Claire Whitfield (CCO) exige segmentación por país en todos los informes de cumplimiento — un evento sin `country` no puede usarse en ninguna auditoría.
- **`clinic_id` es obligatorio** en todos los eventos de inventario (entero 1–12). Sin él, el Dr. Reid (Director de Operaciones Clínicas) no puede identificar qué clínica está experimentando escasez de material.
- **`consumption_type` nunca debe inferirse** — debe provenir directamente del valor que el usuario ha seleccionado en el formulario (`clinical_use` o `expiry_waste`). Nunca lo asumas ni lo defaults.
- **Sin identificadores de paciente, nunca.** Los eventos de SupplyConsumption describen una acción del personal clínico, no un encuentro con un paciente. Si tu implementación llega a incluir el nombre de un paciente, su ID, fecha de nacimiento, diagnóstico o cualquier otro campo vinculado a un paciente en un evento de telemetría, detente y elimínalo. Esta es una frontera infranqueable bajo HIPAA y UK GDPR.
- **`userId` es siempre el UUID de TinyDB** del administrador de la clínica que realiza la acción — nunca su nombre, email ni título de rol clínico.

---

_HealthCore Digital — Documento interno para el AI Engineering Track de 4Geeks Academy_
