# CONTEXT — TrackFlow · Telemetría Fase 4: Reporte desde los Datos

## Tu empresa

**TrackFlow** es una empresa de gestión de almacenes y entrega de última milla con operaciones en Los Ángeles (EE. UU.) y Zaragoza (España). Formas parte de **TrackFlow Tech**. La tabla `telemetry_events` está poblada con eventos reales del backoffice. Hoy construyes el pipeline que convierte esos eventos en las métricas que necesitan Ana Whitfield (Directora de Operaciones de Almacén) y Thomas Harry (CEO).

---

## Tus dos métricas

Estos son los dos cálculos de KPI que debe implementar tu `analysis.py`. Cada uno corresponde directamente a los KPIs definidos en tu plan de la Fase 1.

### Métrica 1 — Volumen de salidas de stock por día y almacén

**Pregunta de negocio:** ¿cuántos eventos de salida de stock (despachos) se crearon por día, segmentados por almacén?

**Responde el KPI:** Tasa de cumplimiento de pedidos — las tendencias de volumen revelan patrones de capacidad antes de que se produzcan incumplimientos de SLA.

```python
# Pseudocódigo — implementar solo con operaciones de Pandas
def stock_exit_volume_per_day_by_warehouse(start_date, end_date):
    # Cargar desde telemetry_events donde event_type = 'stock_exit_created'
    # y tags.exit_type = 'dispatch'
    # y timestamp entre start_date y end_date
    # Convertir timestamp a datetime (utc=True)
    # Extraer fecha del timestamp
    # Extraer warehouse del JSONB de tags
    # groupby(['date', 'warehouse'])['id'].count()
    # Devolver como lista de dicts: [{ "date": "...", "warehouse": "...", "count": N }]
```

**Dimensión de agrupamiento:** fecha + warehouse (de `tags`).
**Agregación:** `.count()` sobre el `id` del evento.

---

### Métrica 2 — Tasa de fallos de salida de stock por día y almacén

**Pregunta de negocio:** ¿qué proporción de intentos de salida de stock fallaron cada día, por almacén?

**Responde el KPI:** Tasa de cumplimiento de pedidos — la tasa de fallos mide directamente el inverso del éxito de cumplimiento.

```python
# Pseudocódigo — implementar solo con operaciones de Pandas
def stock_exit_failure_rate_per_day(start_date, end_date):
    # Cargar desde telemetry_events donde event_type IN (
    #   'stock_exit_created', 'stock_exit_failed'
    # ) y timestamp entre start_date y end_date
    # Convertir timestamp a datetime (utc=True)
    # Extraer fecha y warehouse de tags
    # Crear columna booleana: is_failure = event_type == 'stock_exit_failed'
    # groupby(['date', 'warehouse']).agg(total=('id', 'count'), failures=('is_failure', 'sum'))
    # Calcular failure_rate = failures / total
    # Devolver como lista de dicts: [{ "date": "...", "warehouse": "...", "total": N, "failures": M, "failure_rate": 0.05 }]
```

**Dimensión de agrupamiento:** fecha + warehouse.
**Agregación:** `.agg()` con count y sum, luego ratio derivado.

---

## Ejemplo de JSON esperado

```json
{
  "period": { "from": "2025-01-13", "to": "2025-01-20" },
  "metrics": {
    "stock_exit_volume_per_day_by_warehouse": [
      { "date": "2025-01-13", "warehouse": "LA", "count": 87 },
      { "date": "2025-01-13", "warehouse": "ZGZ", "count": 34 }
    ],
    "stock_exit_failure_rate_per_day": [
      {
        "date": "2025-01-13",
        "warehouse": "LA",
        "total": 90,
        "failures": 3,
        "failure_rate": 0.033
      },
      {
        "date": "2025-01-13",
        "warehouse": "ZGZ",
        "total": 35,
        "failures": 1,
        "failure_rate": 0.029
      }
    ]
  }
}
```

---

## Actividad adicional — Tasa de fallos de autenticación

Si instrumentaste los eventos de autenticación en D47, implementa:

**Pregunta de negocio:** ¿qué porcentaje de intentos de login fallan cada día, por almacén?

```python
# event_type IN ('user_login_succeeded', 'user_login_failed')
# groupby(['date', 'warehouse de tags'])
# failure_rate = failed / (failed + succeeded)
```

---

## Restricciones de negocio para tu pipeline

- **`warehouse` debe venir de `tags`**, no de una columna fija. Extráelo con Pandas: `df['warehouse'] = df['tags'].apply(lambda x: x.get('warehouse'))` — luego filtra las filas donde sea nulo antes de agrupar.
- **Los Ángeles (`LA`) y Zaragoza (`ZGZ`) deben estar siempre segmentadas** — Thomas Harry nunca aceptará un número global que mezcle ambos almacenes. Si `warehouse` falta en una fila, exclúyela de la métrica en lugar de agruparla bajo un valor nulo.
- **Salidas por pérdida** (`exit_type = loss`) pueden extraerse de `tags` en una tercera función si implementas la actividad adicional — carga `stock_exit_created` con SQL, extrae `exit_type` en Pandas, luego filtra antes de agrupar.

---

_TrackFlow Tech — Documento interno para el AI Engineering Track de 4Geeks Academy_
