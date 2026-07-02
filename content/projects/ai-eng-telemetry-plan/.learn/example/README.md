# Riverside Community Garden — Telemetry Plan (Class Example)

> **For instructors:** Parallel classroom scenario for `ai-eng-telemetry-plan`. Same spine (KPIs from context, event envelope, `entity_action` events, property allowlists, stream/batch, `telemetry-plan.md` + `event-schemas.json`), different domain. Students still follow the full monorepo brief in the project root `README.md`.

_Estas instrucciones también están disponibles en [español](./README.es.md)._

---

## The challenge

**GreenPatch Co-op** runs a small tool-lending app for community gardens: members reserve shared equipment (wheelbarrows, hoses, compost bins), check items out, and return them. Stock is never edited directly — only through **checkout** and **return** records tied to a member. The ops team cannot answer basic questions: which tools break most often, who abandons reservations, or when peak checkout happens.

In one session, draft a **mini telemetry plan** before any instrumentation code.

### Scope note

| Graded project (`ai-eng-telemetry-plan`) | This class example                            |
| ---------------------------------------- | --------------------------------------------- |
| Company CONTEXT + inventory monorepo     | Fictional GreenPatch CONTEXT (provided below) |
| ≥5 inventory-flow points + ≥2 backoffice | 3 checkout-flow points + 1 auth point         |
| ≥5 fully designed events                 | 4 events with envelopes                       |
| Full risks/exclusions rubric             | Short exclusions paragraph                    |
| PR to student monorepo                   | Local `docs/telemetry/` only                  |

---

## Mini context (use instead of CONTEXT-company.md)

**KPIs to instrument:**

1. **Tool utilization rate** — % of tools checked out at least once per week.
2. **Reservation abandonment rate** — reservations started but never checked out within 24h.
3. **Return compliance** — returns completed within the allowed window vs. overdue.

**Entities:** `Tool`, `Reservation`, `Checkout`, `Member`.  
**Rule:** `Tool.availableCount` changes only via `Checkout` / `Return`, never direct edits.

---

## What to build

Create in a throwaway folder or shared demo repo:

- `docs/telemetry/telemetry-plan.md`
- `docs/telemetry/event-schemas.json`

### 1. KPI → data mapping

- [ ] For each KPI above: what data composes it? Which API action generates it?
- [ ] Map the **checkout flow**: login → browse tools → create reservation → confirm checkout → return. Mark **3 instrumentation points** (e.g. reservation abandoned, checkout validation failed, overdue return flagged).

### 2. Event Envelope

- [ ] Document mandatory fields: `eventId`, `timestamp` (ISO 8601), `sessionId`, `userId`, `event_type`, `schemaVersion`, `requestId`, `properties`.
- [ ] State that `properties` is allowlist-only per event.

### 3. Design four events

| Event                        | Suggested processing | Notes                             |
| ---------------------------- | -------------------- | --------------------------------- |
| `reservation_created`        | batch                | Volume trends                     |
| `checkout_validation_failed` | batch                | Error patterns by tool            |
| `tool_threshold_low`         | stream               | Ops alert when availableCount low |
| `login_failed`               | stream               | Security / friction signal        |

For each event:

- [ ] Golden-rule sentence: _"We capture `[event_type]` because we need to know `[hypothesis]`, which allows us to make the decision `[decision]`."_
- [ ] Property allowlist table (name, type, required).
- [ ] Stream vs batch with **business urgency** justification.

### 4. JSON schemas

- [ ] Export the four events to `event-schemas.json` (draft-07 or documented custom structure).
- [ ] `additionalProperties: false` on `properties` objects.

### 5. Exclusions (short)

- [ ] List one event you considered and rejected (with reason).
- [ ] Note one data field you will **not** capture (e.g. member email in properties).

---

## Verify together

- [ ] Every event has hypothesis + decision; none are "just in case".
- [ ] Envelope fields consistent across all four events.
- [ ] JSON validates and matches Markdown names/properties.
- [ ] At least one stream and one batch choice with non-technical justification.
- [ ] No passwords or raw tokens in any property allowlist.

---

## Discussion questions

1. Why is `tool_threshold_low` a better stream candidate than `reservation_created`?
2. What goes wrong if `userId` is duplicated inside `properties` instead of only in the envelope?
3. How would you extend this plan to navigation events without exploding event volume?
