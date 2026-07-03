# Architecture Walkthrough

## High-Level Architecture

```text
User / Business Application
   |
   v
Enterprise AI Gateway
   |
   v
Agent Orchestrator
   |
   +--> Agent Registry
   +--> RAG Service
   +--> Policy Engine
   +--> Responsible AI Evaluation
   +--> Human Approval Workflow
   +--> MCP Tool Layer
   +--> Evidence Store
   +--> Trace and Telemetry
Key Design Principle

The LLM is not the control plane.

The platform is the control plane.

The model may suggest an action, but the platform decides whether that action is allowed, whether human approval is required, whether a tool can be invoked, and what evidence must be preserved.

Service Responsibilities
Service	Responsibility
AI Gateway	Intake, risk scoring, routing
RAG Service	Grounding and source retrieval
MCP Server	Approved tool interface
Policy Engine	Governance decisioning
Evidence Store	Persistent evidence and hash-chain integrity
Agent Registry	Agent identity, lifecycle, tool scope, data scope
Approval Service	Human review and approval decisions
Agent Orchestrator	Coordinates the full workflow
Workflow Stages
1. Agent registry enforcement
2. AI gateway intake
3. RAG retrieval
4. Policy evaluation
5. Responsible AI evaluation
6. Human approval workflow if required
7. MCP tool invocation if allowed
8. Evidence persistence
9. Trace and telemetry output
Registry Enforcement

The orchestrator checks whether the requesting agent is:

registered
active
approved for the requested tool
approved for the requested data classification
operating within its risk tier

If the agent fails these checks, the workflow is denied or routed to review evidence.

RAG Grounding

The RAG service retrieves trusted internal context from local policy and runbook documents.

This models enterprise grounding against internal knowledge bases, such as:

policy documents
data classification standards
incident response runbooks
internal AI usage policies
Policy Enforcement

The policy engine returns one of the following decisions:

ALLOW
DENY
REDACT
APPROVAL_REQUIRED

This models enterprise governance logic before tool execution.

Responsible AI Evaluation

The Responsible AI evaluator checks:

safety risk
bias risk
explainability score
source provenance
whether human review is required

It returns:

PASS
REVIEW_REQUIRED
BLOCK
Human Approval Workflow

When review is required, the orchestrator creates an approval record with:

approval_id
workflow_id
trace_id
agent_id
review reason
RAI decision
policy decision
approval status

This creates an auditable human-in-the-loop control.

Tool Invocation

Tools are invoked only when policy, registry, and Responsible AI controls allow the action.

The model does not directly execute tools. The platform executes approved tools.

Evidence and Integrity

Each workflow is persisted into the evidence store.

Evidence includes:

request metadata
policy decision
RAI decision
approval metadata
trace timeline
telemetry
tool invocation status
hash-chain integrity metadata
Observability

Each workflow includes trace events for major stages.

This helps answer:

Where did the workflow spend time?
Which stage made the decision?
Was approval required?
Was a tool invoked?
Was the evidence persisted?
Deployment Mapping

The same architecture can map to:

AWS Bedrock
Azure OpenAI / Microsoft Foundry
OpenAI API
local open-source models

The platform controls remain the same even when the model provider changes.
