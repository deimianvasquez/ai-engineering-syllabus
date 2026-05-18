# AI Engineering for devs — Módulos del programa

_This content is also available in [English](./AIE-from-devs.md)._

## Introducción al curso de AI Engineering

Este programa está diseñado para **ingenieros de software que están listos para dar el salto a la Ingeniería de IA** — profesionales que ya saben construir y entregar software, y que ahora quieren aplicar esa base a los sistemas que están definiendo la próxima década de la industria.

El currículo asume que tienes conocimientos sólidos de **desarrollo frontend** (React, Next.js, JavaScript / TypeScript) y de **desarrollo backend** (FastAPI o Flask). No dedicarás tiempo a los fundamentos del desarrollo web ni al diseño de APIs — en cambio, entrarás directamente en la capa específica de IA: agentes, LLMs, sistemas de recuperación de información, orquestación multi-agente, infraestructura agéntica y las prácticas de seguridad que exigen las aplicaciones de IA en producción.

Si llevas años construyendo software de forma profesional y quieres reposicionarte en la frontera de la disciplina — este es tu programa.

---

## IA y Agentes

### Asistentes personales con OpenClaw

`OpenClaw` `Setup` `Deploy`

Aprenderás a desplegar y configurar un asistente de IA de código abierto y autoalojado — tuyo, bajo tu control, sin depender de proveedores externos. La base práctica sobre la que se construyen los módulos de agentes más avanzados del programa.

**Habilidades desarrolladas:**

- Configurar un agente de IA de código abierto como asistente personal
- Asignar tareas e integrar aplicaciones externas con el agente

---

### Asistentes personales avanzados con OpenClaw

`Habilidades de agente` `Memoria` `Tool Calling` `Configuración avanzada`

Convertirás tu agente asistente básico en una herramienta productiva. Aprenderás a enseñarle nuevas habilidades, elegir el tipo de memoria adecuado para cada caso y configurarlo para que opere con autonomía real en contextos de negocio.

**Habilidades desarrolladas:**

- Identificar escenarios donde un agente resuelve problemas reales de negocio
- Desarrollar habilidades personalizadas para OpenClaw
- Implementar memoria contextual (episódica, semántica, procedimental)
- Configuración y extensión avanzada del agente

---

### Trabajar con agentes de codificación IA

`Coding Agents` `Context Engineering` `Reglas de agente` `Memory Banks` `Habilidades` `SDD`

El salto de "usar IA" a "trabajar profesionalmente con IA." Aprenderás a construir memory banks y reglas de contexto que convierten a un agente de codificación en un colaborador que entiende tu base de código. Dominarás la escritura de especificaciones que un agente puede ejecutar con precisión.

**Habilidades desarrolladas:**

- Construir memory banks y reglas de contexto a partir de una base de código existente
- Escribir especificaciones ejecutables para agentes (agent specs)
- Sintetizar habilidades reutilizables para que los agentes actúen con precisión

---

### LLMs, entrenamiento y RAG

`RAG` `Bases de datos vectoriales` `Chunking` `Fine-tuning` `Embeddings` `Evaluación de modelos`

Entenderás cómo funcionan los modelos que alimentan a los agentes — y cómo hacerlos más inteligentes para casos de uso específicos. Implementarás RAG para que tu agente responda con conocimiento propio y actualizado, y aprenderás cuándo y cómo entrenar o hacer fine-tuning de un modelo.

**Habilidades desarrolladas:**

- Preparar datos y seleccionar modelos para entrenamiento
- Implementar técnicas RAG sobre bases de conocimiento propias
- Trabajar con bases de datos vectoriales
- Evaluar, depurar e integrar modelos en producción

---

### Ingeniería agéntica

`Tool Calling` `CLIs` `MCPs` `Guardrails` `Memoria de agente`

El núcleo técnico del programa. Construirás agentes capaces de llamar herramientas, acceder a sistemas externos vía MCPs y CLIs, operar con memoria persistente y comportarse de forma segura bajo guardrails. El conocimiento que separa a un ingeniero de IA de alguien que solo usa chatbots.

**Habilidades desarrolladas:**

- Construir agentes con tool calling (llamadas reales a funciones)
- Implementar guardrails como mecanismo de seguridad y control
- Proporcionar herramientas al agente mediante CLIs optimizadas para IA
- Extender las capacidades del agente con el Model Context Protocol (MCP)
- Dotar a un agente de memoria persistente

---

### Flujos de trabajo agénticos y orquestación

`Sistemas multi-agente` `LangGraph` `Grafos de estado` `Routing` `Human-in-the-Loop` `Checkpointing`

Cuando un solo agente no es suficiente. Aprenderás a diseñar y orquestar sistemas multi-agente con LangGraph, dominando el modelo de grafo de estado que hace posible la colaboración compleja entre agentes. Definirás esquemas de estado, implementarás enrutamiento condicional y ciclos con condiciones de terminación, construirás checkpoints human-in-the-loop para aprobación y escalado, y compondrás subgrafos modulares reutilizables entre proyectos. También aprenderás a trazar, evaluar y depurar flujos multi-agente: entendiendo qué agente hizo qué, por qué el enrutamiento tomó un camino concreto y cuánto costó cada decisión.

**Habilidades desarrolladas:**

- Diseñar sistemas multi-agente con el modelo de grafo de estado de LangGraph
- Definir esquemas de estado e implementar aristas condicionales y ciclos
- Implementar patrones human-in-the-loop (puertas de aprobación, checkpoints de revisión, enrutamiento de escalado)
- Usar persistencia de estado y checkpointing para flujos de larga duración
- Gestionar errores y recuperación en nodos individuales sin colapsar el grafo
- Construir subgrafos modulares y componerlos en sistemas más grandes
- Implementar memoria y contexto compartidos entre agentes
- Trazar, evaluar y observar la ejecución multi-agente (decisiones de enrutamiento, coste de tokens por ruta)

---

## Infraestructura para IA

### Aplicaciones en contenedores con Docker

`Docker` `Contenedores` `Despliegue` `Entornos reproducibles`

Empaquetado y despliegue de aplicaciones completas con Docker para entornos productivos y reproducibles. Aprenderás a contenerizar aplicaciones potenciadas por IA y a garantizar que funcionen de forma consistente entre desarrollo y producción.

**Habilidades desarrolladas:**

- Empaquetar aplicaciones y sus dependencias en contenedores
- Desplegar aplicaciones full-stack contenerizadas con Docker
- Configurar entornos reproducibles para cargas de trabajo de IA

---

### Optimización de arquitectura

`Rendimiento` `Caché` `Serialización` `Lazy Loading` `Escalabilidad`

Estrategias de rendimiento para sistemas frontend y backend que sirven cargas de trabajo de IA. Aplicarás caché, serialización, lazy loading y prácticas para alta carga para construir sistemas que se mantengan responsivos bajo uso real.

**Habilidades desarrolladas:**

- Aplicar estrategias de caché para reducir la latencia en backends integrados con IA
- Optimizar la serialización y la transferencia de datos entre servicios
- Implementar lazy loading y otros patrones de rendimiento para alta carga

---

### Pipelines de datos

`Pandas` `ETL` `Pipelines de datos` `Data optimization`

Los datos son el combustible de cualquier solución de IA. Aprenderás a construir pipelines que toman datos brutos de una aplicación, los transforman y los dejan listos para alimentar modelos, informes o agentes — el eslabón que determina la calidad del resultado.

**Habilidades desarrolladas:**

- Manipular y preparar conjuntos de datos con Python
- Construir pipelines de datos desde la aplicación hasta los sistemas de análisis

---

### Telemetría

`Observabilidad` `Reporting` `Recolección de datos` `Análisis`

No puedes mejorar lo que no mides. Aprenderás a instrumentar aplicaciones para recopilar datos de comportamiento, construir informes a partir de esos datos y tomar decisiones de negocio basadas en evidencia real — no en intuición.

**Habilidades desarrolladas:**

- Optimizar el almacenamiento para reporting e integridad de datos
- Identificar oportunidades de recolección de datos en escenarios reales
- Recopilar telemetría y contexto de usuario desde la aplicación
- Construir informes a partir de datos de telemetría

---

### Procesamiento asíncrono y despliegue agéntico

`Colas` `Jobs en background` `Workers` `RabbitMQ` `Serverless` `Ejecución durable` `Cronjobs`

Las tareas que no deben bloquear al usuario van a la cola — y los flujos de trabajo agénticos que deben ejecutarse de forma fiable también. Aprenderás a implementar procesamiento en background y sistemas de colas que permiten a agentes y aplicaciones delegar trabajo pesado sin sacrificar el tiempo de respuesta. Después irás más lejos: desplegando flujos agénticos en producción con funciones serverless, patrones de ejecución durable y pipelines disparados por cron. Implementarás patrones de reintento y reanudación desde checkpoints, dispararás pipelines de LangGraph mediante webhooks, y construirás la infraestructura que mantiene a los sistemas multi-agente funcionando de forma autónoma, continua y a escala.

**Habilidades desarrolladas:**

- Implementar procesamiento en background para tareas costosas
- Gestionar colas de procesos con workers
- Usar colas para delegar trabajo entre agentes y servicios
- Desplegar flujos agénticos con funciones serverless y durables
- Disparar pipelines de agentes mediante webhooks y cron jobs
- Implementar patrones de reintento y reanudación desde checkpoints de flujo

---

### Ciberseguridad en aplicaciones de IA

`OWASP` `Seguridad en IA` `Auditoría de LLMs` `Guardrails`

La IA introduce vectores de ataque que la seguridad tradicional no cubre. Aprenderás a identificar las vulnerabilidades más críticas en aplicaciones de IA, implementar prácticas seguras en la integración de modelos y usar los propios LLMs para auditar un sistema.

**Habilidades desarrolladas:**

- Identificar y corregir las vulnerabilidades OWASP Top 10 en aplicaciones web
- Implementar prácticas de seguridad específicas para integraciones de IA
- Usar LLMs como herramienta de auditoría de ciberseguridad
