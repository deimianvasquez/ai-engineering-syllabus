# CONTEXT — TrackFlow · Telemetría Fase 3: Almacenamiento en el Backend

## Tu empresa

**TrackFlow** es una empresa de gestión de almacenes y entrega de última milla con operaciones en Los Ángeles (EE. UU.) y Zaragoza (España). Formas parte de **TrackFlow Tech**. El `TelemetryService` del backoffice ya está enviando batches de eventos al stub. Hoy reemplazas ese stub por la capa de almacenamiento real.

---

## Qué va en `tags` por cada evento

La columna `tags` JSONB almacena las propiedades específicas del evento de tu allowlist. Esto es lo que Supabase recibirá y guardará para cada evento de TrackFlow.

| `event_type` | Contenido de `tags` |
|---|---|
| `stock_entry_created` | `{ "sku_id": 42, "quantity": 200, "warehouse": "LA", "reference": "PO-2025-8841" }` |
| `stock_exit_created` | `{ "sku_id": 42, "quantity": 15, "warehouse": "ZGZ", "exit_type": "dispatch" }` |
| `stock_exit_failed` | `{ "error_code": "INSUFFICIENT_STOCK", "sku_id": 42, "warehouse": "LA", "exit_type": "dispatch" }` |
| `stock_entry_failed` | `{ "error_code": "INVALID_REFERENCE", "warehouse": "ZGZ" }` |
| `sku_list_viewed` | `{ "warehouse": "LA", "item_count": 142 }` |
| `user_login_succeeded` | `{ "warehouse": "ZGZ" }` |
| `user_login_failed` | `{ "reason": "invalid_credentials" }` |
| `session_expired` | `{}` |

Las columnas fijas (`event_type`, `timestamp`, `service`, `level`) se populan desde los campos del envelope. La capa de almacenamiento establece `service` en `backoffice` al persistir — no se envía en el envelope de captura. La columna `value` puede usarse para `quantity` en eventos de entradas/salidas de stock si quieres que sea consultable sin parsear JSONB — documenta tu decisión.

---

## Bulk insert — Notas específicas de TrackFlow

Los picos de tráfico de TrackFlow coinciden con las ventanas de despacho de e-commerce: Black Friday, temporada de Navidad, ventas flash de clientes de moda. Durante estos períodos, los operarios de Los Ángeles pueden generar cientos de eventos `stock_exit_created` y `stock_exit_failed` en poco tiempo. Tu bulk insert debe absorber estas ráfagas sin acumular transacciones.

**Ejemplo de rechazo para TrackFlow:** llega un batch de 6 eventos. El evento 4 es un `stock_exit_failed` sin `warehouse` en `tags` — falla la validación. Los eventos 1, 2, 3, 5 y 6 son válidos y se insertan. La respuesta es `{ "received": 6, "stored": 5, "rejected": 1 }`. Un `stock_exit_failed` sin `warehouse` es operativamente inútil — Andrés Kim (CTO) no puede atribuir el fallo a ninguno de los dos almacenes.

---

## Checklist de verificación para TrackFlow

Después de reemplazar el stub, verifica en el editor de tablas de Supabase:

- [ ] Todos los eventos de órdenes tienen `warehouse` en `tags` (`"LA"` o `"ZGZ"`) — Thomas Harry (CEO) exige segmentación por almacén en cada vista
- [ ] Las filas `stock_exit_created` tienen `exit_type` en `tags` — necesario para el análisis de despacho vs. pérdida
- [ ] Los valores de `reference` en `tags` son referencias de despacho del cliente — nunca direcciones ni teléfonos de destinatarios
- [ ] Ninguna fila contiene nombres de destinatarios, direcciones de entrega ni números de teléfono en ninguna parte de `tags`
- [ ] Las filas `stock_exit_failed` siempre tienen tanto `warehouse` como `exit_type` aunque falten otras propiedades

---

_TrackFlow Tech — Documento interno para el AI Engineering Track de 4Geeks Academy_
