# Phase 5 - Local Policy Engine

## Purpose

This phase creates a local deterministic policy engine for the Enterprise Agentic Workflow Consulting Lab.

The policy engine evaluates whether agent actions, tool requests, and data access patterns should be allowed, denied, redacted, or routed for approval.

## Why This Matters

Before Phase 5, the lab could label risk and metadata.

With Phase 5, the lab can make deterministic governance decisions.

This is the shift from:

```text
This tool is risky.

to:

This action is denied.
This action requires approval.
This response must be redacted.
This action is allowed.
Policy Decisions

The policy engine returns one of four decisions:

ALLOW
DENY
REDACT
APPROVAL_REQUIRED
What This Phase Builds

This phase builds a local FastAPI service with:

GET /health
POST /policy/evaluate
Policy Inputs

The policy engine evaluates:

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
Policy Rules

Initial rules include:

Deny prompt injection attempts
Deny region mismatch
Deny restricted data without approval
Redact when PII is detected
Require approval for high-risk tools
Require approval for confidential data
Allow low-risk approved workflows
What This Phase Does Not Build Yet

This phase does not yet include:

Full OPA runtime
Rego policy files
External policy bundle loading
Real identity provider integration
Real data classification service
Real approval workflow
Gateway-to-policy service integration
MCP-to-policy enforcement integration

Those will be added or mapped in later phases.

Design Principle
The LLM can suggest an action.
The policy engine decides whether the platform can execute it.
Interview Explanation

The policy engine is the deterministic governance layer for agentic AI workflows. I built it because LLMs should not be trusted to make access control decisions. The policy engine evaluates user context, action, data classification, region, risk tier, approval status, PII, and prompt-injection indicators. It returns a clear decision: allow, deny, redact, or approval required. This gives the platform an auditable control point before tools or data are accessed.
