# Phase 12 Evidence - Persistent Agent Registry

## Phase Name

Phase 12 - Persistent Agent Registry

## Status

Complete

## Purpose

Phase 12 created a local persistent agent registry for the Enterprise Agentic Workflow Consulting Lab.

The purpose of this phase was to store governed agent metadata so agents can be discovered, versioned, owned, reviewed, and mapped to approved tools and data access scopes.

## Why This Phase Matters

Before Phase 12:

```text
The lab could run governed workflows.

After Phase 12:

The lab can govern which agents exist, who owns them, what version is active, what tools they may use, and what data they can access.

This supports enterprise agent lifecycle governance.

Built Components
Service
services/agent-registry/app/main.py
Persistent Registry File
services/agent-registry/data/agents.json
Tests
services/agent-registry/tests/test_agent_registry.py
Requirements
services/agent-registry/requirements.txt
Lab Notes
labs/phase-12-persistent-agent-registry/README.md
API Endpoints
GET /health

Purpose:

Validate that the agent registry is running and can read the local registry file.

POST /agents

Purpose:

Create a governed agent record.

GET /agents

Purpose:

List registered agents. Supports filtering by status and risk tier.

GET /agents/{agent_id}

Purpose:

Retrieve one registered agent by ID.

PATCH /agents/{agent_id}/status

Purpose:

Update the lifecycle status of an agent.

Agent Registry Fields

Each registered agent includes:

Field	Purpose
agent_id	Unique agent identifier
agent_name	Human-readable agent name
version	Agent version
owner	Owning team or person
description	Agent purpose
capabilities	What the agent can do
allowed_tools	Tools the agent is permitted to request
risk_tier	low, medium, or high
data_access_scope	Data classifications the agent can access
status	draft, active, deprecated, or disabled
created_at	Agent creation timestamp
updated_at	Agent update timestamp
Agent Lifecycle Status

The registry supports:

draft
active
deprecated
disabled
Validation Result

The persistent agent registry passed tests.

10 passed in 0.47s
Test Coverage

The Phase 12 test coverage validates:

Health check returns healthy registry status
Agent records can be created
Agent records persist to local JSON storage
Duplicate agent name and version returns conflict
Agents can be listed
Agents can be filtered by status
Agents can be filtered by risk tier
Agent can be retrieved by ID
Missing agent returns 404
Agent lifecycle status can be updated
Missing agent status update returns 404
Enterprise Pattern Demonstrated

This phase demonstrates the following enterprise registry pattern:

Governed Agent Registry
   |
   +--> Register agent identity
   +--> Track owner
   +--> Track version
   +--> Track lifecycle status
   +--> Track capabilities
   +--> Track allowed tools
   +--> Track risk tier
   +--> Track data access scope
   |
   v
Agent discovery and governance source
What This Phase Does Not Do Yet

This phase does not yet include:

Orchestrator enforcement against the registry
Registry approval workflow
Version promotion workflow
Owner attestation
Automated risk review
Registry-to-policy integration
Registry-to-MCP tool validation
Registry UI

These are intentionally deferred to later phases.

Production Mapping
Local Lab Feature	Production Equivalent
agents.json	PostgreSQL, DynamoDB, Cosmos DB, Firestore, service catalog, or internal developer portal
agent_id	Agent identity
owner	Accountable business or technical owner
version	Release/version control
status	Lifecycle governance state
allowed_tools	Tool authorization scope
data_access_scope	Data classification boundary
risk_tier	Governance and approval tier
JD Alignment

This phase maps to the job description areas below:

JD Area	Phase 12 Alignment
Persistent Registry	Adds local persistent agent registry
Agent Discovery	Supports listing and retrieving agents
Versioning	Stores agent version metadata
Governance	Tracks owner, risk tier, lifecycle status, and data access scope
Tool Governance	Maps agents to allowed tools
Enterprise Operations	Supports lifecycle management
Consulting Delivery	Demonstrates agent platform governance design
Interview Explanation

Phase 12 adds a persistent agent registry so agents can be discovered, versioned, owned, governed, and mapped to approved tools and data access scopes before execution. This is important because enterprise AI platforms need to know which agents exist, who owns them, what they are allowed to do, what version is active, and whether the agent is draft, active, deprecated, or disabled.

Phase 12 Closure Statement

Phase 12 is complete.

The lab now has a persistent agent registry with tests passing. The next phase should integrate the registry with the orchestrator so workflow execution is allowed only when an agent is active and the requested tool is permitted for that agent.
