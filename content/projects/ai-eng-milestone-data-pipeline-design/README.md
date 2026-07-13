# Milestone 6 — Company's Data Pipeline Design (1/3)

<!-- hide -->

By [@marcogonzalo](https://github.com/marcogonzalo) and [other contributors](https://github.com/4GeeksAcademy/ai-engineering-company-project-monorepo/graphs/contributors) at [4Geeks Academy](https://4geeksacademy.com/)

[![build by developers](https://img.shields.io/badge/build_by-Developers-blue)](https://4geeks.com)
[![4Geeks Academy](https://img.shields.io/twitter/follow/4geeksacademy?style=social&logo=x)](https://x.com/4geeksacademy)

_Estas instrucciones están [disponibles en español](./README.es.md)._

<!-- endhide -->

## 🎯 The Challenge

> 📌 You are building on **your own fork** of the company's **[monorepo](https://github.com/4GeeksAcademy/ai-engineering-company-project-monorepo)** selected at the beginning of the course — not on a new repository.

Over the past weeks you captured telemetry events, stored them in a database, and generated basic reports with Pandas. Your tech lead now wants something more: a data pipeline that is robust, auditable, and that your team can run confidently in production.

Your CTO has sent you this brief through the team's task manager:

> > **Technical Brief — Data Pipeline (Design Phase)**
> >
> > Before writing a single line of orchestration code, I need you to document the design of our data pipeline. The data team has received an internal RFP from the operations area: they want to know exactly how data flows from the moment it is captured in the application to the moment it reaches the dashboards. They also want guarantees around idempotency and auditability before they sign off on moving this to production.
> >
> > Deliverable: a design document in Markdown, committed to the monorepo. No orchestration code yet — design first, implementation next.

### What makes a data pipeline robust?

A data pipeline is not simply a script that moves data from one place to another. A production pipeline has well-defined stages, handles failures predictably, and can be audited. The three key attributes that separate a robust pipeline from one that "just works" are:

- **Idempotency**: running the pipeline twice on the same data produces the same result — no duplicates, no corruption.
- **Observability**: every run leaves enough traces to know what happened, when, and why.
- **Recoverability**: when the pipeline fails mid-way, the next run knows exactly where to resume.

These three attributes are what your design document must demonstrate you have thought through deeply.

### Build the pipeline around a business goal

A data pipeline is not infrastructure for its own sake. It exists to achieve a **specific business goal** — a decision the company needs to make, or a metric it needs to track reliably over time.

Before you design extraction, transformation, or load stages, ask: _what question must this pipeline answer, and who will act on the answer?_ Vague goals produce vague pipelines. Concrete goals shape every design choice — which events to extract, how often to run the flow, what grain to aggregate at, and what "done" looks like for each run.

**Examples of specific goals:**

- Understand **user behavior in the backoffice** (which flows are used, where operators drop off) to **increase conversion or sales rate**.
- Measure **consumption frequency** and **inbound replenishment patterns** to **anticipate stock shortages** and prioritize restocking.

You already defined this direction in earlier milestones. Your **telemetry plan** identified the company's main KPIs; your **telemetry report** turned those KPIs into calculable metrics from stored events. Your pipeline design must **carry that thread forward**: the pipeline should reliably produce the data those KPIs need — at the right freshness, granularity, and audit trail — not merely move rows between tables.

When you write the pipeline purpose in Phase 2, tie it directly to at least one KPI from your monorepo. If a stage in your design does not support a KPI or a concrete operational decision, question whether it belongs in v1.

### Questions to help you design the pipeline

Before writing `PIPELINE_DESIGN.md`, answer in writing — even as a draft — how you would handle each case in **your** monorepo.

#### Idempotency

1. **Duplicates at the source** — How do you prevent counting the same action twice in `telemetry_events` and KPI aggregates? Which envelope field is your dedup key, and at which layer?

   <details>
   <summary>See example and hint</summary>

   An operator confirms `outbound_order_submitted` twice within 300 ms; two rows arrive with the same `eventId` but different receive timestamps.

   **Hint:** upsert on `eventId` at ingest.

   </details>

2. **Re-run after failure** — If the pipeline dies during load with partial data inserted, what happens when you re-run it? How do you guarantee the same outcome as a clean run?

   <details>
   <summary>See example and hint</summary>

   The 02:00 run loaded 847 of 1,412 rows into `reporting.daily_outbound_metrics` and failed on a Supabase timeout.

   **Hint:** upsert by daily partition key.

   </details>

3. **Late events** — How do you recompute a published daily KPI when a delayed event arrives, without inflating metrics or losing audit trail?

   <details>
   <summary>See example and hint</summary>

   At 23:50 a `checkout_validation_failed` is stored with a noon `timestamp`; that day's aggregate is already on the dashboard.

   **Hint:** recompute window; log invalidating run.

   </details>

#### Observability

4. **Silence vs. true absence** — How do you tell zero activity from failed capture or a pipeline that never ran? What minimum signals would you record?

   <details>
   <summary>See example and hint</summary>

   Between 14:00 and 15:00 there are no `login_failed` or `order_submitted` events, but the warehouse kept operating normally.

   **Hint:** heartbeat plus silence alert.

   </details>

5. **Collection traceability** — What traces reconstruct the path event → dashboard and detect gaps, bursts, or interval drift?

   <details>
   <summary>See example and hint</summary>

   A KPI spikes at 09:00 and flatlines at 09:15 — real demand or a batch that processed two windows at once?

   **Hint:** correlate `requestId` and `run_id`.

   </details>

6. **Growth vs. data loss** — If event volume swings day to day, how do you know the app is growing vs. losing or duplicating measurements?

   <details>
   <summary>See example and hint</summary>

   Mondays: 12,000 events; Sundays: 800 — operator shifts or intermittent `POST /telemetry` failures?

   **Hint:** compare events to active sessions.

   </details>

#### Recoverability

7. **Database outage** — Where do you resume if the connection drops mid-pipeline? What checkpoint do you persist?

   <details>
   <summary>See example and hint</summary>

   Pandas finished grouping by `product_id`, but Supabase dropped on `INSERT` into the reporting table.

   **Hint:** phase checkpoint in `pipeline_runs`.

   </details>

8. **Frontend buffer** — Does buffering offline events in the browser make sense? What risks does it introduce, and which layer should own them?

   <details>
   <summary>See example and hint</summary>

   An operator loses WiFi for 20 minutes; the browser stores 45 events in `localStorage` and sends them in one batch on reconnect.

   **Hint:** client buffer; server-side dedup.

   </details>

9. **Transmission retry** — How do you design retries on `POST /telemetry` without breaking idempotency? What server response means "already stored" vs. "retry"?

   <details>
   <summary>See example and hint</summary>

   The client gets a timeout, retries, but the server already persisted the event on the slow first request.

   **Hint:** `Idempotency-Key`; return 200 if exists.

   </details>

#### Cross-cutting

10. **Concurrent runs** — What do you observe, how do you avoid load race conditions, and how do you recover when cron and a manual trigger from `services/` overlap?

    <details>
    <summary>See example and hint</summary>

    The scheduled flow starts at 02:00; at 02:05 someone clicks "Run pipeline now" in the operations backoffice.

    **Hint:** window lock; unique `run_id`.

    </details>

---

## 🌱 How to Start

1. Run `git pull` on your monorepo fork to make sure you have the latest state.
2. Explore the [`data/`](https://github.com/4GeeksAcademy/ai-engineering-company-project-monorepo/tree/main/data) folder in the monorepo — it contains the subfolders `raw/`, `process/`, `pipelines/`, and `eval/` that you will use throughout this module. Orchestration code will live in `data/pipelines/`; reusable transformation scripts in `data/process/`; HTTP endpoints that query or trigger the pipeline will live in `services/` and import from `data/pipelines/` — not the other way around.
3. Create the file `data/pipelines/PIPELINE_DESIGN.md` — that is where your design document goes.
4. Review the telemetry events, KPIs, and domain entities already in your monorepo to identify what data your pipeline must process.

> **Note on tooling:** Today you are introduced to **Prefect** as an orchestration framework — flows, tasks, states, and configuration blocks. Your design document should reflect how you would organize your pipeline using these concepts, even though the code implementation comes over the next days.

---

## 💻 What You Need to Do

### Phase 1 — Current state analysis

- [ ] Document in a "Current State" section the data you already have: which telemetry events you have captured, where they are stored, and which reports you already generate with Pandas.
- [ ] Identify the limitations of your current implementation: what happens if the script fails mid-run? Can you tell whether data has already been processed?

### Phase 2 — Pipeline design

- [ ] Define the **purpose** of the pipeline in a single concrete sentence: what problem it solves and what value it delivers to your company.
- [ ] Specify the **extraction format**: where data comes from (table, endpoint, file), in what format it arrives, and how often it is updated.
- [ ] Design the **data flow** with a text or Mermaid diagram showing at least three clearly separated stages: extraction, transformation, and load.
- [ ] Describe how you would handle a source that **updates existing records** rather than always inserting new ones — explain the concrete strategy to avoid duplicates in your specific case.

### Phase 3 — Resilience and idempotency

- [ ] Define your **idempotency strategy**: if the pipeline fails during the load phase and is re-run, explain exactly how you guarantee that already-loaded data is neither corrupted nor duplicated.
- [ ] Design your **execution log**: specify the minimum fields you would record in every run (start time, end time, records processed, status, errors) and explain why each field is necessary to audit the pipeline in production.

### Phase 4 — Mapping to Prefect

- [ ] Map your design to Prefect concepts: identify which parts would be **flows**, which would be **tasks**, and which **states** (Running, Completed, Failed) are relevant for your pipeline.
- [ ] Indicate which configuration or credentials you would manage as **Prefect blocks** (for example, the connection to Supabase).

### Phase 5 — Application integration (design only)

- [ ] Sketch which **endpoints in `services/`** the operations team will use to query the last run's status/metadata and to trigger a manual flow run.
- [ ] For each endpoint, state which **function or flow in `data/pipelines/`** it will call — no ETL logic belongs in `services/`.

⚠️ **IMPORTANT:** Field names, entity IDs, and domain-specific values in your design must match your company's domain vocabulary in the monorepo. A generic design that ignores your company's data model will not be accepted.

---

## ✅ What We Will Evaluate

- [ ] The file `data/pipelines/PIPELINE_DESIGN.md` exists in the monorepo and is written in readable Markdown.
- [ ] The pipeline purpose is defined in a single concrete sentence that mentions the company's business, not only the technology.
- [ ] The data flow diagram shows at least three distinct stages (extraction, transformation, load) with the real entity or table names from the company.
- [ ] The strategy for handling updates to existing records is documented with a concrete mechanism (e.g., upsert by primary key, last-modified timestamp, control table).
- [ ] The idempotency strategy is explicit: it describes what happens on the second run after a load-phase failure, not just what would be desirable.
- [ ] The execution log specifies at least five fields with the field name, data type, and justification for why that field is necessary for auditing.
- [ ] The Prefect mapping identifies at least two flows and three tasks with concrete names aligned with the pipeline stages.
- [ ] The design documents at least two planned `services/` endpoints (status query and manual trigger) and names the `data/pipelines/` functions each will import.
- [ ] The design is consistent with the telemetry events and KPIs already captured in your monorepo.

---

## 📦 How to Submit

1. Make sure `data/pipelines/PIPELINE_DESIGN.md` is committed to your monorepo fork.
2. Commit with the message: `feat: add pipeline design document`.
3. Push your changes to your GitHub repository and share the URL with your tech lead.

---

This and many other projects are built by students as part of the [Coding Bootcamps](https://4geeksacademy.com/) at 4Geeks Academy. By [@marcogonzalo](https://github.com/marcogonzalo) and [other contributors](https://github.com/4GeeksAcademy/ai-engineering-company-project-monorepo/graphs/contributors). Find out more about [Full-Stack Software Developer](https://4geeksacademy.com/en/career-programs/full-stack), [Data Science & Machine Learning](https://4geeksacademy.com/en/career-programs/data-science-ml), [Cybersecurity](https://4geeksacademy.com/en/career-programs/cybersecurity) and [AI Engineering](https://4geeksacademy.com/en/career-programs/ai-engineering).
