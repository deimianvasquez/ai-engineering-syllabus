# Skill-Type Examples (Reference)

Use these to tailor tone and focus; do not copy verbatim. Each example is **content-led** (theory topics named first) with the project as application — match that pattern, not project-only narratives. Each question models the **Question design rubric** (a trade-off, failure mode, evidence demand, or second-order effect) — match that reasoning depth, not surface recall.

### Web fundamentals (HTML, CSS, SEO, accessibility)

- **Student:** You will build a professional landing page with HTML and CSS, focusing on semantic structure, visual hierarchy, accessibility, and SEO. By the end, you should be able to review structure, contrast, and headings with clear criteria, and apply correct tags in your project. Before class, reflect: if you stripped every semantic tag but kept the same visuals, what exactly would a screen reader, a crawler, or an AI assistant lose — and how would you prove it?

- **Professor (mini kit):**
  - **Learn:** semantics + hierarchy. Question: when you replace `div` with semantic tags, what becomes possible for a screen reader or an assistant that wasn't before — and how would you prove the difference rather than assume it?
  - **Reflect:** speed vs semantic quality trade-off. Question: where exactly does "moving fast" turn into debt you'll pay later, and what signal would tell you you've crossed that line?
  - **Be aware of:** contrast/alt text/headings. Question: what minimum criteria define "accessible enough" for this stage, and what evidence (tool, audit, test) would prove a page meets it?
  - **Do:** review structure via DOM/inspection tools. Question: before asking AI to rewrite markup, what would you verify first so you can tell a real improvement from a confident-looking regression?
  - **Avoid:** anti-patterns like "layout without semantics." Question: if you let AI pick tags by intuition with no rules, what fails downstream — and who discovers it, and when?
  - **Facilitator probes (Reflect/Avoid):** "If they say 'it doesn't matter,' ask for the concrete user or SEO cost of the worst case"; "If they reduce SEO to keywords, ask what document structure communicates that keywords cannot."

### Tailwind and dashboards

- **Student:** You will design a Tailwind dashboard that organizes KPIs, drivers, and operational details so information becomes immediately clear. By the end, you should be able to justify your visual hierarchy and ensure responsive behavior in your project. Before class, reflect: if a user had only 5 seconds on your dashboard, which single layout decision determines whether they understand it — and how would you measure you got it right?

- **Professor (mini kit):**
  - **Learn:** information design (KPI/driver/operational layers). Question: if layout should follow the decisions users make, what would you have to remove from a screen that looks "complete" but doesn't support any decision?
  - **Reflect:** density vs readability trade-off. Question: when the dashboard breaks on mobile, what do you cut first — and what does that priority order reveal about who the dashboard is really for?
  - **Be aware of:** contrast, spacing, and scanability. Question: which measurable signal (time-to-understand, error rate, task completion) would you trust over your own taste to judge "is this clear"?
  - **Do:** repeatable component structure. Question: what rule would you write so AI can restyle without silently changing layout — and how would you catch it the day it ignores the rule?
  - **Avoid:** style copy/paste without intent. Question: how do you detect when AI has optimized for "looks good" at the cost of usability, before a real user does?
  - **Facilitator probes (Reflect/Avoid):** "If they only discuss colors, ask how fast a user can read the top KPI (e.g., within 5 seconds) and how they'd measure it."

### Programming / TypeScript (logic, algorithms)

- **Student:** In this session, you will practice logic and algorithmic thinking with TypeScript to solve problems clearly and predictably. By the end, you should be able to implement small functions, cover edge cases, and explain why your data flow is correct. Before class, reflect: which edge case makes your function return a wrong answer instead of crashing — and what test would catch it before a user does?

- **Professor (mini kit):**
  - **Learn:** control flow + types + data. Question: what minimum input/output contract makes this algorithm deterministic — and what would you have to assume about the data for it to hold?
  - **Reflect:** simplification vs edge-case coverage trade-off. Question: if AI suggests a shortcut that's faster but slightly less correct, how do you decide — and what would make that trade acceptable in one context but reckless in another?
  - **Be aware of:** edge cases and validation. Question: which business rule is hiding inside this edge case, and what happens to the user the day it goes unhandled?
  - **Do:** testable, readable implementation. Question: before accepting a PR, what one test would convince you the logic is correct — and what would convince you it isn't?
  - **Avoid:** imperative coding without plan / ambiguous logic. Question: when code "works" but isn't maintainable, who pays for that later and how would you spot it in review today?
  - **Facilitator probes (Reflect/Avoid):** "If they say 'it works,' ask for the smallest test that would make it fail"; "If they justify by intuition, ask which invariant must always hold."

### Working with coding agents (context, rules, memory bank)

- **Student:** You will prepare a project so a coding agent can work with real context: review the repo, create `.agents/rules`, and maintain a useful memory-bank so AI does not improvise blindly. By the end, you should be able to convert good and bad code patterns into clear working rules. Before class, reflect: which undocumented pattern in your repo would an agent copy and scale into a bigger problem — and how would you notice before it spreads?

- **Professor (mini kit):**
  - **Learn:** context engineering, rules (user vs project, globs, alwaysApply), and memory-bank. Question: when do several small, scoped contexts beat one large context — and how would you measure the effect on cost, latency, and answer quality rather than guess?
  - **Reflect:** implementation plan vs imperative prompt-by-prompt commands. Question: at what point does "moving fast with AI" quietly break the plan, and what evidence in the repo (diffs, commits, drift) would let you catch it early?
  - **Be aware of:** file references, project structure, and business context (not only technical context). Question: what is the minimum that must live in `memory-bank` so a fresh agent doesn't hallucinate the product — and what's the cost of putting too much there?
  - **Do:** fork project, commit by meaningful step, write `.agents/rules`, maintain `memory-bank`. Question: before trusting an agent's summary, how would you verify it against the actual code instead of taking its word?
  - **Avoid:** planless imperative development, "Global Dictator" rule overrides, ambiguous rules, blind trust in proactivity, dumping huge chat logs. Question: when your rules are vague or grant too much autonomy, what's the first thing that goes wrong — and how would you notice before it ships?
  - **Facilitator probes (Reflect/Avoid):** "If they say 'AI already knows,' ask which file proves it"; "If they want to override team rules, ask who pays that cost in production."

### OpenClaw modules (personal assistants, integrations, security)

- **Student:** You will configure your first OpenClaw assistant on a VPS, set up `openclaw.json`, and connect it to Telegram to operate it safely. By the end, you should be able to assign concrete tasks without exposing secrets or giving full system access. Before class, reflect: if one credential leaked from your assistant, what is the blast radius — and which default-deny permission would have contained it?

- **Professor (mini kit):**
  - **Learn:** OpenClaw as an assistant that "knows nothing until taught"; model selection by task; API → skills/workflows. Question: if installing OpenClaw isn't enough to get a useful agent, what architectural decisions actually create the value — and which would you make first?
  - **Reflect:** automation speed vs attack surface (MCP/integrations). Question: which integration earns being connected first, which should wait for stronger policy — and what would change your ranking?
  - **Be aware of:** security risks, secrets handling, minimum permissions, and installation discipline. Question: which data must never enter the agent's workspace/context, and what's the blast radius if it does?
  - **Do:** configure Telegram/MCP with bounded scope; transform an API into a reproducible skill. Question: how would you prove an execution actually succeeded without "trusting the chat transcript"?
  - **Avoid:** exposed keys, sensitive data access, full access permissions, assuming Zapier-MCP is the only path. Question: if the agent gained write access to a system it shouldn't touch, what's the worst realistic outcome — and what control would have prevented it?
  - **Facilitator probes (Reflect/Avoid):** "If they say 'connect everything,' ask for a tool allowlist and who approves additions"; "If they downplay security, ask for the worst-case impact of one leaked key."

### Agent loop (Python, LLM + tools, observe-decide-act)

- **Student:** You will build a basic Python agent loop where the LLM decides, code executes, and tools act inside a controlled cycle. By the end, you should define objective, stop condition, and conversation logging (for example, CSV) to verify the agent actually solved the task. Before class, reflect: reading only your log, how would you tell a loop that genuinely succeeded from one that merely gave up — and what signal makes that unambiguous?

- **Professor (mini kit):**
  - **Learn:** observe → decide → act → observe cycle; LLM/code/tool/loop roles. Question: which part of the flow must live in code rather than the prompt — and what fails if you push that responsibility onto the model?
  - **Reflect:** tool count vs agent clarity trade-off. Question: how many tools is too many for this loop, and what observable symptom (wrong tool calls, loops, cost) would tell you you've crossed the line?
  - **Be aware of:** explicit objective, observable state, and finish condition. Question: what objective signal would you stop the loop on, so termination depends on evidence instead of "looks done"?
  - **Do:** build `.py` calling API via tools; persist CSV log (`actor`, `message`, `tool_call`, `timestamp`). Question: reading only the CSV log, what pattern would warn you of an infinite loop or a poorly defined tool before you watch it run?
  - **Avoid:** heavy logic inside tools, ambiguous tools, monolithic prompt, no stop condition. Question: when one tool does everything and the LLM only "approves," what breaks first — and why is it hard to debug?
  - **Facilitator probes (Reflect/Avoid):** "If the prompt is 3 pages long, ask what concretely should move into code"; "If there's no stop condition, ask for the test that proves the loop terminates."

