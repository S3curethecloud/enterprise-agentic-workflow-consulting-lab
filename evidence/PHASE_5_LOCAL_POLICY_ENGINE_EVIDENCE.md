# Phase 5 Evidence - Local Policy Engine

## Phase Name

Phase 5 - Local Policy Engine

## Status

Complete

## Purpose

Phase 5 created a local deterministic policy engine for the Enterprise Agentic Workflow Consulting Lab.

The purpose of this phase was to move the lab from risk labeling into actual governance decisioning. The policy engine evaluates whether an agent action, tool request, or data access pattern should be allowed, denied, redacted, or routed for approval.

This phase supports the Senior Consultant - Agent Developer role by demonstrating how enterprise agentic workflows can enforce deterministic policy decisions before actions proceed.

## Why This Phase Matters

Before Phase 5, the lab could identify risk metadata.

With Phase 5, the lab can make deterministic governance decisions.

This is the shift from:

```text
This tool is risky.

to:

This action is allowed.
This action is denied.
This response must be redacted.
This action requires approval.
Core Design Principle
The LLM can suggest an action.
The policy engine decides whether the platform can execute it.

This is a foundational principle for trusted enterprise agentic AI.

Built Components
Service
services/policy-engine/app/main.py
Policy Rules
services/policy-engine/policies/policy_rules.json
Tests
services/policy-engine/tests/test_policy_engine.py
Requirements
services/policy-engine/requirements.txt
Lab Notes
labs/phase-05-local-policy-engine/README.md
API Endpoints
GET /health

Purpose:

Validate that the policy engine is running and can load policy rules.

Example response includes:

service
status
policy_version
rule_count
timestamp
POST /policy/evaluate

Purpose:

Evaluate user, action, tool, data, region, risk, approval, PII, and prompt context to return a deterministic policy decision.

The policy engine currently evaluates:

user_id
role
action
tool_name
data_classification
user_region
data_region
risk_tier
approval_present
pii_detected
prompt_text
business_justification
Policy Decisions

The policy engine returns one of four decisions:

Decision	Meaning
ALLOW	Action may proceed
DENY	Action is blocked
REDACT	Sensitive content must be redacted before response
APPROVAL_REQUIRED	Human or external approval is required before execution
Initial Policy Rules
Policy ID	Rule	Decision
POL-AI-001	Deny prompt injection attempts	DENY
POL-DATA-001	Approval required for confidential data	APPROVAL_REQUIRED
POL-DATA-002	Deny restricted data without explicit approval	DENY
POL-PII-001	Redact PII in model output or tool response	REDACT
POL-TOOL-001	Approval required for high-risk tools	APPROVAL_REQUIRED
POL-REGION-001	Deny region mismatch	DENY
POL-DEFAULT-ALLOW	Allow low-risk approved workflow	ALLOW
Example Request
{
  "user_id": "ola.consultant",
  "role": "security_architect",
  "action": "read_customer_record",
  "tool_name": "read_customer_record",
  "data_classification": "confidential",
  "user_region": "us",
  "data_region": "us",
  "risk_tier": "medium",
  "approval_present": false,
  "pii_detected": false,
  "prompt_text": "Read customer record for support investigation.",
  "business_justification": "Support investigation"
}
Example Response Shape
{
  "evaluation_id": "eval-generated-id",
  "trace_id": "trace-generated-id",
  "user_id": "ola.consultant",
  "action": "read_customer_record",
  "decision": "APPROVAL_REQUIRED",
  "policy_id": "POL-DATA-001",
  "reason": "Confidential data access requires approval before execution.",
  "requires_approval": true,
  "requires_redaction": false,
  "allowed_to_execute": false,
  "evidence_created": true,
  "timestamp": "generated-timestamp"
}
Validation Result

The local policy engine passed tests.

8 passed in 0.51s
Test Coverage

The current test suite validates:

Health check endpoint returns healthy status
Low-risk internal action returns ALLOW
Confidential data access returns APPROVAL_REQUIRED
Restricted data without approval returns DENY
PII detection returns REDACT
Prompt injection attempt returns DENY
Region mismatch returns DENY
High-risk tool without approval returns APPROVAL_REQUIRED
Enterprise Pattern Demonstrated

This phase demonstrates the following pattern:

Agent Action or Tool Request
   |
   v
Policy Engine
   |
   +--> Inspect prompt text
   +--> Inspect data classification
   +--> Inspect region compatibility
   +--> Inspect risk tier
   +--> Inspect approval status
   +--> Inspect PII flag
   |
   v
ALLOW / DENY / REDACT / APPROVAL_REQUIRED
What This Phase Does Not Do Yet

This phase does not yet include:

Full OPA runtime
Rego policy files
External policy bundle loading
Real identity provider integration
Real approval workflow
Gateway-to-policy service integration
MCP-to-policy enforcement integration
Persistent evidence store
OpenTelemetry export

These are intentionally deferred to later phases.

JD Alignment

This phase maps to the job description areas below:

JD Area	Phase 5 Alignment
Governance	Adds deterministic policy evaluation
OPA/Rego Familiarity	Models OPA-style policy decisions locally
Responsible AI	Adds PII redaction, prompt-injection blocking, approval requirements
Enterprise AI Gateway	Prepares policy handoff enforcement
MCP Tool Layer	Prepares tool execution policy enforcement
Security	Adds data classification, region, and risk-tier decisions
API & Contracts	Uses FastAPI and structured Pydantic models
Observability	Adds evaluation_id and trace_id
Interview Explanation

The policy engine is the deterministic governance layer for enterprise agentic AI. I built it because LLMs should not make access control decisions. The model may suggest an action, but the policy engine evaluates user context, action, data classification, region, risk tier, approval status, PII indicators, and prompt-injection patterns before execution. It returns a clear decision: allow, deny, redact, or approval required.

Phase 5 Closure Statement

Phase 5 is complete.

The lab now has a working local policy engine with tests passing. The next phase should integrate the gateway, RAG service, MCP-style tool server, and policy engine into a single local agent workflow simulation.
