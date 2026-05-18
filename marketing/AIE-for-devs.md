# AI Engineering for devs — Program modules

_Este contenido también está disponible en [espanol](./AIE-from-devs.es.md)._

## AI Engineering Course Introduction

This program is designed for **software engineers who are ready to make the leap into AI Engineering** — professionals who already know how to build and ship software, and now want to apply that foundation to the systems shaping the next decade of the industry.

The curriculum assumes you bring working knowledge of **frontend development** (React, Next.js, JavaScript / TypeScript) and **backend development** (FastAPI or Flask). You will not spend time on the basics of web development or API design — instead, you will move directly into the AI-specific layer: agents, LLMs, retrieval systems, multi-agent orchestration, agentic infrastructure, and the security practices that production AI applications demand.

If you have been building software professionally and want to reposition yourself at the frontier of the discipline — this is the program for you.

---

## Core AI and Agents

### Personal Assistants with OpenClaw

`OpenClaw` `Setup` `Deploy`

You will learn to deploy and configure an open-source, self-hosted AI assistant — yours, under your control, without relying on external vendors. The practical foundation for the program's more advanced agent modules.

**Skills developed:**

- Configure an open-source AI agent as a personal assistant
- Assign tasks and integrate external applications with the agent

---

### Advanced Personal Assistants with OpenClaw

`Agent Skills` `Memory` `Tool Calling` `Advanced configuration`

You will take your basic assistant agent to a productive tool. You will learn to teach it new skills, choose the right memory type for each case, and configure it to operate with real autonomy in business contexts.

**Skills developed:**

- Identify scenarios where an agent solves real business problems
- Develop custom skills for OpenClaw
- Implement contextual memory (episodic, semantic, procedural)
- Advanced configuration and extension of the agent

---

### Working with AI Coding Agents

`Coding Agents` `Context Engineering` `Agent Rules` `Memory Banks` `Skills` `SDD`

The leap from "using AI" to "working professionally with AI." You will learn to build memory banks and context rules that turn a coding agent into a collaborator that understands your codebase. You will master writing specifications an agent can execute with precision.

**Skills developed:**

- Build memory banks and context rules from an existing codebase
- Write executable specifications for agents (agent specs)
- Synthesize reusable skills so agents act with precision

---

### LLMs, Training & RAG

`RAG` `Vector DBs` `Chunking` `Fine-tuning` `Embeddings` `Model Evaluation`

You will understand how the models that power agents work — and how to make them smarter for specific use cases. You will implement RAG so your agent answers with proprietary, up-to-date knowledge, and learn when and how to train or fine-tune a model.

**Skills developed:**

- Prepare data and select models for training
- Implement RAG techniques on proprietary knowledge bases
- Work with vector databases
- Evaluate, debug, and integrate models in production

---

### Agentic Engineering

`Tool Calling` `CLIs` `MCPs` `Guardrails` `Agent Memory`

The technical heart of the program. You will build agents that can call tools, access external systems via MCPs and CLIs, operate with persistent memory, and behave safely under guardrails. The knowledge that separates an AI engineer from someone who only uses chatbots.

**Skills developed:**

- Build agents with tool calling (real function calls)
- Implement guardrails as a security and control mechanism
- Provide tools to the agent via CLIs optimized for AI
- Extend agent capabilities with the Model Context Protocol (MCP)
- Give an agent persistent memory

---

### Agentic Workflows & Orchestration

`Multi-Agent Systems` `LangGraph` `State Graphs` `Routing` `Human-in-the-Loop` `Checkpointing`

When one agent is not enough. You will learn to design and orchestrate multi-agent systems with LangGraph, mastering the state graph model that makes complex agent collaboration possible. You will define state schemas, implement conditional routing and cycles with termination conditions, build human-in-the-loop checkpoints for approval and escalation, and compose modular subgraphs that can be reused across projects. You will also learn to trace, evaluate, and debug multi-agent flows — understanding which agent did what, why routing took a specific path, and what each decision cost.

**Skills developed:**

- Design multi-agent systems with LangGraph's state graph model
- Define state schemas and implement conditional edges and cycles
- Implement human-in-the-loop patterns (approval gates, review checkpoints, escalation routing)
- Use state persistence and checkpointing for long-running workflows
- Handle errors and recovery at individual nodes without crashing the graph
- Build modular subgraphs and compose them into larger systems
- Implement shared memory and context across agents
- Trace, evaluate, and observe multi-agent execution (routing decisions, token cost per path)

---

## Infrastructure for AI

### Container Applications with Docker

`Docker` `Containerization` `Deployment` `Reproducible Environments`

Packaging and deploying full applications with Docker for productive, reproducible environments. You will learn to containerize AI-powered applications and ensure they run consistently across development and production.

**Skills developed:**

- Package applications and their dependencies into containers
- Deploy containerized full-stack applications with Docker
- Configure reproducible environments for AI workloads

---

### Architecture Optimization

`Performance` `Caching` `Serialization` `Lazy Loading` `Scalability`

Performance strategies for frontend and backend systems that serve AI workloads. You will apply caching, serialization, lazy loading, and high-load practices to build systems that remain responsive under real usage.

**Skills developed:**

- Apply caching strategies to reduce latency in AI-integrated backends
- Optimize serialization and data transfer between services
- Implement lazy loading and other high-load performance patterns

---

### Data Pipelines

`Pandas` `ETL` `Data Pipelines` `Data optimization`

Data is the fuel of any AI solution. You will learn to build pipelines that take raw data from an application, transform it, and leave it ready to feed models, reports, or agents — the link that determines output quality.

**Skills developed:**

- Manipulate and prepare datasets with Python
- Build data pipelines from the application to analysis systems

---

### Telemetry

`Observability` `Reporting` `Data Collection` `Analysis`

You cannot improve what you do not measure. You will learn to instrument applications to collect behavioral data, build reports from that data, and make business decisions based on real evidence — not intuition.

**Skills developed:**

- Optimize storage for reporting and data integrity
- Identify data collection opportunities in real scenarios
- Collect telemetry and user context from the application
- Build reports from telemetry data

---

### Asynchronous Processing and Agentic Deployment

`Queues` `Background Jobs` `Workers` `RabbitMQ` `Serverless` `Durable Execution` `Cronjobs`

Tasks that must not block the user go to the queue — and agent workflows that must run reliably go here too. You will learn to implement background processing and queue systems that let agents and applications delegate heavy work without sacrificing response time. Then you will take it further: deploying agentic workflows into production with serverless functions, durable execution patterns, and cron-triggered pipelines. You will implement retry and resume from checkpoints, trigger LangGraph pipelines via webhooks, and build the infrastructure that keeps multi-agent systems running autonomously, continuously, and at scale.

**Skills developed:**

- Implement background processing for costly tasks
- Manage process queues with workers
- Use queues to delegate work between agents and services
- Deploy agentic workflows with serverless and durable functions
- Trigger agent pipelines via webhooks and cron jobs
- Implement retry and resume patterns from workflow checkpoints

---

### Cybersecurity in AI Applications

`OWASP` `AI Security` `LLM Auditing` `Guardrails`

AI introduces attack vectors traditional security does not cover. You will learn to identify the most critical vulnerabilities in AI applications, implement safe practices in model integration, and use LLMs themselves to audit a system.

**Skills developed:**

- Identify and fix OWASP Top 10 vulnerabilities in web applications
- Implement security practices specific to AI integrations
- Use LLMs as a cybersecurity auditing tool
