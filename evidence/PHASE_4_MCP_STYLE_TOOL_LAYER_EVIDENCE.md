# Phase 4 Evidence - MCP-Style Tool Layer

## Phase Name

Phase 4 - MCP-Style Tool Layer

## Status

Complete

## Purpose

Phase 4 created a local MCP-style tool server for the Enterprise Agentic Workflow Consulting Lab.

The purpose of this phase was to expose approved enterprise tools through structured contracts so future agents can discover and request tools without directly accessing enterprise systems.

This phase supports the Senior Consultant - Agent Developer role by demonstrating how agentic workflows can use controlled tool contracts, metadata, schema validation, risk tiering, policy flags, approval requirements, trace IDs, and evidence-ready responses.

## Why This Phase Matters

Without a tool layer, agents can become uncontrolled integrations.

With an MCP-style tool layer:

```text
Agent does not directly touch enterprise systems.
Agent asks for an approved tool.
Tool schema validates the request.
Policy can inspect the action.
Evidence records what happened.
Phase 4 Design Principle
The model may request a tool.
The platform authorizes and executes the tool.

This principle is central to safe enterprise agentic AI design.

Built Components
Service
services/mcp-server/app/main.py
Tool Registry
services/mcp-server/registry/tools.json
Mock Data
services/mcp-server/data/customer-records.json
services/mcp-server/data/tickets.json
Tests
services/mcp-server/tests/test_mcp_server.py
Requirements
services/mcp-server/requirements.txt
Lab Notes
labs/phase-04-mcp-tool-layer/README.md
API Endpoints
GET /health

Purpose:

Validate that the MCP-style tool server is running and can load the tool registry.

Example response includes:

service
status
tool_count
timestamp
GET /tools

Purpose:

List approved tools and their metadata.

GET /tools/{tool_name}

Purpose:

Describe a specific tool contract.

POST /tools/{tool_name}/invoke

Purpose:

Invoke an approved tool through a structured contract.

The MCP-style server currently provides:

Tool discovery
Tool metadata
Input schema validation
Risk tier metadata
Policy check metadata
Approval requirement metadata
Tool execution simulation
Trace ID support
Evidence creation flag
Initial Tools
Tool	Purpose	Risk Tier	Policy Check	Approval
search_internal_docs	Search approved internal documents	low	false	false
query_policy	Query policy guidance for an action	medium	true	false
read_customer_record	Read synthetic customer record	high	true	true
create_ticket	Create synthetic support/compliance ticket	medium	true	false
Example Tool Registry Entry
{
  "tool_name": "read_customer_record",
  "description": "Reads a mock customer record when policy and authorization allow access.",
  "risk_tier": "high",
  "requires_policy_check": true,
  "requires_approval": true,
  "input_schema": {
    "customer_id": "string",
    "purpose": "string"
  }
}
Example Tool Invocation
{
  "user_id": "ola.consultant",
  "role": "security_architect",
  "trace_id": "trace-test-002",
  "arguments": {
    "customer_id": "cust-001",
    "purpose": "support investigation"
  }
}
Example Response Shape
{
  "invocation_id": "invoke-generated-id",
  "trace_id": "trace-test-002",
  "tool_name": "read_customer_record",
  "user_id": "ola.consultant",
  "risk_tier": "high",
  "requires_policy_check": true,
  "requires_approval": true,
  "policy_status": "approval_required",
  "execution_status": "completed",
  "result": {
    "found": true,
    "customer_id": "cust-001",
    "purpose": "support investigation",
    "record": {
      "customer_id": "cust-001",
      "name": "Mock Customer One",
      "classification": "confidential",
      "region": "us",
      "status": "active",
      "notes": "Synthetic customer record for lab use only."
    },
    "warning": "This is synthetic lab data. Real customer data access would require policy approval."
  },
  "evidence_created": true,
  "timestamp": "generated-timestamp"
}
Validation Result

The MCP-style tool layer passed local tests.

7 passed in 0.47s
Test Coverage

The current test suite validates:

Health check endpoint returns healthy status
Tool registry exposes four approved tools
Individual tool metadata can be retrieved
query_policy tool can be invoked
read_customer_record tool can be invoked
create_ticket tool can be invoked
Missing required tool arguments return validation error
Enterprise Pattern Demonstrated

This phase demonstrates the following pattern:

Agent or Client
   |
   v
MCP-Style Tool Server
   |
   +--> Discover approved tools
   +--> Read tool metadata
   +--> Validate input schema
   +--> Identify risk tier
   +--> Identify policy and approval requirements
   +--> Execute controlled tool simulation
   +--> Return evidence-ready response
What This Phase Does Not Do Yet

This phase does not yet include:

Full MCP protocol implementation
Live LLM tool calling
Real enterprise application integration
Real OPA/Rego policy enforcement
Real authentication
Real authorization
Real customer data access
Real ticketing system integration
Persistent evidence store
OpenTelemetry export

These are intentionally deferred to later phases.

JD Alignment

This phase maps to the job description areas below:

JD Area	Phase 4 Alignment
MCP Interoperability	Builds an MCP-style tool server pattern
Tool Use	Exposes approved tools through structured contracts
Agentic Workflows	Prepares agent runtime to call tools safely
API & Contracts	Uses FastAPI, JSON contracts, and schema validation
Governance	Adds policy and approval metadata to each tool
Responsible AI	Adds evidence flag, risk tier, and tool warnings
Enterprise AI Gateway	Supports gateway-to-tool interoperability
Local Execution Gateway	Demonstrates local controlled tool execution
Observability	Uses trace IDs and invocation IDs
Interview Explanation

The MCP-style tool layer gives enterprise agents a controlled way to discover and request tools. I built it because agents should not directly touch enterprise systems. The tool server exposes metadata, validates required arguments, labels risk tier, identifies policy and approval requirements, supports trace correlation, and returns evidence-ready responses. This makes tool use governable instead of uncontrolled integration.

Phase 4 Closure Statement

Phase 4 is complete.

The lab now has a working MCP-style tool layer with tests passing. The next phase should introduce a policy engine so tool requests can be evaluated through deterministic governance decisions before execution.
