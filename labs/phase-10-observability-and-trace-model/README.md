# Phase 10 - Observability and Trace Model

## Purpose

This phase adds a local observability and trace model to the Enterprise Agentic Workflow Consulting Lab.

The orchestrator now returns a structured trace timeline for each governed agent workflow.

## Why This Matters

Before Phase 10:

```text
The workflow had IDs, evidence records, and hash integrity.

After Phase 10:

The workflow has a structured trace model that explains what happened at each stage.

This improves auditability, supportability, debugging, and production readiness.

New Observability Fields

The orchestrator response now includes:

trace_timeline
stage_event_count
total_latency_ms
Trace Event Fields

Each trace event includes:

event_id
trace_id
workflow_id
stage_name
event_type
status
latency_ms
timestamp
details
Trace Stages

The workflow emits trace events for:

ai_gateway
rag_retrieval
policy_evaluation
mcp_tool_invocation
Event Types

The workflow emits these event types:

request_risk_routing
source_grounding
governance_decision
controlled_tool_execution
Updated Workflow Story
User Request
   |
   v
AI Gateway
   |
   +--> trace event: request_risk_routing
   |
   v
RAG Retrieval
   |
   +--> trace event: source_grounding
   |
   v
Policy Evaluation
   |
   +--> trace event: governance_decision
   |
   v
MCP Tool Invocation
   |
   +--> trace event: controlled_tool_execution
   |
   v
Evidence Store
   |
   +--> stores trace summary in evidence metadata
Why This Is Enterprise-Grade

This lets the platform answer:

Which workflow ran?
Which trace links the workflow?
Which stages executed?
Which stage made the final decision?
Which policy was used?
Was a tool invoked or skipped?
What was the approximate stage latency?
Which evidence record proves the workflow?
What record hash verifies integrity?
Current Latency Model

This phase uses deterministic latency placeholders.

This is intentional because the lab is still local-first and deterministic.

In production, these placeholders can map to:

OpenTelemetry span duration
API gateway latency
model latency
RAG retrieval latency
policy evaluation latency
tool execution latency
evidence persistence latency
What This Phase Does Not Build Yet

This phase does not yet include:

Real OpenTelemetry SDK instrumentation
OTLP exporter
Jaeger
Grafana Tempo
Prometheus metrics
Grafana dashboard
Distributed service-to-service tracing
Cost telemetry
Token usage telemetry

Those will be added or mapped in later phases.

Production Mapping
Local Field	Production Equivalent
trace_id	OpenTelemetry trace ID
event_id	Span or event ID
workflow_id	Agent workflow run ID
stage_name	Span name
event_type	Span attribute or event name
latency_ms	Span duration
evidence_record_id	Audit artifact link
record_hash	Evidence integrity digest
Interview Explanation

Phase 10 adds trace-level observability to the governed agent workflow. Each workflow now returns a trace timeline across gateway, RAG, policy evaluation, and MCP tool invocation. The trace includes event IDs, trace ID, workflow ID, stage name, event type, status, latency placeholders, timestamps, and details. This makes the workflow easier to debug, audit, support, and map to OpenTelemetry in production.

Phase 10 Closure Statement

Phase 10 is complete when orchestrator tests pass, the workflow returns a structured trace timeline, and evidence records include trace metadata.
