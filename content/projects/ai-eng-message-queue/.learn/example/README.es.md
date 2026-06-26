# Ejemplo en clase: Cola de miniaturas — App de eventos universitarios

> **Para instructores:** Escenario paralelo en aula para `ai-eng-message-queue`. Misma columna vertebral (broker Redis, worker Celery, `202` + `task_id`, consulta de estado, reintentos con backoff, DLQ en base de datos, Flower, proceso worker separado), dominio distinto. Los estudiantes siguen el enunciado completo del monorepo en el `README.md` raíz del proyecto.

_Estas instrucciones también están disponibles en [inglés](./README.md)._

---

## El reto

### Nota de alcance

Este ejemplo está acotado a una sesión en vivo. Conserva los mismos patrones que el proyecto oficial del estudiante pero usa una app preconstruida de **eventos universitarios**: subida de fotos para galerías en lugar de informes de telemetría empresarial. Requisitos secundarios (workers en Kubernetes, enrutamiento multi-cola) se simplifican — ver notas abajo.

Una app de clubes universitarios permite subir fotos de eventos. Redimensionar cada imagen a miniatura bloquea el handler de subida de Flask varios segundos. Tu trabajo es encolar la generación de miniaturas y devolver inmediatamente mientras un worker procesa la cola.

> **Del ticket del tech lead:**
>
> - Redis corre como broker en Docker; API y worker comparten `REDIS_URL`.
> - `POST /events/{event_id}/photos` devuelve `202` con `task_id` — nunca espera al resize.
> - `GET /tasks/{task_id}` devuelve `pending`, `started`, `success` o `failure`.
> - Los argumentos de la tarea contienen solo `photo_id` — no bytes de imagen.
> - Tras 3 intentos fallidos, registrar `task_id`, intento y error en `dlq_tasks`.
> - El worker es un proceso separado; Flower en el puerto `5555`.

---

## Vista del código

```text
api/                     API Flask de subida (modificar solo el handler de upload)
db/
  events.db              SQLite: tablas events, photos
services/
  celery_app.py          ← configurar Celery + Redis
  tasks/
    thumbnails.py        ← implementar @app.task generate_thumbnail
  dlq.py                 ← implementar record_dlq_entry
docker-compose.yml       servicios redis + flower
uploads/originals/       Imágenes a tamaño completo en disco
uploads/thumbs/          El worker escribe miniaturas aquí
```

---

## Qué construir

### Infraestructura

- [ ] Añadir servicio `redis` (puerto `6379`, `noeviction`) y `flower` (puerto `5555`) a `docker-compose.yml`.
- [ ] `REDIS_URL=redis://localhost:6379/0` en `.env`.

### Tarea Celery

- [ ] `generate_thumbnail(photo_id: str)` — cargar fila photo, leer archivo de `uploads/originals/`, escribir thumb en `uploads/thumbs/`.
- [ ] `max_retries=3`, backoff exponencial (`countdown = 10 * 2**retries`).
- [ ] `task_time_limit=120`.
- [ ] En `MaxRetriesExceededError` → `record_dlq_entry(...)`.

### Cambios en la API

- [ ] `POST /events/{event_id}/photos` guarda archivo + fila DB, llama `generate_thumbnail.delay(photo_id)`, devuelve `202 {"task_id": "..."}`.
- [ ] `GET /tasks/{task_id}` mapea estados Celery a los valores del contrato.

### Worker + observabilidad

- [ ] Levantar worker: `celery -A services.celery_app worker --loglevel=info`.
- [ ] Registrar `task_id`, intento, estado, `duration_ms` por ejecución.
- [ ] Flower muestra tareas encoladas y completadas.

---

## Verificar juntos

- [ ] La subida devuelve `202` en menos de 200ms mientras la miniatura sigue procesándose.
- [ ] Consultar `GET /tasks/{task_id}` hasta `success`; archivo thumb existe en disco.
- [ ] Romper ruta de import PIL → observar logs de reintento con delay creciente.
- [ ] Tras 3 fallos → fila en `dlq_tasks`.
- [ ] Detener Flask, mantener worker → tarea encolada sigue completándose.
- [ ] Args de tarea en Flower muestran solo string `photo_id`, no contenido de archivo.

---

## Preguntas de discusión

1. ¿Por qué pasar `photo_id` en lugar de datos base64 de la imagen en el mensaje Celery?
2. ¿Qué pasa con tareas en vuelo si Redis reinicia sin persistencia habilitada?
3. ¿Por qué `noeviction` importa para un broker de colas pero suele ser incorrecto para caché pura?
