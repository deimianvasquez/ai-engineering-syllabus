# In-Class Example: Photo Thumbnail Queue — Campus Events App

> **For instructors:** Parallel classroom scenario for `ai-eng-message-queue`. Same spine (Redis broker, Celery worker, `202` + `task_id`, status polling, retries with backoff, DLQ in database, Flower, separate worker process), different domain. Students still follow the full monorepo brief in the project root `README.md`.

_These instructions are also available in [Spanish](./README.es.md)._

---

## The challenge

### Scope note

This example is scoped for one live classroom session. It keeps the same patterns as the official student project but uses a tiny pre-built **campus events** app: photo uploads for event galleries instead of company telemetry reports. Secondary requirements (production Kubernetes workers, multi-queue routing) are simplified — see notes below.

A university club app lets organizers upload event photos. Resizing each image to thumbnails blocks the Flask upload handler for several seconds. Your job is to enqueue thumbnail generation and return immediately while a worker processes the queue.

> **From the tech lead's ticket:**
>
> - Redis runs as broker in Docker; API and worker share `REDIS_URL`.
> - `POST /events/{event_id}/photos` returns `202` with `task_id` — never waits for resize.
> - `GET /tasks/{task_id}` returns `pending`, `started`, `success`, or `failure`.
> - Task args contain only `photo_id` — not image bytes.
> - After 3 failed attempts, record `task_id`, attempt, and error in `dlq_tasks`.
> - Worker is a separate process; Flower on port `5555`.

---

## Codebase overview

```text
api/                     Flask upload API (modify upload handler only)
db/
  events.db              SQLite: events, photos tables
services/
  celery_app.py          ← configure Celery + Redis
  tasks/
    thumbnails.py        ← implement @app.task generate_thumbnail
  dlq.py                 ← implement record_dlq_entry
docker-compose.yml       redis + flower services
uploads/originals/       Full-size images on disk
uploads/thumbs/          Worker writes thumbnails here
```

---

## What to build

### Infrastructure

- [ ] Add `redis` service (port `6379`, `noeviction`) and `flower` (port `5555`) to `docker-compose.yml`.
- [ ] `REDIS_URL=redis://localhost:6379/0` in `.env`.

### Celery task

- [ ] `generate_thumbnail(photo_id: str)` — load photo row, read file from `uploads/originals/`, write thumb to `uploads/thumbs/`.
- [ ] `max_retries=3`, exponential backoff (`countdown = 10 * 2**retries`).
- [ ] `task_time_limit=120`.
- [ ] On `MaxRetriesExceededError` → `record_dlq_entry(...)`.

### API changes

- [ ] `POST /events/{event_id}/photos` saves file + DB row, calls `generate_thumbnail.delay(photo_id)`, returns `202 {"task_id": "..."}`.
- [ ] `GET /tasks/{task_id}` maps Celery states to contract status values.

### Worker + observability

- [ ] Start worker: `celery -A services.celery_app worker --loglevel=info`.
- [ ] Log `task_id`, attempt, status, `duration_ms` per execution.
- [ ] Flower shows queued and completed tasks.

---

## Verify together

- [ ] Upload returns `202` in under 200ms while thumbnail still processing.
- [ ] Poll `GET /tasks/{task_id}` until `success`; thumb file exists on disk.
- [ ] Break PIL import path → observe retry logs with increasing delay.
- [ ] After 3 failures → row in `dlq_tasks`.
- [ ] Stop Flask, keep worker running → queued task still completes.
- [ ] Flower task args show only `photo_id` string, not file content.

---

## Discussion questions

1. Why pass `photo_id` instead of base64 image data in the Celery message?
2. What happens to in-flight tasks if Redis restarts without persistence enabled?
3. Why is `noeviction` important for a queue broker but often wrong for a pure cache?
