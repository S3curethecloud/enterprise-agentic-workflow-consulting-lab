# Phase 4 - MCP-Style Tool Layer

## Purpose

This phase creates a local MCP-style tool layer for the Enterprise Agentic Workflow Consulting Lab.

The tool layer exposes approved tools through structured contracts so future agents can discover and request tools without directly accessing enterprise systems.

## Why This Matters

Without a tool layer, agents can become uncontrolled integrations.

With an MCP-style layer:

```text
Agent does not directly touch enterprise systems.
Agent asks for an approved tool.
Tool schema validates the request.
Policy can inspect the action.
Evidence records what happened.
Phase 4 Design Principle
The model may request a tool.
The platform authorizes and executes the tool.
What This Phase Builds

This phase builds a local FastAPI service with:

GET /health
GET /tools
GET /tools/{tool_name}
POST /tools/{tool_name}/invoke
Initial Tools
search_internal_docs
query_policy
read_customer_record
create_ticket
Tool Metadata

Each tool includes:

tool_name
description
risk_tier
requires_policy_check
requires_approval
input_schema
What This Phase Does Not Build Yet

This phase does not yet include:

Full MCP protocol implementation
Real enterprise system integration
Real OPA/Rego policy enforcement
Real authentication
Real authorization
Real persistent ticketing system
Real customer data access
Live LLM tool calling

Those will be added or mapped in later phases.

Interview Explanation

The MCP-style tool layer gives agents a controlled way to discover and request tools. I built it because enterprise agents should not directly touch enterprise systems. The tool server provides metadata, schema validation, policy flags, approval requirements, execution responses, trace IDs, and evidence flags. This creates an interoperability layer that can later be connected to a real MCP implementation or enterprise AI gateway.
