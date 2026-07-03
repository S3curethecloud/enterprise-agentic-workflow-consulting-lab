# Phase 16 - Orchestrator Approval Integration

## Purpose

This phase integrates the agent orchestrator with the human approval workflow service.

The orchestrator now automatically creates approval records when a workflow requires human review or approval.

## Why This Matters

Before Phase 16:

```text
Human review existed as a separate approval service.

After Phase 16:

Review-required agent workflows automatically create auditable approval records.

This closes the loop between Responsible AI review, policy approval, workflow execution, and evidence.

New Orchestrator Response Fields

The orchestrator response now includes:

approval_required
approval_id
approval_status
approval_reason
approval_service_status
approval_record_created
Approval Creation Conditions

The orchestrator creates an approval record when:

Responsible AI returns REVIEW_REQUIRED
Responsible AI returns BLOCK
Policy returns APPROVAL_REQUIRED
Registry or governance denial requires review evidence
Updated Workflow
User Request
   |
   v
Agent Registry Enforcement
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
Responsible AI Evaluation
   |
   v
Human Approval Workflow if required
   |
   +--> Create approval record
   +--> Return approval_id
   +--> Persist approval metadata in evidence
   |
   v
MCP Tool Invocation only when policy and RAI pass
   |
   v
Evidence + Trace + Telemetry
Evidence Integration

The persisted workflow evidence metadata now includes:

approval_required
approval_id
approval_status
approval_reason
approval_service_status
approval_record_created
Approval Service Integration

The orchestrator writes approval records into:

services/approval-service/data/approvals.json

Each approval record includes:

approval_id
workflow_id
trace_id
agent_id
requested_by
approver
review_reason
rai_decision
policy_decision
risk_tier
data_classification
requested_action
requested_tool
approval_status
decision_reason
created_at
updated_at
decided_at
Enterprise Value

This lets the platform answer:

Which workflows required approval?
Why was approval required?
Which agent triggered the request?
What policy or RAI decision caused the approval?
Which approval ID tracks the review?
Was the approval request persisted as evidence?
What This Phase Does Not Do Yet

This phase does not yet include:

Resuming workflow after approval
Blocking until approval is decided
Notification routing
Email/Slack integration
Identity-backed approver validation
Approval evidence hash chaining
Approval dashboard

Those can be added or mapped in later phases.

Production Mapping
Local Lab Feature	Production Equivalent
approvals.json	Approval workflow DB
create_approval_record	Approval ticket/workflow creation
approval_id	Human review artifact ID
approval_status	Workflow approval state
approval_service_status	Approval service integration result
approval metadata in evidence	Audit-ready governance trace
Interview Explanation

Phase 16 integrates the orchestrator with the approval workflow so review-required agent actions automatically generate approval records, preserve approval IDs in evidence, and prevent execution until a human decision is recorded. This connects Responsible AI, policy governance, and human-in-the-loop approval into one auditable workflow.

Phase 16 Closure Statement

Phase 16 is complete when review-required workflows automatically create approval records, approval IDs are returned in the orchestrator response, approval metadata is persisted in evidence, and tests validate the integration.
