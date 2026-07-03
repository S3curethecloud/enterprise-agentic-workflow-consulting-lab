# Phase 6 Evidence - Local Agent Workflow Integration

## Phase Name

Phase 6 - Local Agent Workflow Integration

## Status

Complete

## Purpose

Phase 6 created a local agent workflow orchestrator for the Enterprise Agentic Workflow Consulting Lab.

The purpose of this phase was to connect the major enterprise agent control points into a single simulated workflow:

- AI Gateway
- RAG retrieval
- Policy evaluation
- MCP-style tool invocation
- Evidence summary

This phase proves that the lab can move beyond isolated services and demonstrate an end-to-end governed enterprise agentic workflow.

## Why This Phase Matters

Before Phase 6, each component worked independently:

```text
AI Gateway     = request control point
RAG Service    = trusted knowledge point
MCP Server     = controlled tool point
Policy Engine  = deterministic governance point

Phase 6 connects those concepts into one flow.

This is where the lab starts proving the full enterprise agentic AI story:

I can design and implement governed enterprise agentic workflows where request intake, source grounding, policy decisions, tool execution, and evidence are connected end-to-end.
Built Components
Service
services/agent-orchestrator/app/main.py
Tests
services/agent-orchestrator/tests/test_agent_orchestrator.py
Requirements
services/agent-orchestrator/requirements.txt
Lab Notes
labs/phase-06-local-agent-workflow-integration/README.md
API Endpoints
GET /health

Purpose:

Validate that the local agent workflow orchestrator is running.

Example response includes:

service
status
workflow
timestamp
POST /agent/workflow

Purpose:

Accept an enterprise user request and simulate the full governed agent workflow.

The orchestrator currently simulates:

Request intake
AI Gateway risk scoring
Gateway routing decision
RAG retrieval
Source grounding
Policy evaluation
MCP-style tool invocation if allowed
Final decision
Final workflow status
Evidence summary
Workflow Stages

The orchestrator returns four stages:

Stage	Purpose
ai_gateway	Scores request risk and determines routing
rag_retrieval	Retrieves grounded policy/runbook context
policy_evaluation	Returns deterministic governance decision
mcp_tool_invocation	Invokes or skips controlled tool execution
Workflow Decisions

The workflow can return:

Decision	Meaning
ALLOW	Workflow may execute the approved tool
DENY	Workflow is blocked
REDACT	Workflow requires redaction before response
APPROVAL_REQUIRED	Workflow must wait for approval
Workflow Status Values

The workflow can return:

Status	Meaning
workflow_completed	Policy allowed execution and tool ran
workflow_denied	Policy denied the workflow
workflow_requires_redaction	Sensitive content must be redacted
workflow_waiting_for_approval	Human or external approval is required
Example Request
{
  "user_id": "ola.consultant",
  "role": "security_architect",
  "department": "ai_platform",
  "request": "Create a ticket after policy review for customer support workflow.",
  "action": "create_ticket",
  "tool_name": "create_ticket",
  "data_classification": "confidential",
  "user_region": "us",
  "data_region": "us",
  "risk_tier": "high",
  "approval_present": true,
  "pii_detected": false,
  "business_justification": "Approved policy review"
}
Example Response Shape
{
  "workflow_id": "workflow-generated-id",
  "trace_id": "trace-generated-id",
  "user_id": "ola.consultant",
  "final_decision": "ALLOW",
  "final_status": "workflow_completed",
  "grounded_context_found": true,
  "tool_invoked": true,
  "tool_name": "create_ticket",
  "stages": [
    {
      "stage_name": "ai_gateway",
      "status": "completed",
      "details": {
        "prompt_risk_score": 100,
        "risk_label": "high",
        "policy_handoff_required": true,
        "routing_decision": "agent_runtime_with_policy_review",
        "evidence_created": true
      }
    },
    {
      "stage_name": "rag_retrieval",
      "status": "completed",
      "details": {
        "grounded_context_found": true,
        "confidence": 0.85,
        "source_count": 2,
        "evidence_created": true
      }
    },
    {
      "stage_name": "policy_evaluation",
      "status": "completed",
      "details": {
        "decision": "ALLOW",
        "policy_id": "POL-DEFAULT-ALLOW",
        "allowed_to_execute": true,
        "evidence_created": true
      }
    },
    {
      "stage_name": "mcp_tool_invocation",
      "status": "completed",
      "details": {
        "tool_name": "create_ticket",
        "tool_invoked": true,
        "evidence_created": true
      }
    }
  ],
  "evidence_summary": {
    "gateway_evidence": true,
    "rag_evidence": true,
    "policy_evidence": true,
    "tool_evidence": true,
    "final_decision": "ALLOW"
  }
}
Validation Result

The local agent workflow orchestrator passed tests.

6 passed in 0.47s
Test Coverage

The current test suite validates:

Health check endpoint returns healthy status
Internal document search workflow returns ALLOW
Allowed workflow invokes the tool
Confidential customer data without approval returns APPROVAL_REQUIRED
Prompt injection attempt returns DENY
Approved high-risk ticket creation returns ALLOW and invokes create_ticket
PII detection returns REDACT and skips tool execution
Evidence summary is returned across gateway, RAG, policy, and tool stages
Enterprise Pattern Demonstrated

This phase demonstrates the following end-to-end pattern:

Enterprise User Request
   |
   v
AI Gateway
   |
   +--> Risk scoring
   +--> Routing decision
   +--> Policy handoff signal
   |
   v
RAG Retrieval
   |
   +--> Source grounding
   +--> Confidence scoring
   +--> Context retrieval
   |
   v
Policy Engine
   |
   +--> ALLOW
   +--> DENY
   +--> REDACT
   +--> APPROVAL_REQUIRED
   |
   v
MCP-Style Tool Layer
   |
   +--> Invoke approved tool only when policy allows
   +--> Skip tool when policy denies, requires redaction, or requires approval
   |
   v
Evidence-Ready Workflow Response
What This Phase Does Not Do Yet

This phase does not yet include:

Live service-to-service HTTP calls
Real LLM reasoning
Real LangChain, AutoGen, CrewAI, or LlamaIndex orchestration
Real MCP protocol implementation
Real OPA/Rego runtime enforcement
Real OpenTelemetry collector
Persistent evidence database
Human approval queue
Cloud deployment

These are intentionally deferred to later phases.

JD Alignment

This phase maps to the job description areas below:

JD Area	Phase 6 Alignment
Agentic Workflows	Connects gateway, RAG, policy, and tools end-to-end
Enterprise AI Gateway	Simulates gateway-controlled intake and routing
RAG	Adds grounded context before action
MCP Interoperability	Uses MCP-style tool invocation stage
Governance	Applies deterministic policy before execution
Responsible AI	Supports deny, redact, approval-required, and evidence outputs
Observability	Uses workflow_id, trace_id, stage details, and evidence summary
Consulting Delivery	Demonstrates an enterprise-ready workflow explanation
Interview Explanation

Phase 6 proves the end-to-end enterprise agentic workflow. A user request enters through a gateway, receives a risk and routing decision, retrieves grounded context through RAG, gets evaluated by a policy engine, and only invokes an MCP-style tool if policy allows execution. The final response includes a trace ID, final decision, workflow status, stage details, source grounding, and evidence summary. This demonstrates how agentic AI can be made governable, auditable, and enterprise-ready.

Phase 6 Closure Statement

Phase 6 is complete.

The lab now has a local end-to-end agent workflow orchestrator with tests passing. The next phase should add persistent evidence records so every workflow run can produce durable audit artifacts instead of only returning evidence flags in the API response.
