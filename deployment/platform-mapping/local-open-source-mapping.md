# Local Open-Source Model Platform Mapping

## Purpose

This document maps the local lab architecture to an enterprise self-hosted or open-source model deployment pattern.

## Local-to-Open-Source Mapping

| Local Component | Open-Source Mapping |
|---|---|
| AI Gateway | Kong, Envoy, NGINX, custom gateway |
| Agent Orchestrator | LangGraph, CrewAI, AutoGen, custom Python runtime |
| Model Runtime | vLLM, Ollama, TGI, llama.cpp, Ray Serve |
| RAG Service | OpenSearch, Qdrant, Weaviate, Milvus, pgvector |
| MCP Server | MCP server, FastAPI tool layer |
| Policy Engine | OPA/Rego, Cedar, custom policy API |
| Evidence Store | PostgreSQL, MinIO, immutable object storage |
| Agent Registry | PostgreSQL, Backstage, internal service catalog |
| Approval Service | Temporal, Camunda, Jira, ServiceNow |
| Observability | Prometheus, Grafana, Jaeger, OpenTelemetry |

## Production Architecture

```text
Enterprise App
   |
   v
Self-Hosted AI Gateway
   |
   v
Agent Runtime on Kubernetes
   |
   +--> Self-hosted LLM endpoint
   +--> Vector Database
   +--> MCP Tool Services
   +--> OPA Policy Engine
   +--> Agent Registry
   +--> Approval Workflow
   +--> Evidence Store
   |
   v
Prometheus / Grafana / Jaeger / SIEM
Interview Explanation

For regulated environments or strong data residency requirements, I would map the platform to a self-hosted open-source model architecture. The model can run behind an internal endpoint using vLLM, TGI, Ollama, or Ray Serve, while governance remains enforced through the gateway, registry, policy engine, Responsible AI evaluation, approval service, and evidence store.
