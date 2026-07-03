# Phase 7 - Persistent Evidence Store

## Purpose

This phase creates a local persistent evidence store for the Enterprise Agentic Workflow Consulting Lab.

The evidence store turns workflow evidence from temporary API response flags into durable audit artifacts.

## Why This Matters

Before Phase 7:

```text
Evidence exists only in the response.

After Phase 7:

Every workflow run can write a persistent evidence record.

This is a major enterprise-readiness step because governed AI systems need auditable records that can be reviewed, replayed, investigated, and used for compliance reporting.

What This Phase Builds

This phase builds a local FastAPI evidence service with:

GET /health
POST /evidence/records
GET /evidence/records
GET /evidence/records/{record_id}
GET /evidence/workflows/{workflow_id}
Evidence Record Fields

Each evidence record captures:

record_id
workflow_id
trace_id
user_id
request
final_decision
final_status
grounded_context_found
source_count
policy_id
tool_name
tool_invoked
workflow stages
metadata
created_at
Why This Is Important for Enterprise Agentic AI

Enterprise agentic workflows require evidence because the organization must be able to answer:

Who made the request?
What did the agent retrieve?
What policy was evaluated?
What decision was returned?
Was a tool invoked?
Why was execution allowed or blocked?
What trace links the workflow together?
What record can be reviewed later?
Current Storage Approach

This phase uses a local JSON file:

services/evidence-store/data/evidence-records.json

This is intentional for local-first learning and testability.

In a production design, this could map to:

PostgreSQL
DynamoDB
Azure Cosmos DB
Google Firestore
OpenSearch
SIEM archive
Compliance evidence lake
What This Phase Does Not Build Yet

This phase does not yet include:

Automatic orchestrator-to-evidence-store integration
Database-backed persistence
Evidence signing
Tamper-evident hashing
OpenTelemetry trace export
SIEM forwarding
Approval workflow records
Compliance dashboard

Those will be added or mapped in later phases.

Interview Explanation

The persistent evidence store turns agent workflow decisions into durable audit artifacts. Instead of only returning an evidence flag in the response, each workflow can produce a record with workflow ID, trace ID, user, request, final decision, policy ID, source count, tool invocation status, stage details, and timestamp. This supports auditability, incident review, compliance reporting, and enterprise governance.
