# CONTEXT — HealthCore · Telemetría Fase 4: Reporte desde los Datos

## Tu empresa

**HealthCore** es una empresa de servicios sanitarios ambulatorios con 12 clínicas en EE. UU. y Reino Unido. Formas parte de **HealthCore Digital**. La tabla `telemetry_events` está poblada con eventos reales del backoffice. Hoy construyes el pipeline que convierte esos eventos en las métricas que necesitan el Dr. Marcus Reid (Director de Operaciones Clínicas) y la Dra. Sandra Okonkwo (CEO).

---

## Tus dos métricas

Estos son los dos cálculos de KPI que debe implementar tu `analysis.py`. Cada uno corresponde directamente a los KPIs definidos en tu plan de la Fase 1.

### Métrica 1 — Volumen de consumo de suministros por día, clínica y país

**Pregunta de negocio:** ¿cuántos eventos de consumo de suministros se crearon por día, segmentados por clínica y país?

**Responde el KPI:** Tasa de disponibilidad de suministros críticos — el volumen por clínica revela qué localizaciones consumen suministros más rápidamente.

```python
# Pseudocódigo — implementar solo con operaciones de Pandas
def supply_consumption_volume_per_day(start_date, end_date):
    # Cargar desde telemetry_events donde event_type = 'supply_consumption_created'
    # y timestamp entre start_date y end_date
    # Convertir timestamp a datetime (utc=True)
    # Extraer fecha del timestamp
    # Extraer clinic_id y country del JSONB de tags
    # groupby(['date', 'clinic_id', 'country'])['id'].count()
    # Devolver como lista de dicts: [{ "date": "...", "clinic_id": N, "country": "...", "count": N }]
```

**Dimensión de agrupamiento:** fecha + clinic_id + country (todos de `tags`).
**Agregación:** `.count()` sobre el `id` del evento.

---

### Métrica 2 — Frecuencia de consumo clínico por día y país

**Pregunta de negocio:** ¿cuántos eventos de consumo de uso clínico ocurrieron por día, segmentados por país?

**Responde el KPI:** Frecuencia de consumo clínico — la métrica que activa los ajustes proactivos de nivel de stock.

```python
# Pseudocódigo — implementar solo con operaciones de Pandas
def clinical_consumption_per_day(start_date, end_date):
    # Cargar desde telemetry_events donde event_type = 'supply_consumption_created'
    # y tags.consumption_type = 'clinical_use'
    # y timestamp entre start_date y end_date
    # Convertir timestamp a datetime (utc=True)
    # Extraer fecha y country de tags
    # groupby(['date', 'country'])['id'].count()
    # Devolver como lista de dicts: [{ "date": "...", "country": "...", "count": N }]
```

**Dimensión de agrupamiento:** fecha + country (de `tags`).
**Agregación:** `.count()` sobre el `id` del evento.

---

## Ejemplo de JSON esperado

```json
{
  "period": { "from": "2025-01-13", "to": "2025-01-20" },
  "metrics": {
    "supply_consumption_volume_per_day": [
      { "date": "2025-01-13", "clinic_id": 1, "country": "US", "count": 42 },
      { "date": "2025-01-13", "clinic_id": 10, "country": "UK", "count": 31 }
    ],
    "clinical_consumption_per_day": [
      { "date": "2025-01-13", "country": "US", "count": 4 },
      { "date": "2025-01-13", "country": "UK", "count": 2 }
    ]
  }
}
```

---

## Actividad adicional — Tasa de fallos de autenticación

Si instrumentaste los eventos de autenticación en D47, implementa:

**Pregunta de negocio:** ¿qué porcentaje de intentos de login fallan cada día, por país?

```python
# event_type IN ('user_login_succeeded', 'user_login_failed')
# groupby(['date', 'country de tags'])
# failure_rate = failed / (failed + succeeded)
```

Claire Whitfield (CCO) exige esta métrica segmentada por país — una tasa combinada que mezcle EE. UU. y Reino Unido no es válida para informes de cumplimiento.

---

## Restricciones de negocio para tu pipeline

- **`clinic_id` y `country` deben venir de `tags`**, no de columnas fijas. Extrae ambos antes de agrupar: `df['clinic_id'] = df['tags'].apply(lambda x: x.get('clinic_id'))` — filtra las filas donde cualquiera sea nulo antes de agrupar.
- **EE. UU. y Reino Unido deben estar siempre segmentados** — Claire Whitfield (CCO) exige datos a nivel de país para cada informe de cumplimiento. Una métrica combinada que mezcle ambas jurisdicciones no tiene valor de cumplimiento.
- **Ningún dato de paciente aparecerá en tu pipeline** — si algún campo en `tags` contiene lo que parece ser un nombre de paciente, ID o diagnóstico, detente inmediatamente, no lo incluyas en ninguna métrica y escala al tech lead. Tu pipeline solo debe tocar `supply_id`, `clinic_id`, `country`, `consumption_type` y `event_type`.

---

_HealthCore Digital — Documento interno para el AI Engineering Track de 4Geeks Academy_
