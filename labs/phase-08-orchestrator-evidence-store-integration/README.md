# Phase 8 - Orchestrator Evidence Store Integration

## Purpose

This phase integrates the local agent workflow orchestrator with the persistent evidence store.

The orchestrator now writes a durable evidence record every time a workflow runs.

## Why This Matters

Before Phase 8:

```text
Phase 6 returned an evidence summary.
Phase 7 stored evidence records.

After Phase 8:

Every orchestrator workflow run automatically writes a persistent evidence record.

This connects the end-to-end agent workflow with durable auditability.

New Workflow Behavior

The orchestrator response now includes:

evidence_record_id
evidence_persisted

The response also includes these values inside the evidence_summary object.

Updated Architecture Flow
User Request
   |
   v
AI Gateway Decision
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
Persistent Evidence Record
   |
   v
Evidence-ready workflow response
Durable Evidence File

The orchestrator writes records to:

services/evidence-store/data/evidence-records.json
Evidence Record Includes

Each workflow evidence record includes:

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
Why This Is Enterprise-Grade

This phase turns the workflow into an auditable system.

The enterprise can now answer:

What request came in?
What sources were used?
What policy decision was made?
Was a tool invoked?
Was execution blocked, redacted, or routed for approval?
What trace ID connects the stages?
What evidence record proves the workflow outcome?
What This Phase Does Not Build Yet

This phase does not yet include:

Live HTTP call from orchestrator to evidence-store API
Database-backed persistence
Tamper-evident evidence signing
Hash chaining
SIEM forwarding
OpenTelemetry export
Approval workflow lifecycle records

Those will be added or mapped in later phases.

Interview Explanation

Phase 8 connects the agent workflow to durable audit evidence. Each orchestrator run now automatically writes an evidence record containing the workflow ID, trace ID, user request, final decision, status, policy ID, source count, tool invocation status, stage details, metadata, and timestamp. This proves the workflow is not only governed at runtime but also auditable after execution.
