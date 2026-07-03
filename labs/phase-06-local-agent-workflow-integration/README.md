# Phase 6 - Local Agent Workflow Integration

## Purpose

This phase creates a local agent workflow orchestrator for the Enterprise Agentic Workflow Consulting Lab.

The orchestrator connects the major enterprise agent control points into one end-to-end simulated workflow.

## Why This Matters

Before Phase 6, each service worked independently:

```text
AI Gateway = request control point
RAG Service = trusted knowledge point
MCP Server = controlled tool point
Policy Engine = deterministic governance point

Phase 6 connects those concepts into one workflow.

Phase 6 Goal

Build a local agent workflow orchestrator that simulates the full enterprise flow:

1. Receive an enterprise user request
2. Send request through AI Gateway logic
3. Retrieve grounded context from RAG
4. Evaluate action through Policy Engine
5. Invoke approved MCP-style tool if allowed
6. Return final workflow decision and evidence summary
Architecture Flow
User Request
   |
   v
AI Gateway Decision
   |
   v
RAG Retrieval
   |
   v
Policy Evaluation
   |
   v
MCP Tool Invocation if allowed
   |
   v
Evidence-ready workflow response
What This Phase Builds

This phase builds a local FastAPI service with:

GET /health
POST /agent/workflow
Workflow Stages

The orchestrator returns four workflow stages:

ai_gateway
rag_retrieval
policy_evaluation
mcp_tool_invocation

Each stage includes status, decision details, and evidence indicators.

Final Workflow Decisions

The workflow can return:

ALLOW
DENY
REDACT
APPROVAL_REQUIRED
Final Workflow Status Values

The workflow can return:

workflow_completed
workflow_denied
workflow_requires_redaction
workflow_waiting_for_approval
What This Phase Does Not Build Yet

This phase does not yet include:

Live service-to-service HTTP calls
Real LLM reasoning
Real LangChain, AutoGen, CrewAI, or LlamaIndex runtime
Real MCP protocol implementation
Real OPA/Rego enforcement
Real OpenTelemetry collector
Persistent evidence store
Human approval queue

Those will be added or mapped in later phases.

Why This Uses Local Logic First

The orchestrator intentionally uses local deterministic logic first.

This makes the enterprise flow easy to test, inspect, and explain before introducing distributed service calls, external providers, or orchestration frameworks.

Interview Explanation

This phase proves the full enterprise agentic workflow pattern. A user request enters through a gateway, retrieves grounded context through RAG, gets evaluated by the policy engine, and only invokes a tool if policy allows execution. The response includes the final decision, workflow status, stage details, trace ID, and evidence summary. This shows how agentic AI can be made governable, auditable, and enterprise-ready.
