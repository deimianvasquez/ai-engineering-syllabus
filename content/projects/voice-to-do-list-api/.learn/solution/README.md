# Voice Command API - Reference solution

This README defines what a correct reference implementation should include for the **Voice Command API - Talk to Your Task List** project.

The expected result is a FastAPI backend that supports in-memory CRUD for tasks and a `/instruction` endpoint that uses Groq to transform a user transcription into strict routing JSON.

## Expected deliverables

A valid solution should include:

- A FastAPI app in `src` (or equivalent backend folder) with all required routes.
- In-memory storage only (module-level list of task dictionaries).
- CORS configuration so the provided frontend can call the API.
- Environment-based Groq API key loading (`.env`, not hardcoded).
- Correct JSON responses and status codes for task endpoints and instruction routing.

## Required task data model

Each task in memory should follow this shape:

```json
{
  "id": 1,
  "title": "Buy groceries",
  "done": false
}
```

Model constraints:

- `id`: unique integer.
- `title`: non-empty string.
- `done`: boolean, default `false`.

## Required API endpoints

The reference implementation must expose:

- `GET /tasks`
  - Returns the full tasks list.
- `POST /tasks`
  - Creates a task from request body (`title` required, `done` optional).
  - Returns created object with generated `id`.
- `PUT /tasks/{task_id}`
  - Replaces a task completely for the given id.
- `PATCH /tasks/{task_id}`
  - Partially updates `title` and/or `done`.
- `DELETE /tasks/{task_id}`
  - Deletes task by id and returns confirmation payload.
- `POST /instruction`
  - Receives transcription text.
  - Calls Groq to infer routing.
  - Returns strict JSON with `endpoint`, `method`, and `params`.

## `/instruction` endpoint contract

The backend must send a system prompt that forces Groq to output only this structure:

```json
{
  "endpoint": "/tasks",
  "method": "POST",
  "params": { "title": "Buy groceries" }
}
```

Important behavior:

- No free text in model output; only JSON.
- No hardcoded intent logic in backend (avoid keyword `if/else` intent matching).
- If model output is invalid JSON, return a clear API error.

## Minimal implementation behavior

A correct solution should support at least these spoken flows:

- "add buy groceries to my list" -> `/tasks` with `POST`.
- "show my tasks" -> `/tasks` with `GET`.
- "mark task 2 as done" -> `/tasks/2` with `PATCH`.
- "delete task 1" -> `/tasks/1` with `DELETE`.

The frontend should be able to:

1. Send transcription to `/instruction`.
2. Receive routing JSON.
3. Execute follow-up request to target task endpoint.
4. Render final API response.

## Reviewer checklist

- [ ] In-memory list is the only data store (no DB, no files).
- [ ] All five CRUD task routes are implemented and functional.
- [ ] IDs are unique and task lifecycle (create/update/delete) is consistent.
- [ ] Correct HTTP codes and JSON payloads are returned.
- [ ] CORS allows calls from the provided frontend.
- [ ] Groq API key is loaded securely from env variables.
- [ ] `/instruction` calls Groq and returns valid routing JSON.
- [ ] Prompting enforces strict JSON output format.
- [ ] No hardcoded intent parser in backend logic.
- [ ] End-to-end flow works for create/list/update/delete commands.

## Notes for reviewers

- UI styling and frontend internals are out of scope for grading.
- Since storage is in memory, task data reset on server restart is expected.
- Small differences in internal code organization are acceptable if API behavior matches the contract.
