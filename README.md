# Enterprise Agentic Workflow Consulting Lab

## Status

**Complete — 18-phase enterprise agentic AI workflow lab finalized.**

This repository demonstrates a complete enterprise-grade agentic AI workflow platform for consulting, architecture review, and interview preparation.

## Portfolio Summary

I built an enterprise-grade agentic AI workflow platform that demonstrates AI gateway routing, RAG grounding, MCP-style tool execution, policy governance, agent registry enforcement, Responsible AI evaluation, human approval, observability, cost telemetry, tamper-evident evidence, deployment readiness, and cloud platform mapping.

## Purpose

This lab was built to align with the **Senior Consultant - Agent Developer, LLM & Agentic Workflows** role.

The project demonstrates how to design, implement, govern, observe, and explain agentic AI workflows in an enterprise environment.

It covers:

- LLM agent workflow design
- Enterprise AI Gateway patterns
- Local Execution Gateway pattern
- MCP-style interoperability
- RAG and knowledge grounding
- Tool-use governance
- Policy enforcement
- Agent registry and lifecycle control
- Responsible AI evaluation
- Human-in-the-loop approval
- Evidence and auditability
- Observability and telemetry
- Cost and performance tracking
- Cloud deployment mapping

## Core Principle

```text
The LLM is not the control plane.

The platform is the control plane.

The model may request a tool or suggest an action, but the platform authorizes, governs, executes, observes, and records that action.

High-Level Architecture
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
Services
Service	Purpose
AI Gateway	Request intake, risk scoring, and routing
RAG Service	Grounded retrieval from trusted internal sources
MCP Server	MCP-style enterprise tool interface
Policy Engine	Governance decisions: ALLOW, DENY, REDACT, APPROVAL_REQUIRED
Evidence Store	Persistent evidence and tamper-evident hash chain
Agent Registry	Agent identity, lifecycle, tool scope, data scope, and risk tier
Approval Service	Human approval request creation, approval, and rejection
Agent Orchestrator	End-to-end workflow coordination
Completed 18 Phases
Phase	Status	Capability
1	Complete	Platform decision foundation
2	Complete	Local AI Gateway skeleton
3	Complete	Local RAG service
4	Complete	MCP-style tool layer
5	Complete	Local policy engine
6	Complete	Local agent workflow integration
7	Complete	Persistent evidence store
8	Complete	Orchestrator evidence store integration
9	Complete	Tamper-evident evidence hashing
10	Complete	Observability and trace model
11	Complete	Cost and performance telemetry model
12	Complete	Persistent agent registry
13	Complete	Agent registry and orchestrator enforcement
14	Complete	Responsible AI evaluation layer
15	Complete	Human approval workflow service
16	Complete	Orchestrator approval integration
17	Complete	Cloud platform mapping and deployment readiness
18	Complete	Final consulting demo package and interview story
What This Lab Demonstrates

This lab demonstrates how an enterprise agent workflow can:

Receive a request through an AI gateway.
Validate the requesting agent through an agent registry.
Retrieve grounded context through RAG.
Evaluate governance policy.
Run Responsible AI evaluation.
Create human approval records when required.
Invoke tools only when allowed.
Persist tamper-evident evidence.
Emit trace and telemetry metadata.
Map to AWS, Azure, OpenAI API, and local open-source platforms.
Demo Package

The final consulting demo package is available in:

demo/

It includes:

File	Purpose
EXECUTIVE_SUMMARY.md	Business and architecture summary
JD_ALIGNMENT_MATRIX.md	Role-to-lab alignment
ARCHITECTURE_WALKTHROUGH.md	Technical architecture explanation
FINAL_DEMO_GUIDE.md	Demo flow and presentation guide
INTERVIEW_STORY.md	Interview-ready project explanation
DEMO_SCRIPT.md	Spoken walkthrough script
Deployment Readiness

Deployment readiness artifacts are available in:

deployment/

They include:

File	Purpose
README.md	Deployment overview
SERVICE_CONTRACTS.md	Service responsibilities and boundaries
DEPLOYMENT_READINESS_CHECKLIST.md	Production readiness checklist
platform-mapping/aws-bedrock-mapping.md	AWS Bedrock mapping
platform-mapping/azure-openai-foundry-mapping.md	Azure OpenAI / Microsoft Foundry mapping
platform-mapping/openai-api-mapping.md	OpenAI API mapping
platform-mapping/local-open-source-mapping.md	Local open-source model mapping
Local Docker Deployment

Validate Compose configuration:

docker compose config

Build and run:

docker compose build
docker compose up

Service health checks:

curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health
curl http://localhost:8005/health
curl http://localhost:8006/health
curl http://localhost:8007/health
curl http://localhost:8008/health
Validation

Key validation performed across the lab:

AI Gateway tests passed
RAG service tests passed
MCP server tests passed
Policy engine tests passed
Evidence store tests passed
Agent orchestrator tests passed
Agent registry tests passed
Approval service tests passed
Docker Compose configuration validated

Recent validations:

Phase 14 orchestrator tests: 12 passed
Phase 15 approval service tests: 10 passed
Phase 16 orchestrator approval integration tests: 9 passed
Docker Compose config: succeeded
Cloud Platform Mapping

The architecture maps to:

Platform	Mapping
AWS Bedrock	Bedrock, Knowledge Bases, Lambda action groups, Step Functions, DynamoDB, S3
Azure OpenAI / Microsoft Foundry	Azure OpenAI, Azure AI Search, API Management, Container Apps, Logic Apps
OpenAI API	Enterprise AI Gateway, custom orchestrator, MCP tools, vector DB, policy service
Local Open-Source Models	vLLM, Ollama, TGI, llama.cpp, LangGraph, OPA, Qdrant, Grafana
Interview Explanation

I built a governed enterprise agentic workflow platform that demonstrates how agents can safely retrieve knowledge, evaluate policy, request tool execution, route sensitive actions to human approval, and preserve evidence. The key pattern is that the LLM does not directly control enterprise systems. The model can request an action, but the platform authorizes, executes, observes, and records that action.

Final Outcome

This 18-phase Enterprise Agentic Workflow Consulting Lab is complete.

It is ready to be used as a portfolio project, technical interview walkthrough, architecture discussion artifact, and consulting reference implementation.
