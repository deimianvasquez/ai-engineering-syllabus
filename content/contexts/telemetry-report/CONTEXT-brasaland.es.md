# CONTEXT — Brasaland · Telemetría Fase 4: Reporte desde los Datos

## Tu empresa

**Brasaland** es una cadena de restaurantes de comida a la brasa con 14 locales en Colombia y Florida. Formas parte de **Brasaland Digital**. La tabla `telemetry_events` está poblada con eventos reales del backoffice. Hoy construyes el pipeline que convierte esos eventos en las métricas que necesitan Felipe Guerrero (Director de Operaciones) y Mariana Restrepo (CEO).

---

## Tus dos métricas

Estos son los dos cálculos de KPI que debe implementar tu `analysis.py`. Cada uno corresponde directamente a los KPIs definidos en tu plan de la Fase 1.

### Métrica 1 — Consumo diario por local

**Pregunta de negocio:** ¿cuántos eventos de salida de ingredientes (consumo) se registraron por día, segmentados por local?

**Responde el KPI:** Tasa de consumo diario por ingrediente y local.

```python
# Pseudocódigo — implementar solo con operaciones de Pandas
def consumption_by_location_per_day(start_date, end_date):
    # Cargar desde telemetry_events donde event_type = 'ingredient_exit_created'
    # y tags.reason = 'consumption'
    # y timestamp entre start_date y end_date
    # Convertir timestamp a datetime (utc=True)
    # Extraer fecha del timestamp
    # Extraer location_id del JSONB de tags
    # groupby(['date', 'location_id'])['id'].count()
    # Devolver como lista de dicts: [{ "date": "...", "location_id": N, "count": N }]
```

**Dimensión de agrupamiento:** fecha + location_id (de `tags`).
**Agregación:** `.count()` sobre el `id` del evento.

---

### Métrica 2 — Tasa de fallos de órdenes por día

**Pregunta de negocio:** ¿qué proporción de intentos de orden (entrada + salida) fallaron cada día?

**Responde el KPI:** Frecuencia de stock agotado (indirectamente — los fallos señalan estrés en la cadena de suministro).

```python
# Pseudocódigo — implementar solo con operaciones de Pandas
def order_failure_rate_per_day(start_date, end_date):
    # Cargar desde telemetry_events donde event_type IN (
    #   'ingredient_exit_created', 'ingredient_entry_created',
    #   'ingredient_exit_failed', 'ingredient_entry_failed'
    # ) y timestamp entre start_date y end_date
    # Convertir timestamp a datetime (utc=True)
    # Extraer fecha
    # Crear columna booleana: is_failure = event_type termina en '_failed'
    # groupby('date').agg(total=('id', 'count'), failures=('is_failure', 'sum'))
    # Calcular failure_rate = failures / total
    # Devolver como lista de dicts: [{ "date": "...", "total": N, "failures": M, "failure_rate": 0.12 }]
```

**Dimensión de agrupamiento:** fecha.
**Agregación:** `.agg()` con count y sum, luego ratio derivado.

---

## Ejemplo de JSON esperado

```json
{
  "period": { "from": "2025-01-13", "to": "2025-01-20" },
  "metrics": {
    "consumption_by_location_per_day": [
      { "date": "2025-01-13", "location_id": 3, "count": 12 },
      { "date": "2025-01-13", "location_id": 7, "count": 8 }
    ],
    "order_failure_rate_per_day": [
      { "date": "2025-01-13", "total": 20, "failures": 3, "failure_rate": 0.15 }
    ]
  }
}
```

---

## Actividad adicional — Tasa de fallos de autenticación

Si instrumentaste los eventos de autenticación en D47, implementa:

**Pregunta de negocio:** ¿qué porcentaje de intentos de login fallan cada día, por local?

```python
# event_type IN ('user_login_succeeded', 'user_login_failed')
# groupby(['date', 'location_id de tags'])
# failure_rate = failed / (failed + succeeded)
```

---

## Restricciones de negocio para tu pipeline

- **`location_id` debe venir de `tags`**, no de una columna fija. Extráelo con Pandas: `df['location_id'] = df['tags'].apply(lambda x: x.get('location_id'))` — luego filtra las filas donde sea nulo antes de agrupar.
- **Colombia y Florida deben estar siempre segmentadas** en la métrica de consumo — Felipe necesita comparar ambos mercados. Mapea `location_id` (1–14) a país usando tus datos de referencia de ubicaciones.
- **El KPI de ratio de merma** (IngredientExit con `reason = waste`) puede añadirse como tercera función si implementas la actividad adicional — carga con SQL (`event_type` + timestamp), extrae `reason` de `tags` en Pandas, luego `df[df['reason'] == 'waste']` antes de agrupar.

---

_Brasaland Digital — Documento interno para el AI Engineering Track de 4Geeks Academy_
