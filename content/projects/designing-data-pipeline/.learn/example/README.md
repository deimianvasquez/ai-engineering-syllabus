# Riverside Public Library — Loan Activity Pipeline (Class Example)

> **For instructors:** Parallel classroom scenario for `designing-data-pipeline`. Same spine (ETL design doc, CSV format analysis, data flow diagram, deduplication for updates-as-inserts, idempotency, execution log, robustness criteria), different domain. Students still follow the full Veridian Logistics brief in the project root `README.md`.

_Estas instrucciones también están disponibles en [español](./README.es.md)._

---

## The challenge

**Riverside Public Library** runs a legacy circulation system across three branches. Every night it exports a single CSV of loan activity: new checkouts, renewals, returns, and overdue notices. When a loan moves from _checked out_ to _returned_, the system **appends a new row** instead of updating the original — so the same `loan_id` can appear multiple times with different statuses.

Ops wants reliable weekly reports (active loans per branch, overdue rate) but any pipeline that loads rows blindly double-counts active loans.

In one session, draft a **mini `PIPELINE_DESIGN.md`** — no code.

### Scope note

| Graded project (`designing-data-pipeline`) | This class example                         |
| ------------------------------------------ | ------------------------------------------ |
| Veridian Logistics / five hubs / shipments | Riverside Library / three branches / loans |
| Full CTO brief + all rubric sections       | Same section headings, smaller narrative   |
| Multi-hub freight metrics                  | Branch-level loan KPIs                     |
| Student repo + commit                      | Local markdown only                        |

---

## What to build

Create `PIPELINE_DESIGN.md` (throwaway folder or demo repo) with these sections:

### 1. Purpose

- [ ] State the duplicate-row problem (status updates as inserts).
- [ ] Name outputs: e.g. `reporting.fact_loans` (one row per `loan_id`) and `reporting.daily_branch_metrics`.

### 2. Data format analysis

- [ ] When is CSV fine at source? When would you use Parquet or typed staging?
- [ ] One justified recommendation per pipeline zone (raw / staging / reporting).

### 3. Data flow diagram

- [ ] Mermaid or ASCII: source → extract → transform (dedup here) → load → destination.
- [ ] Label where idempotency is enforced.

### 4. Deduplication strategy

- [ ] Business key: `loan_id` (and `branch_id` if loans can transfer).
- [ ] Rule: keep latest row by `event_timestamp` across **all files in the batch**.
- [ ] Note one edge case (e.g. renewal then return same night).

### 5. Idempotency plan

- [ ] Describe failure mid-load and safe retry (staging table, transactional merge, or `run_id` checkpoint).
- [ ] Explain why re-running does not duplicate `fact_loans` rows.

### 6. Execution log (minimum five fields)

| Field              | Why it matters                 |
| ------------------ | ------------------------------ |
| `run_id`           | Trace one execution            |
| `source_files`     | Audit which nightly export ran |
| `rows_extracted`   | Detect empty/truncated files   |
| `rows_after_dedup` | Measure duplicate pressure     |
| `status`           | Alerting                       |

Add at least one more field with rationale.

### 7. Robustness criteria

- [ ] List three concrete traits (schema validation, quarantine, alerting, raw retention, etc.) — not generic "good code."

---

## Verify together

- [ ] Dedup addresses updates-as-inserts, not just `DISTINCT` within one file.
- [ ] Diagram shows dedup **before** reporting merge.
- [ ] Idempotency mechanism is specific (not "run again").
- [ ] Format section includes trade-offs, not format definitions only.
- [ ] No Python/SQL implementation files — design doc only.

---

## Discussion questions

1. Why must deduplication run across the whole nightly batch instead of per CSV file?
2. What breaks if you use `returned_at` as the ordering column when some returns lack that field?
3. How would you extend this design if the library adds real-time API events alongside the nightly CSV?
