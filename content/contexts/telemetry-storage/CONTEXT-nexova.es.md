# CONTEXT — Nexova · Telemetría Fase 3: Almacenamiento en el Backend

## Tu empresa

**Nexova** es una consultora de recursos humanos y adquisición de talento con oficinas en Valencia (España) y Miami (Florida). Formas parte del equipo interno de Ingeniería de IA. El `TelemetryService` del backoffice ya está enviando batches de eventos al stub. Hoy reemplazas ese stub por la capa de almacenamiento real.

---

## Qué va en `tags` por cada evento

La columna `tags` JSONB almacena las propiedades específicas del evento de tu allowlist. Esto es lo que Supabase recibirá y guardará para cada evento de Nexova.

| `event_type` | Contenido de `tags` |
|---|---|
| `asset_entry_created` | `{ "asset_id": 8, "quantity": 5, "office": "Valencia", "supplier": "Dell Technologies" }` |
| `asset_exit_created` | `{ "asset_id": 8, "quantity": 1, "office": "Miami", "exit_type": "allocation" }` |
| `asset_exit_failed` | `{ "error_code": "INSUFFICIENT_STOCK", "asset_id": 8, "office": "Valencia" }` |
| `asset_entry_failed` | `{ "error_code": "UNKNOWN_SUPPLIER", "office": "Miami" }` |
| `asset_list_viewed` | `{ "office": "Valencia", "item_count": 18 }` |
| `user_login_succeeded` | `{ "office": "Miami" }` |
| `user_login_failed` | `{ "reason": "session_expired" }` |
| `session_expired` | `{}` |

Las columnas fijas (`event_type`, `timestamp`, `service`, `level`) se populan desde los campos del envelope. La capa de almacenamiento establece `service` en `backoffice` al persistir — no se envía en el envelope de captura. La columna `value` puede usarse para `quantity` en eventos de entradas/salidas de activos si quieres que sea consultable sin parsear JSONB — documenta tu decisión.

---

## Bulk insert — Notas específicas de Nexova

Las oficinas de Valencia y Miami operan en zonas horarias distintas. Los días de incorporación de nuevos empleados — cuando varios `asset_exit_created` se disparan en secuencia — son los momentos de mayor tráfico para el sistema de telemetría. Tu bulk insert debe manejar ráfagas de eventos de salida sin degradar el tiempo de respuesta del backoffice.

**Ejemplo de rechazo para Nexova:** llega un batch de 4 eventos. El evento 2 es un `asset_exit_created` sin el campo `office` en `tags` — falla la validación. Los eventos 1, 3 y 4 son válidos y se insertan. La respuesta es `{ "received": 4, "stored": 3, "rejected": 1 }`. Sin `office`, Sergio Molina (CTO) no puede segmentar Valencia vs. Miami — el evento se descarta correctamente.

---

## Checklist de verificación para Nexova

Después de reemplazar el stub, verifica en el editor de tablas de Supabase:

- [ ] Las filas `asset_entry_created` y `asset_exit_created` tienen `office` en `tags` — sin él la segmentación entre oficinas es imposible
- [ ] Las filas `asset_exit_created` **no** contienen nombres ni emails de empleados en `tags`
- [ ] Las filas `asset_exit_failed` tienen tanto `error_code` como `asset_id` en `tags` — necesarios para identificar qué tipo de activo genera más fricciones
- [ ] Ninguna fila contiene claves de licencia de software ni valores de contratos con proveedores en ninguna parte de `tags`

---

_Nexova AI Engineering Team — Documento interno para el AI Engineering Track de 4Geeks Academy_
