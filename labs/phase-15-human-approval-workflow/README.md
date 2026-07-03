# Phase 15 - Human Approval Workflow

## Purpose

This phase adds a local human approval workflow service to the Enterprise Agentic Workflow Consulting Lab.

Phase 14 introduced Responsible AI review outcomes such as REVIEW_REQUIRED and BLOCK. Phase 15 creates a dedicated approval service so review-required workflows can be routed, approved, rejected, tracked, and preserved as evidence.

## Why This Matters

Before Phase 15:

```text
The workflow could identify that human review was required.

After Phase 15:

The platform can create, track, approve, reject, and evidence human review decisions.

This supports human-in-the-loop governance for enterprise agentic AI workflows.

What This Phase Builds

This phase builds a local FastAPI approval service with:

GET /health
POST /approvals
GET /approvals
GET /approvals/{approval_id}
PATCH /approvals/{approval_id}/approve
PATCH /approvals/{approval_id}/reject
Approval Record Fields

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
Approval Status Values

Approval records can have the following states:

pending
approved
rejected
Enterprise Workflow
Review-Required Agent Workflow
   |
   v
Create Approval Request
   |
   +--> workflow_id
   +--> trace_id
   +--> agent_id
   +--> policy decision
   +--> RAI decision
   +--> risk tier
   +--> data classification
   |
   v
Human Reviewer
   |
   +--> approve
   +--> reject
   |
   v
Approval Evidence Record
Why This Is Enterprise-Grade

This lets the platform answer:

Which workflow required review?
Which agent requested the action?
Why was approval required?
Who reviewed the request?
Was it approved or rejected?
What was the decision reason?
When was the decision made?
Can the decision be audited later?
What This Phase Does Not Build Yet

This phase does not yet include:

Orchestrator integration with approval service
Approval-triggered workflow continuation
Notification routing
Email or Slack approval flow
Identity-provider-backed approver validation
Approval evidence hash chaining
Approval UI

Those can be added or mapped in later phases.

Production Mapping
Local Lab Feature	Production Equivalent
approvals.json	Approval database or workflow engine
POST /approvals	Human review ticket creation
approval_status	Workflow approval state
approver	Assigned governance reviewer
decision_reason	Audit justification
approved/rejected endpoint	Human-in-the-loop control
decided_at	Approval decision timestamp
Interview Explanation

Phase 15 adds a human approval workflow so review-required agent actions can be routed to an approver, approved or rejected, and preserved as evidence before execution proceeds. This is important because enterprise agentic AI systems need human-in-the-loop controls for sensitive data, high-risk decisions, and Responsible AI review paths.

Phase 15 Closure Statement

Phase 15 is complete when the approval service can create, list, retrieve, approve, and reject human review requests with tests passing.
