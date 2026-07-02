# Platform Decision Guide

## Purpose

This guide explains how to choose between AWS Bedrock, Amazon SageMaker, Azure OpenAI / Microsoft Foundry, OpenAI API, and local open-source models for enterprise agentic AI workflows.

The goal is not to pick a platform by brand name. The goal is to choose the platform that best fits the business workflow, data sensitivity, governance model, cost target, latency requirement, and operating maturity of the client.

## Core Decision Principle

Start with the workflow, not the model.

Before choosing a platform, ask:

- What business workflow are we automating or assisting?
- Does the agent need to retrieve enterprise knowledge?
- Does the agent need to call tools or APIs?
- What data classifications are involved?
- Does the client require cloud-specific governance?
- Does the team need managed services or full control?
- What are the cost, latency, and reliability requirements?
- What evidence must be captured for audit and compliance?

## Platform Summary

| Platform | Best For | Not Best For |
|---|---|---|
| AWS Bedrock | Managed GenAI apps, RAG, agents, guardrails, AWS-native governance | Full model weight control or deep custom training |
| Amazon SageMaker | Custom model training, fine-tuning, MLOps, custom endpoints | Simple managed GenAI apps where Bedrock is enough |
| Azure OpenAI / Microsoft Foundry | Microsoft-heavy enterprises, Entra ID, Azure governance, Copilot-style workflows | AWS-first or cloud-neutral operating models |
| OpenAI API | Fast application development, strong model capability, function calling | Strict cloud-boundary or self-hosting requirements |
| Local Open-Source Models | Self-hosting, model control, data residency, customization | Teams without MLOps/GPU/platform maturity |

## Recommended Consulting Answer

I would not start by choosing a model or framework. I would start by understanding the workflow, data sensitivity, governance requirements, latency target, cost envelope, and operating model. From there, I would choose the platform that gives the client the best balance of speed, control, governance, and long-term maintainability.

## When Bedrock Is the Best Starting Point

Use Bedrock when:

- The client is AWS-first
- They want managed foundation model access
- They need RAG with AWS-native integration
- They want guardrails and governance controls
- They do not want to manage GPU or model infrastructure
- IAM, CloudWatch, CloudTrail, and AWS controls are already part of the operating model

Do not use Bedrock first when:

- The client needs direct control over model weights
- The client needs heavy custom model training
- The required model is not available in Bedrock
- The architecture must remain cloud-neutral
- The client wants to self-host all model workloads

## When SageMaker Is the Best Starting Point

Use SageMaker when:

- The client needs model training or fine-tuning
- The client needs custom inference endpoints
- MLOps, model registry, experiments, and model lifecycle management are required
- The team has ML engineering maturity
- The client needs deeper control over packaging and deployment

Do not use SageMaker first when:

- The goal is a fast RAG or agent proof-of-concept
- Managed foundation model access is enough
- The team does not have ML engineering capacity
- Speed and simplicity matter more than model customization

## When Azure OpenAI / Microsoft Foundry Is the Best Starting Point

Use Azure OpenAI / Microsoft Foundry when:

- The client is Microsoft-first
- Entra ID, Azure Monitor, Defender, Purview, and Azure governance are central
- The workflow connects to Microsoft 365 or enterprise Microsoft data systems
- The organization wants Azure-native AI development and governance
- Copilot-style enterprise workflows are a major goal

Do not use it first when:

- The client is AWS-first
- The client requires cloud-neutral design
- Azure governance is not part of the operating model
- Procurement or compliance favors a different AI provider

## When OpenAI API Is the Best Starting Point

Use OpenAI when:

- The team needs fast access to strong LLM capability
- Function calling and structured outputs are important
- The client is comfortable with an external provider
- The goal is rapid application development or prototype validation

Do not use OpenAI first when:

- The client requires all processing inside AWS or Azure
- External model APIs are not approved
- The client requires private model hosting
- Data residency requires local or dedicated infrastructure

## When Local Open-Source Models Are the Best Starting Point

Use local open-source models when:

- The client needs self-hosting
- Data residency or isolation is mandatory
- Model control is more important than managed simplicity
- The team has MLOps and platform maturity
- Cost at scale favors owning the runtime

Do not use local open-source first when:

- The team cannot operate GPU infrastructure
- Time-to-market is critical
- Security patching and model lifecycle ownership are unclear
- The client lacks observability and MLOps maturity

## Final Rule

Managed platforms reduce operational burden.

Self-hosted platforms increase control.

The right answer depends on which tradeoff the client can support.
