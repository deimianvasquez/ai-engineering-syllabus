# Library Desk Queue — Tagged Service Queue (Class Example)

> **For instructors:** Parallel classroom scenario for `branch-queue`. Same spine (one deque per service tag, global ticket counter, five core operations, CLI menu, stdlib-only data structures, design discussion on concurrency), different domain. Students still follow the full bank brief in the project root `README.md`.

_These instructions are also available in [Spanish](./README.es.md)._

---

## The challenge

A neighborhood library still hands out paper slips at the help desk. Patrons wait for **returns**, **hold pickups**, or **new library cards** — each desk clerk handles only one service type. Your live demo models a **terminal queue manager** (no UI) that lets each clerk call their next patron instantly without scanning everyone in the room.

> **From the desk supervisor's spec:**
>
> - Each patron gets a **service tag**: `returns`, `pickup`, or `new_card`.
> - Record patron name, service tag, and arrival time.
> - Ticket numbers are global (1, 2, 3, …) across all services.
> - Each clerk calls the next patron **only from their service queue** — FIFO within that tag.
> - Operations: issue ticket, call next, peek next, list waiting (grouped), stats.

### Scope note

Scoped for **one live session (~60–90 min)**. Same patterns as the student project, but:

- Domain is a **library help desk**, not a bank branch.
- Single file `library_queue.py` — no starter repo.
- `DESIGN.md` is **verbal in class**; students write it for the real project.
- Full five-option CLI menu is homework if time runs short; live demo needs at least issue ticket / call next / view waiting.

---

## What to build

### Data model

- [ ] `PatronTicket` dataclass: `number` (int), `patron_name`, `service_tag` (`"returns"` | `"pickup"` | `"new_card"`), `issued_at` (`datetime`).
- [ ] `LibraryDeskQueue` class with one internal `deque` per service tag and a global ticket counter.

### Core queue operations

- [ ] `issue_ticket(patron_name, service_tag)` — enqueue in the correct service deque; return the ticket.
- [ ] `call_next(service_tag)` — dequeue and return next patron for that tag; meaningful error if empty.
- [ ] `peek_next(service_tag)` — next patron without removing.
- [ ] `list_waiting()` — dict of each tag → ordered list of waiting tickets.
- [ ] `stats()` — count per tag plus `"total"`.

| Method         | Expected behavior                                                      |
| -------------- | ---------------------------------------------------------------------- |
| `issue_ticket` | Ticket lands in the matching service deque; number increments globally |
| `call_next`    | `popleft` from the requested tag's deque only                          |
| `peek_next`    | Front of that deque, no mutation                                       |
| `list_waiting` | `{returns: [...], pickup: [...], new_card: [...]}` in FIFO order       |
| `stats`        | e.g. `{returns: 1, pickup: 0, new_card: 2, total: 3}`                  |

### CLI (minimum for live demo)

- [ ] Text menu loop:
  - Issue ticket (name + service tag).
  - Call next patron (`call_next` — prompt for tag).
  - View waiting list (`list_waiting`).
  - _(Homework if needed: stats + exit polish)_

### Correctness (demo in front of class)

- [ ] Two `returns` patrons → first issued is called first.
- [ ] `call_next("pickup")` does not remove anyone from `returns`.
- [ ] Ticket numbers never repeat across different service tags.
- [ ] Empty `call_next` / `peek_next` → caught in CLI, no crash.
- [ ] Invalid service tag rejected at issuance.

⚠️ **Stdlib only:** `collections.deque`, `datetime`.

---

## Verify together

- [ ] Issue pickup ticket, then returns ticket → `call_next("returns")` serves the returns patron, pickup still waiting.
- [ ] Issue two pickup tickets 30 seconds apart → first issued called first on `call_next("pickup")`.
- [ ] `list_waiting` order matches expected FIFO within each tag after mixed inserts.
- [ ] `stats()` counts match visible queue.
- [ ] `call_next` on empty tag prints friendly message, program continues.
- [ ] Invalid tag (e.g. `renewal`) rejected without crash.

---

## Discussion questions

1. Why does a single list of all waiting patrons make `call_next` slow as the room fills up? What operation becomes O(n)?
2. How is a tagged service queue different from a **priority** queue (like triage levels)? When would you use each?
3. If two clerks share the same `returns` deque, what mutation order on `call_next` prevents calling the same patron twice?
