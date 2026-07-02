# Phase 2 Evidence - Local AI Gateway Skeleton

## Phase Name

Phase 2 - Local AI Gateway Skeleton

## Status

Complete

## Purpose

Phase 2 created the first working local service for the Enterprise Agentic Workflow Consulting Lab.

The purpose of this phase was to build a local AI Gateway skeleton that acts as the controlled entry point before an enterprise agent runtime, RAG service, MCP tool layer, policy engine, LLM provider, or evidence service is invoked.

This phase supports the Senior Consultant - Agent Developer role by demonstrating how enterprise agentic workflows should begin with a controlled gateway pattern rather than allowing users or applications to call models and tools directly.

## Why This Phase Matters

Enterprise AI agents should not operate as uncontrolled chatbot endpoints.

Before an agent retrieves data, calls a tool, invokes a model, or performs an action, the enterprise needs a control point that can evaluate:

- Who is making the request
- What role or department the user belongs to
- What the user is asking the agent to do
- Whether the request appears sensitive or risky
- Whether policy review is required
- Where the request should be routed
- What evidence should be created for audit and observability

The AI Gateway is that control point.

## Built Components

### Service

- services/ai-gateway/app/main.py

### Tests

- services/ai-gateway/tests/test_gateway.py

### Requirements

- services/ai-gateway/requirements.txt

### Lab Notes

- labs/phase-02-ai-gateway-skeleton/README.md

## API Endpoints

### GET /health

Purpose:

Validate that the AI Gateway service is running.

Example response includes:

- service
- status
- timestamp

### POST /gateway/request

Purpose:

Accept an enterprise agent request and return a structured gateway decision.

The gateway currently simulates:

- Request intake
- User context handling
- Prompt risk scoring
- Risk label assignment
- Routing decision
- Policy handoff flag
- Evidence creation flag
- Trace ID generation
- Request ID generation

## Example Request

```json
{
  "user_id": "ola.consultant",
  "role": "security_architect",
  "department": "ai_platform",
  "request": "Search the internal AI policy and create a ticket if this workflow is non-compliant.",
  "data_region": "us",
  "risk_tier": "medium"
}
Example Response
{
  "request_id": "req-generated-id",
  "trace_id": "trace-generated-id",
  "user_id": "ola.consultant",
  "role": "security_architect",
  "department": "ai_platform",
  "prompt_risk_score": 62,
  "risk_label": "medium",
  "routing_decision": "agent_runtime",
  "policy_handoff_required": true,
  "evidence_created": true,
  "timestamp": "generated-timestamp",
  "status": "accepted_for_agent_processing"
}
Validation Result

The AI Gateway skeleton passed local tests.

3 passed in 0.38s
Test Coverage

The current test suite validates:

Health check endpoint returns healthy status
Medium-risk enterprise request is accepted
Policy handoff is required for action-oriented requests
Evidence creation flag is set
Low-risk informational request is accepted
Enterprise Pattern Demonstrated

This phase demonstrates the following pattern:

User Request
   |
   v
AI Gateway
   |
   +--> Generate request_id
   +--> Generate trace_id
   +--> Score prompt risk
   +--> Assign risk label
   +--> Choose routing path
   +--> Determine policy handoff requirement
   +--> Create evidence stub
   |
   v
Accepted for future agent processing
What This Phase Does Not Do Yet

This phase does not yet include:

Real LLM calls
Amazon Bedrock integration
OpenAI integration
Azure OpenAI / Foundry integration
RAG retrieval
MCP tool execution
OPA/Rego policy evaluation
OpenTelemetry export
Persistent evidence storage

These are intentionally deferred to later phases.

JD Alignment

This phase maps to the job description areas below:

JD Area	Phase 2 Alignment
Enterprise AI Gateway	Creates the first local gateway skeleton
Local Execution Gateways	Demonstrates local-first request control
Agentic Workflows	Prepares the controlled entry point for agent execution
Governance	Adds policy handoff decisioning
Responsible AI	Adds risk scoring and evidence creation placeholders
Observability	Adds request_id and trace_id for correlation
API & Contracts	Uses FastAPI and structured Pydantic models
Cloud & DevOps	Establishes testable service structure
Interview Explanation

The AI Gateway is the front door for enterprise agentic workflows. I built it first because enterprise agents should not call models, tools, or data sources directly without a control layer. The gateway gives the platform a consistent place to apply user context, risk scoring, routing, policy handoff, trace correlation, and evidence creation before the request reaches the agent runtime.

Phase 2 Closure Statement

Phase 2 is complete.

The lab now has a working local AI Gateway skeleton with tests passing. The next phase should add a local RAG service so the agent workflow can retrieve trusted enterprise knowledge before generating an answer or calling a tool.
