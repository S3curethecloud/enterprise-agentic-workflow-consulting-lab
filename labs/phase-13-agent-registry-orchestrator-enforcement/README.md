# Phase 13 - Agent Registry + Orchestrator Enforcement

## Purpose

This phase integrates the persistent agent registry with the local agent workflow orchestrator.

The orchestrator now checks agent identity, lifecycle status, allowed tools, data access scope, and risk tier before allowing a workflow to proceed.

## Why This Matters

Before Phase 13:

```text
Agents could be registered.
Workflows could be executed.

After Phase 13:

Only approved, active, correctly scoped agents can execute governed workflows.

This turns the registry from a metadata store into an enforcement control.

Enforcement Rules

The orchestrator now enforces:

agent exists
agent status is active
requested tool is in allowed_tools
requested data classification is in data_access_scope
workflow risk is compatible with agent risk_tier
New Request Field

The orchestrator request now includes:

agent_id
New Response Fields

The orchestrator response now includes:

agent_id
agent_name
agent_version
agent_registry_status
agent_registry_decision
agent_registry_reason
Registry Enforcement Decisions

The registry stage can return:

ALLOW
DENY
Registry Enforcement Status Values

The registry stage can return:

agent_registry_allowed
agent_not_found
agent_not_active
tool_not_allowed
data_scope_not_allowed
risk_tier_exceeded
Updated Workflow
User Request
   |
   v
Agent Registry Enforcement
   |
   +--> Is the agent registered?
   +--> Is the agent active?
   +--> Is the tool allowed?
   +--> Is the data scope allowed?
   +--> Is the risk tier allowed?
   |
   v
AI Gateway
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
Evidence + Trace + Telemetry
Why This Is Enterprise-Grade

This lets the platform answer:

Which agent executed the workflow?
Was the agent active?
Was the tool allowed for that agent?
Was the data scope allowed?
Was the risk tier compatible?
Which registry decision allowed or blocked the workflow?
Was the registry decision persisted in evidence?
Evidence Integration

The persisted evidence metadata now includes:

agent_id
agent_name
agent_version
agent_registry_status
agent_registry_decision
agent_registry_reason
What This Phase Does Not Build Yet

This phase does not yet include:

Live service-to-service call to the agent registry API
Agent approval workflow
Agent version promotion workflow
Owner attestation
Registry UI
Fine-grained RBAC
Real identity provider integration

Those will be added or mapped in later phases.

Interview Explanation

Phase 13 integrates the agent registry with the orchestrator so execution is gated by agent identity, lifecycle status, allowed tools, data access scope, and risk tier before the workflow proceeds. This means only approved, active, correctly scoped agents can execute governed workflows. Registry decisions are included in the workflow response, trace timeline, and persisted evidence metadata.

Phase 13 Closure Statement

Phase 13 is complete when the orchestrator denies unregistered, disabled, over-scoped, or risk-incompatible agents and tests validate registry-based enforcement.
