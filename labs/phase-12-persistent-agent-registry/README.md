# Phase 12 - Persistent Agent Registry

## Purpose

This phase creates a local persistent agent registry for the Enterprise Agentic Workflow Consulting Lab.

The registry stores governed agent metadata so agents can be discovered, versioned, owned, reviewed, and mapped to approved tools and data access scopes.

## Why This Matters

Before Phase 12:

```text
The lab could run governed workflows.

After Phase 12:

The lab can govern which agents exist, who owns them, what version is active, what tools they may use, and what data they can access.

This supports enterprise agent lifecycle governance.

What This Phase Builds

This phase builds a local FastAPI service with:

GET /health
POST /agents
GET /agents
GET /agents/{agent_id}
PATCH /agents/{agent_id}/status
Agent Registry Fields

Each agent record includes:

agent_id
agent_name
version
owner
description
capabilities
allowed_tools
risk_tier
data_access_scope
status
created_at
updated_at
Agent Lifecycle Status

Agents can have the following statuses:

draft
active
deprecated
disabled
Why This Is Enterprise-Grade

This lets the platform answer:

Which agents exist?
Who owns each agent?
Which version is active?
What capabilities does the agent have?
Which tools is the agent allowed to use?
What data classification scope can the agent access?
What risk tier is assigned?
Is the agent draft, active, deprecated, or disabled?
Current Storage Approach

This phase uses a local JSON file:

services/agent-registry/data/agents.json

This is intentional for local-first learning and testability.

In production, this could map to:

PostgreSQL
DynamoDB
Azure Cosmos DB
Google Firestore
Service catalog
Internal developer portal
Agent governance registry
What This Phase Does Not Build Yet

This phase does not yet include:

Orchestrator enforcement against the registry
Registry approval workflow
Version promotion workflow
Owner attestation
Automated risk review
Registry-to-policy integration
Registry-to-MCP tool validation
Registry UI

Those will be added or mapped in later phases.

Interview Explanation

Phase 12 adds a persistent agent registry so agents can be discovered, versioned, owned, governed, and mapped to approved tools and data access scopes before execution. This is important because enterprise AI platforms need to know which agents exist, who owns them, what they are allowed to do, and whether they are active, deprecated, or disabled.

Phase 12 Closure Statement

Phase 12 is complete when the registry service can create, list, filter, retrieve, and update agent lifecycle status with tests passing.
