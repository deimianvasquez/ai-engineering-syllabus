# Backend Serialization Audit

<!-- hide -->

By [@4GeeksAcademy](https://github.com/4GeeksAcademy) and [other contributors](https://github.com/4GeeksAcademy/backend-serialization-audit/graphs/contributors) at [4Geeks Academy](https://4geeksacademy.com/)

[![build by developers](https://img.shields.io/badge/build_by-Developers-blue)](https://4geeks.com)
[![4Geeks Academy](https://img.shields.io/twitter/follow/4geeksacademy?style=social&logo=x)](https://x.com/4geeksacademy)

_Estas instrucciones están [disponibles en español](./README.es.md)._

**Before you start**: 📗 [Read the instructions](https://4geeks.com/lesson/how-to-start-a-project) on how to start a coding project.

<!-- endhide -->

---

## 🎯 Your Challenge

The backend your company has been building throughout the course is about to face real users. Before that happens, your CTO has flagged a critical concern: several API endpoints are returning raw database objects with no shape control, no field filtering, and no protection against exposing internal model fields. In a low-traffic demo environment this is invisible — at scale, it creates performance bottlenecks, security risks, and brittle client contracts.

You've been assigned to lead a backend serialization audit. The goal is not to rewrite anything from scratch, but to inspect every existing endpoint with a trained eye and bring the API up to production standards.

> Your CTO has shared the following brief:
>
> #### What we need
>
> - A written audit identifying every endpoint and its current serialization state.
> - A classification of each endpoint: which ones expose unnecessary fields, which ones lack a defined response schema, and which ones are already shaped correctly.
> - For each endpoint that needs work, a note on _what kind_ of improvement is required — not just "needs serializer", but _why_ and _what the output shape should be_.
>
> #### Minimum deliverable
>
> Every endpoint in the API must have an explicit response serializer defined before this task is considered done. No endpoint should return a raw ORM object.
>
> #### What good looks like
>
> Beyond the minimum, I expect to see payload optimization where it matters: nested relationships flattened when the client doesn't need the full object, list endpoints that return only the fields consumers actually use, and write endpoints that accept only the fields they should.

This is the kind of review that separates an API that works from an API that can be trusted. Take ownership of the full surface area of your backend and bring it up to the standard your company's frontend — and your users — deserve.

### What are serializers and why do they matter here?

Serializers define the contract between your backend and anything that consumes it. In FastAPI, Pydantic models serve this role: they validate input, shape output, and make the API's behaviour explicit and testable. Without them, your API implicitly returns whatever the ORM produces — which can include internal IDs, hashed passwords, relational noise, and unstable field names. At high traffic, this also means serializing more data than the client ever requested.

A well-designed serializer layer means:
- **Clients receive only what they need** — smaller payloads, faster responses.
- **Internal model changes don't break the API contract** — the serializer absorbs the difference.
- **Sensitive fields are never accidentally exposed** — the schema is the source of truth.

When auditing, think at three levels: _what does this endpoint receive_, _what should it return_, and _what is it actually returning today_.

---

## 🌱 How to Start the Project

This project is built on top of your company's existing monorepo. You do not need to fork a new repository.

1. Open your monorepo in your coding environment (Codespaces or local).
2. Navigate to your FastAPI application — typically under `/apps/<your-app-name>/` or the backend folder established in previous milestones.
3. Make sure your environment is running and your existing endpoints are reachable before you begin the audit.
4. Work on a dedicated branch: `git checkout -b feature/serialization-audit`.

---

## 💻 What You Need to Do

### Phase 1 — Audit

- [ ] List every endpoint in your FastAPI application (route, method, and purpose).
- [ ] For each endpoint, document its current response behaviour: does it use a `response_model`? Does it return a raw ORM object, a dict, or a typed schema?
- [ ] Classify each endpoint into one of three states:
  - **✅ Already serialized** — has an explicit `response_model` and the schema is appropriate.
  - **⚠️ Partially serialized** — has a response model but it's incomplete, over-exposes fields, or doesn't match what the client needs.
  - **❌ Not serialized** — returns a raw ORM object or an untyped dict.
- [ ] Record the audit results in a Markdown file at `docs/serialization-audit.md`.

### Phase 2 — Implementation

- [ ] Create or update Pydantic schemas for every endpoint classified as ❌ or ⚠️.
- [ ] Ensure every endpoint has an explicit `response_model` declared on its route decorator.
- [ ] For list endpoints: define a schema that returns only the fields consumers need — avoid returning full nested objects when a flat representation is sufficient.
- [ ] For write endpoints (POST, PUT, PATCH): define a separate input schema that accepts only the fields that should be writable. Do not reuse the response schema as the input schema.
- [ ] Ensure no endpoint exposes sensitive fields (e.g., hashed passwords, internal tokens, raw foreign keys when a nested object is available).
- [ ] Where a relationship is needed in the response, decide explicitly: return the full nested object, return only the related ID, or return a flat projection — and document that decision in your audit file.

### Phase 3 — Verification

- [ ] Confirm that all endpoints continue to pass any existing tests after the schema changes.
- [ ] Manually test at least three endpoints using the FastAPI interactive docs (`/docs`) and verify the response shape matches the defined schema.
- [ ] Update the audit document to mark all endpoints as ✅ once the implementation is complete.

---

## ✅ What We Will Evaluate

- [ ] Every endpoint in the application has an explicit `response_model` declared.
- [ ] Pydantic schemas are defined for both input and output where applicable — input and output schemas are not conflated.
- [ ] List endpoint schemas return only the fields necessary for the consumer — no unnecessary nesting or over-fetching.
- [ ] No endpoint exposes sensitive model fields in its response schema.
- [ ] The serialization audit document (`docs/serialization-audit.md`) exists, lists all endpoints, their original state, and the changes applied.
- [ ] The application continues to function correctly after all schema changes — no regressions.

> **Note:** The quality of the audit document is evaluated as a deliverable in itself. A complete implementation with no audit trail is not sufficient.

---

## 📦 How to Submit

Push your branch to GitHub and open a pull request against `main` with the title `feat: serialization audit and implementation`. Share the PR URL according to your instructor's instructions.

---

This and many other projects are built by students as part of the [Career Programs](https://4geeksacademy.com/compare-programs) at [4Geeks Academy](https://4geeksacademy.com). By [@4GeeksAcademy](https://github.com/4GeeksAcademy) and [other contributors](https://github.com/4GeeksAcademy/backend-serialization-audit/graphs/contributors). Find out more about [AI Engineering](https://4geeksacademy.com/en/coding-bootcamps/ai-engineering), [Data Science & Machine Learning](https://4geeksacademy.com/en/coding-bootcamps/data-science-ml), [Cybersecurity](https://4geeksacademy.com/en/coding-bootcamps/cybersecurity) and [Full-Stack Software Developer with AI](https://4geeksacademy.com/en/coding-bootcamps/full-stack-developer).
