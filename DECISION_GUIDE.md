# Platform Decision Guide

## Purpose

This guide explains when to use AWS Bedrock, Amazon SageMaker, OpenAI, Azure OpenAI / Microsoft Foundry, or local open-source models in enterprise agentic AI workflows.

The goal is not to choose a platform by brand name. The goal is to choose the platform that fits the workflow, data sensitivity, governance requirements, latency, cost, and operating model.

## Decision Summary

| Platform | Best For | Do Not Use First When |
|---|---|---|
| AWS Bedrock | Managed GenAI apps, RAG, agents, guardrails, AWS-native integration | You need full model weight or runtime control |
| Amazon SageMaker | Custom training, fine-tuning, MLOps, custom model hosting | You only need a fast managed RAG or agent app |
| OpenAI API | Fast LLM app development, strong tool calling, prototyping | Client requires AWS-only, Azure-only, or private hosting |
| Azure OpenAI / Microsoft Foundry | Microsoft-heavy enterprises, Entra ID, Azure governance, Copilot-style workflows | Client is AWS-first or requires cloud-neutral design |
| Local Open-Source Models | Self-hosting, data residency, model control, customization | Team lacks MLOps, GPU, or platform maturity |

## AWS Bedrock

Use Bedrock when:

- The client is AWS-first
- The team wants managed foundation model access
- The workflow needs RAG, agents, or guardrails
- The team wants to avoid managing GPU or model infrastructure
- IAM, CloudWatch, CloudTrail, and AWS-native controls are important

Do not use Bedrock first when:

- The client needs full model weight control
- The client needs deep custom training
- The required model is not available through Bedrock
- The architecture must be completely cloud-neutral

Best explanation:

Bedrock is best when the client wants to build secure GenAI applications quickly on AWS without managing model infrastructure.

## Amazon SageMaker

Use SageMaker when:

- The client needs custom model training
- Fine-tuning is required
- MLOps, model registry, experiments, and custom endpoints are required
- The team needs deeper control over model packaging and deployment

Do not use SageMaker first when:

- A managed foundation model and RAG are enough
- The team needs quick validation
- The team lacks ML engineering maturity

Best explanation:

SageMaker is stronger when the problem is model engineering and MLOps. Bedrock is stronger when the problem is fast, managed GenAI application development.

## OpenAI API

Use OpenAI when:

- The team wants fast access to strong LLM capability
- Function calling and structured outputs are important
- The client is comfortable with OpenAI as an external provider
- The goal is fast prototyping or application development

Do not use OpenAI first when:

- The client requires all workloads inside AWS or Azure
- Compliance does not approve external model APIs
- The client requires private model hosting or model weight control

Best explanation:

OpenAI can be a strong application development choice, but enterprise fit depends on data governance, procurement approval, provider strategy, and security requirements.

## Azure OpenAI / Microsoft Foundry

Use Azure OpenAI or Microsoft Foundry when:

- The client is Microsoft-first
- Entra ID, Azure Monitor, Microsoft Purview, Defender, and Azure governance are central
- The workflow aligns with Microsoft enterprise data and productivity systems
- The client wants Azure-native AI development and governance

Do not use it first when:

- The client is AWS-first
- The architecture must be cloud-neutral
- Azure governance is not part of the client operating model

Best explanation:

Foundry is a strong fit for Microsoft-heavy enterprises that want agent development, model evaluation, and governance aligned with Azure identity and management patterns.

## Local Open-Source Models

Use open-source models when:

- The client needs self-hosting
- Data residency or isolation requires local/private deployment
- Model customization is important
- Cost at scale favors owning the runtime
- The team has platform and MLOps maturity

Do not use open-source self-hosting first when:

- The team cannot operate GPU infrastructure
- Time-to-market is critical
- Security patching, monitoring, and model lifecycle ownership are unclear

Best explanation:

Open-source gives control, but control comes with operational responsibility.
