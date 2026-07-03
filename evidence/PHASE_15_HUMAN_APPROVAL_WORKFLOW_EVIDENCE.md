# Phase 15 Evidence - Human Approval Workflow

## Phase Name

Phase 15 - Human Approval Workflow

## Status

Complete

## Purpose

Phase 15 added a local human approval workflow service to the Enterprise Agentic Workflow Consulting Lab.

The purpose of this phase was to make review-required workflows actionable by creating a dedicated approval service that can create, track, approve, reject, and preserve human review decisions.

## Why This Phase Matters

Before Phase 15:

```text
The workflow could identify that human review was required.

After Phase 15:

The platform can create, track, approve, reject, and evidence human review decisions.

This supports human-in-the-loop governance for sensitive data access, high-risk workflows, policy approval paths, and Responsible AI review paths.

Built Components
Approval Service
services/approval-service/app/main.py
Persistent Approval Store
services/approval-service/data/approvals.json
Tests
services/approval-service/tests/test_approval_service.py
Requirements
services/approval-service/requirements.txt
Lab Notes
labs/phase-15-human-approval-workflow/README.md
API Endpoints
GET /health

Purpose:

Validate that the approval service is running and can read the approval store.

POST /approvals

Purpose:

Create a human approval request for a review-required workflow.

GET /approvals

Purpose:

List approval requests. Supports filtering by approval status.

GET /approvals/{approval_id}

Purpose:

Retrieve one approval request by ID.

PATCH /approvals/{approval_id}/approve

Purpose:

Approve a pending approval request.

PATCH /approvals/{approval_id}/reject

Purpose:

Reject a pending approval request.

Approval Record Fields

Each approval record includes:

Field	Purpose
approval_id	Unique approval request identifier
workflow_id	Workflow requiring review
trace_id	Trace associated with the workflow
agent_id	Agent that requested or triggered the workflow
requested_by	User who initiated the workflow
approver	Assigned or acting reviewer
review_reason	Reason human review is required
rai_decision	Responsible AI decision
policy_decision	Policy engine decision
risk_tier	Workflow risk tier
data_classification	Data sensitivity level
requested_action	Requested workflow action
requested_tool	Requested tool
approval_status	pending, approved, or rejected
decision_reason	Human reviewer explanation
created_at	Approval request creation timestamp
updated_at	Last update timestamp
decided_at	Approval or rejection timestamp
Approval Status Values

The approval service supports:

pending
approved
rejected
Validation Result

The approval service tests passed.

10 passed in 0.51s
Test Coverage

The Phase 15 test coverage validates:

Health check returns healthy approval service status
Approval requests can be created
Approval requests persist to local JSON storage
Approval requests can be listed
Pending approvals can be filtered
Approval request can be retrieved by ID
Missing approval returns 404
Pending request can be approved
Pending request can be rejected
Already decided request cannot be approved again
Already decided request cannot be rejected again
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
Enterprise Pattern Demonstrated

This phase demonstrates the following enterprise human-in-the-loop pattern:

Responsible AI or Policy Review Required
   |
   v
Approval Request
   |
   +--> Pending
   +--> Approved
   +--> Rejected
   |
   v
Auditable Human Decision
What This Phase Does Not Do Yet

This phase does not yet include:

Orchestrator integration with the approval service
Approval-triggered workflow continuation
Notification routing
Email or Slack approval flow
Identity-provider-backed approver validation
Approval evidence hash chaining
Approval UI

These are intentionally deferred to the next integration phase or later deployment phases.

Production Mapping
Local Lab Feature	Production Equivalent
approvals.json	Approval database or workflow engine
POST /approvals	Human review ticket creation
approval_status	Workflow approval state
approver	Assigned governance reviewer
decision_reason	Audit justification
approve/reject endpoints	Human-in-the-loop control
decided_at	Approval decision timestamp
JD Alignment

This phase maps to the job description areas below:

JD Area	Phase 15 Alignment
Responsible AI	Provides human review workflow for RAI outcomes
Governance Standards	Adds auditable approval process
Enterprise Workflows	Supports review-required workflow handling
Agentic Workflows	Creates approval artifacts for agent actions
Risk Management	Tracks risk tier and data classification
Evidence	Preserves approval decision metadata
Consulting Delivery	Demonstrates human-in-the-loop governance design
Interview Explanation

Phase 15 adds a human approval workflow so review-required agent actions can be routed to an approver, approved or rejected, and preserved as evidence before execution proceeds. This is important because enterprise agentic AI systems need human-in-the-loop controls for sensitive data, high-risk decisions, and Responsible AI review paths.

Phase 15 Closure Statement

Phase 15 is complete.

The lab now has a standalone human approval workflow service with tested create, list, retrieve, approve, and reject paths. The next phase should integrate the orchestrator with the approval service so review-required workflows automatically create approval requests and preserve approval IDs in the workflow evidence.
