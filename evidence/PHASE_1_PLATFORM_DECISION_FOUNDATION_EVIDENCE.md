# Phase 1 Evidence - Platform Decision Foundation

## Phase Name

Phase 1 - Source of Truth, Architecture, RAG, and Platform Decision Foundation

## Status

Complete

## Purpose

Phase 1 established the foundation for the Enterprise Agentic Workflow Consulting Lab.

The purpose of this phase was to define the project source of truth, document the high-level enterprise agentic AI architecture, explain RAG design principles, and create platform decision guides across AWS, Azure, OpenAI, and local open-source model paths.

This phase does not require live cloud accounts or API credentials. It is intentionally cloud-neutral and local-first so the architecture, decision logic, and governance principles are understood before platform-specific live implementation.

## Completed Deliverables

### Core Project Files

- PROJECT_SOT.md
- README.md
- ROADMAP.md
- ARCHITECTURE.md
- DECISION_GUIDE.md

### Learning Notes

- docs/03-platform-decision-guide.md
- docs/09-rag-design-guide.md

### Platform Guides

- platform-guides/aws/01-aws-bedrock-path.md
- platform-guides/aws/02-aws-sagemaker-path.md
- platform-guides/azure/01-azure-openai-foundry-path.md
- platform-guides/openai/01-openai-api-path.md
- platform-guides/local-open-source/01-local-open-source-llama-path.md

### Visuals

- visuals/high-level-agentic-architecture.mmd
- visuals/rag-design-flow.mmd
- visuals/aws-bedrock-agent-flow.mmd
- visuals/aws-sagemaker-agent-flow.mmd
- visuals/azure-openai-foundry-agent-flow.mmd
- visuals/openai-agent-flow.mmd
- visuals/local-open-source-agent-flow.mmd

## Architecture Foundation Established

Phase 1 established the following enterprise agentic AI pattern:

```text
User / Business Application
   |
   v
Enterprise AI Gateway
   |
   v
Agent Runtime
   |---- RAG Service
   |---- MCP Tool Layer
   |---- Policy Engine
   |---- Evidence Service
   |---- Observability Layer
   |
   v
Approved Enterprise Tools and Data Sources
Platform Decision Coverage

Phase 1 defined when to use each platform:

Platform	Best Fit
AWS Bedrock	AWS-first managed GenAI applications, RAG, agents, guardrails
Amazon SageMaker	Custom model engineering, training, fine-tuning, MLOps
Azure OpenAI / Microsoft Foundry	Microsoft-first enterprise AI and agent development
OpenAI API	Fast direct LLM application development and tool calling
Local Open-Source Models	Self-hosting, control, isolation, customization, data residency
Key Consulting Principle

The platform should not be chosen by brand name.

The platform should be chosen based on:

Business workflow
Data sensitivity
Governance requirements
Cloud strategy
Latency targets
Cost envelope
Model capability
Operating maturity
Compliance approval
Long-term maintainability
RAG Foundation Established

Phase 1 documented RAG as the preferred starting point when the agent needs to answer from trusted enterprise knowledge.

RAG was positioned as useful for:

Policy Q&A
Compliance lookup
Runbook assistants
Internal documentation search
Support triage
Architecture knowledge assistants
Governance and evidence lookup

RAG was also bounded as not suitable for:

Replacing systems of record
High-risk decisions without validation
Sensitive retrieval without access control
Autonomous action without policy and approval
Using outdated or low-quality documents as trusted sources
Interview Value

Phase 1 supports the following interview message:

I do not start agentic AI design by picking a model or framework. I start with the workflow, data sensitivity, governance requirements, integration pattern, and operating model. From there, I choose the platform and architecture that best balances speed, control, security, observability, and long-term maintainability.
Why This Phase Matters

This phase proves the ability to reason like a senior consultant:

Explain why Bedrock differs from SageMaker
Explain when Azure Foundry is a better fit than Bedrock
Explain when OpenAI API is appropriate
Explain when local open-source models make sense
Explain why RAG should often come before fine-tuning
Explain why agents need gateways, policy checks, observability, and evidence
Phase 2 Recommendation

Phase 2 should begin the local implementation.

Recommended Phase 2:

Phase 2 - Local AI Gateway Skeleton

Phase 2 should build a local service that accepts an agent request and produces:

request_id
user context
prompt risk score
routing decision
policy handoff placeholder
evidence stub

No live cloud account is required for Phase 2.

Phase 1 Closure Statement

Phase 1 is complete.

The lab now has a clear source of truth, architecture baseline, RAG design guide, platform decision framework, platform-specific paths, and visual maps. The next step is to move from architecture notes into a local working AI Gateway skeleton.
