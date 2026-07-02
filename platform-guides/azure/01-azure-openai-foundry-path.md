# Azure OpenAI and Microsoft Foundry Path

## Purpose

This guide explains how the enterprise agentic workflow pattern maps to Azure OpenAI and Microsoft Foundry.

Azure OpenAI and Microsoft Foundry are strong choices when the client is Microsoft-first and wants AI development aligned with Entra ID, Azure governance, Azure Monitor, Microsoft security services, Microsoft data platforms, and Copilot-style enterprise workflows.

## When to Use Azure OpenAI / Microsoft Foundry

Use Azure OpenAI or Microsoft Foundry when:

- The client is Microsoft-first
- The organization already uses Entra ID for identity
- Azure governance is part of the operating model
- The client uses Microsoft Purview, Defender, Azure Monitor, or Microsoft 365
- The workflow integrates with Microsoft enterprise data systems
- The client wants agent development, model evaluation, and governance inside the Azure ecosystem
- The enterprise wants strong alignment with Copilot-style workflows

## When Not to Use Azure OpenAI / Microsoft Foundry First

Do not use Azure OpenAI or Microsoft Foundry first when:

- The client is AWS-first
- The client requires a cloud-neutral design
- Azure governance is not part of the operating model
- The client needs a model or runtime not available in Azure
- The client requires self-hosting or direct model weight control
- Procurement or compliance has approved another provider path

## Azure OpenAI / Foundry Versus AWS Bedrock

Simple distinction:

```text
Use Azure OpenAI / Microsoft Foundry when the enterprise operating model is Microsoft-first.

Use AWS Bedrock when the enterprise operating model is AWS-first.

Both can support managed GenAI application patterns.

The decision should be based on:

Client cloud strategy
Identity provider
Data platform
Governance tools
Existing security operations
Model availability
Cost and latency requirements
Compliance approval
Azure Enterprise Agent Pattern
Enterprise User
   |
   v
Entra ID
   |
   v
Business App / AI Gateway
   |
   v
Microsoft Foundry / Azure AI Platform
   |
   +--> Azure OpenAI Model Deployment
   |
   +--> RAG / Data Connection Layer
   |
   +--> Agent / Tool Workflow
   |
   +--> Safety and Evaluation Controls
   |
   v
Enterprise APIs / Data Sources
   |
   v
Azure Monitor / Evidence Store
Azure Path in This Lab

In this private lab, Azure OpenAI / Microsoft Foundry is represented as a platform path.

Phase 1 does not require a live Azure account.

The goal is to understand:

Why Azure OpenAI and Foundry exist
When they are the right enterprise choice
What they are not meant for
How Microsoft identity and governance influence platform selection
How the same RAG and agent workflow maps into Azure
How observability and evidence fit into Azure-native operations
Future Live Demo Step Guide

A future Azure OpenAI / Microsoft Foundry live demo would follow these steps:

Confirm Azure subscription and region
Confirm access to Azure OpenAI or Microsoft Foundry services
Create a resource group
Create or select an Azure AI Foundry project
Deploy or select an Azure OpenAI model
Configure identity through Entra ID or managed identity
Connect an approved data source for RAG
Define agent instructions and tool contracts
Add safety and evaluation controls
Add application API layer
Enable Azure Monitor logging and tracing
Capture evidence for model calls, retrieval, tool calls, and policy decisions
Identity Design Notes

Azure enterprise AI workloads should use identity-aware access patterns.

Recommended identity principles:

Use Entra ID for enterprise user identity
Use managed identity for service-to-service access
Avoid embedding secrets in code
Scope permissions to approved resources
Separate admin permissions from runtime permissions
Apply conditional access where appropriate
Log access and administrative activity

Example identity design goal:

The agent runtime can call approved Azure OpenAI deployments and approved enterprise tools using managed identity, but it cannot access unrelated resources or bypass enterprise policy controls.
RAG Design on Azure

Azure-based RAG can use an approved enterprise data source, a search or retrieval layer, and an Azure OpenAI model deployment.

RAG flow:

User Question
   |
   v
Application / Agent
   |
   v
Enterprise Data Retrieval
   |
   v
Relevant Enterprise Context
   |
   v
Azure OpenAI Model
   |
   v
Grounded Answer with Sources

Enterprise RAG controls:

Approved data sources only
Entra ID-aware access
Data classification metadata
Source tracking
Confidence threshold
Prompt injection checks
Output validation
Evidence logging
Agentic Workflow on Azure

An Azure agentic workflow can use a model deployment, tools, retrieval, and governance controls.

Agent flow:

User Request
   |
   v
Business App / AI Gateway
   |
   v
Agent interprets task
   |
   v
Agent retrieves knowledge if needed
   |
   v
Agent selects approved tool
   |
   v
Policy and authorization check
   |
   v
Tool executes if allowed
   |
   v
Agent returns governed response
What to Watch Carefully

Azure OpenAI and Foundry reduce some platform burden, but they do not remove architecture responsibility.

Watch for:

Weak managed identity design
Overly broad role assignments
Uncontrolled data source connections
Missing data classification
Missing output safety controls
Missing cost monitoring
No traceability for tool calls
No human approval for high-risk actions
No evidence record for compliance review
Assuming Microsoft-native means automatically governed
Responsible AI Controls

An Azure-based enterprise agent should include:

Safety controls
Source grounding
Evaluation
PII detection or redaction where required
Human approval for sensitive actions
Logging of retrieved context
Logging of tool calls
Provenance metadata
Explainability notes for policy decisions
Evidence records for audit
Observability

Track:

Model deployment used
Prompt size
Completion size
Latency
Retrieval time
Tool call time
Policy decision
Error rate
Cost estimate
Trace ID
Final response status
Human approval status where applicable
Strong Interview Explanation

I would use Azure OpenAI or Microsoft Foundry when the client is Microsoft-first and wants AI development aligned with Entra ID, Azure governance, Azure Monitor, Microsoft security services, and Microsoft enterprise data systems. The platform choice should follow the client's operating model. If the client is AWS-first, Bedrock may be a better fit. If the client needs self-hosting or direct model control, then a local or custom model platform may be better.
