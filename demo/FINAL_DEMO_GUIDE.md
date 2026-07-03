# Final Demo Guide

## Purpose

This guide explains how to demonstrate the Enterprise Agentic Workflow Consulting Lab.

The demo should show that the platform can govern agent workflows end-to-end across registry enforcement, RAG grounding, policy evaluation, Responsible AI, approval routing, tool execution, evidence, trace, and telemetry.

## Demo Story

An enterprise wants to allow AI agents to help with internal policy and support workflows.

The risk is that agents may access sensitive data, invoke tools, or make decisions without proper governance.

This platform solves that by placing enterprise controls around the agent.

## Demo Flow

### 1. Start with the architecture

Explain:

```text
This is not just an LLM app. This is a governed agentic workflow platform.

Show the service boundaries:

AI Gateway
RAG Service
MCP Tool Layer
Policy Engine
Evidence Store
Agent Registry
Approval Service
Agent Orchestrator
2. Explain the key control principle

Say:

The model may request a tool. The platform authorizes and executes the tool.

Then explain that registry, policy, Responsible AI, and approval controls sit before tool execution.

3. Show a successful workflow

Use a low-risk request where:

agent is active
tool is allowed
data scope is allowed
policy allows the action
Responsible AI passes
no approval is required
tool invocation succeeds
evidence is stored

Expected story:

This workflow completed because all governance controls passed.
4. Show a review-required workflow

Use a bias-sensitive or confidential-data request where:

Responsible AI returns REVIEW_REQUIRED
human_review_required is true
approval record is created
approval_id is returned
tool is not invoked
evidence stores approval metadata

Expected story:

This workflow did not proceed silently. The platform created an approval record and preserved that approval ID in evidence.
5. Show a blocked workflow

Use an unsafe request where:

Responsible AI returns BLOCK
final status is blocked
tool is not invoked
approval/audit record is created
evidence is preserved

Expected story:

The workflow was blocked before tool execution because Responsible AI controls detected unsafe intent.
6. Show deployment readiness

Show:

Dockerfiles
docker-compose.yml
service contracts
deployment checklist
platform mappings

Expected story:

The same local architecture can map to AWS Bedrock, Azure OpenAI, OpenAI API, or self-hosted open-source models.
Demo Commands
Check repository files
find services -maxdepth 2 -type f | sort
find deployment -type f | sort
find demo -type f | sort
Run orchestrator tests
cd services/agent-orchestrator
source .venv/bin/activate
PYTHONPATH=. pytest -q
Run approval service tests
cd services/approval-service
source .venv/bin/activate
PYTHONPATH=. pytest -q
Validate Docker Compose
docker compose config
What to Emphasize

Emphasize that this lab demonstrates:

agent development
agentic workflow design
enterprise gateway thinking
MCP-style tool interoperability
RAG grounding
policy enforcement
Responsible AI
human approval
evidence
telemetry
deployment mapping
Best Closing Line

This lab shows that I understand agentic AI beyond prompts. I can design the enterprise control plane around agents so workflows are governed, observable, auditable, and ready for cloud deployment.
