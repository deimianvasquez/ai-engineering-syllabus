# Building Bullet-Proof Applications - Reference Solution

## Purpose

This reference solution describes the expected architecture, implementation scope, and validation evidence for a complete submission.

## Solution Structure

- `app/models/` for persistence models and schema contracts.
- `app/services/` for business logic and route-independent operations.
- `app/routes/` (or equivalent) for API endpoint definitions.
- `app/core/security.py` (or equivalent) for JWT, password hashing, and auth dependencies.
- `tests/` for route, service, and auth behavior tests.

## Required Coverage (From README)

- Create a `TESTING.md` file at the root of your project documenting: how to run the tests, what each test suite covers, and which cases you decided to include and why.
- Before writing any test, list in `TESTING.md` the cases you plan to cover: happy path, edge cases, and failure modes for each endpoint.
- Create a `tests/` directory at the root of your FastAPI project.
- Write a test module for each authentication endpoint (e.g., `test_register.py`, `test_login.py`, `test_token.py`).
- For each endpoint, implement at minimum:
- One happy-path test (valid input, expected response)
- One edge-case test (boundary input: empty field, duplicate user, etc.)
- One failure-mode test (invalid credentials, expired token, malformed request)

## Expected API Surface

- Implement and validate the required routes from the README.

## Key Implementation Decisions

- Passwords are never stored in plain text; use `passlib` with `bcrypt`.
- JWT creation/validation is centralized in one security module.
- `get_current_user` is used as a reusable dependency on protected routes.
- Secret keys and token TTL come from environment variables.
- Unauthorized access returns `401`; forbidden ownership actions return `403`.

## Indicative Examples

### Example: Login success response

```json
{
  "access_token": "<jwt-token>",
  "token_type": "bearer"
}
```

### Example: Accessing a protected route without token

```json
{
  "detail": "Not authenticated"
}
```

### Example: Ownership violation

```json
{
  "detail": "Forbidden"
}
```

## Validation Notes

- Verify register -> login -> authenticated request flow in `/docs`.
- Validate invalid, malformed, and expired token scenarios.
- Confirm protected and public routes behavior matches the rubric.
- Ensure the final output remains aligned with all project evaluation criteria.
