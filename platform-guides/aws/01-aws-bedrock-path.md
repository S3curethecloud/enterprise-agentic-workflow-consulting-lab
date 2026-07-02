# AWS Bedrock Path

## Purpose

This guide explains how the enterprise agentic workflow pattern maps to Amazon Bedrock.

Amazon Bedrock is best suited for managed generative AI application development on AWS. It gives teams access to foundation models, RAG through Knowledge Bases, agent capabilities, guardrails, and AWS-native security and observability integration without requiring the team to manage model infrastructure.

## When to Use Amazon Bedrock

Use Bedrock when:

- The client is AWS-first
- The team wants managed foundation model access
- The team needs to build RAG, chat, summarization, or agentic workflows quickly
- The team wants to reduce operational burden
- The organization already uses IAM, CloudWatch, CloudTrail, KMS, and other AWS controls
- The team wants model choice without managing GPU infrastructure
- The use case needs guardrails, logging, and enterprise governance patterns

## When Not to Use Amazon Bedrock First

Do not use Bedrock as the first choice when:

- The client needs full control over model weights
- The client needs deep custom training pipelines
- The client needs a model that is not available through Bedrock
- The client requires full cloud-neutral design
- The team wants to self-host all inference workloads
- The workload requires low-level GPU or inference runtime optimization

## Bedrock Versus SageMaker

Bedrock is best when the goal is managed GenAI application development.

SageMaker is best when the goal is custom model engineering, training, fine-tuning, custom hosting, experiment tracking, and MLOps.

Simple distinction:

```text
Use Bedrock when you want to build with foundation models.

Use SageMaker when you need to build, train, tune, host, and manage models.
Bedrock Enterprise Agent Pattern
Enterprise User
   |
   v
Enterprise AI Gateway
   |
   v
Amazon Bedrock Runtime
   |
   +--> Foundation Model
   |
   +--> Bedrock Knowledge Base
   |
   +--> Bedrock Guardrails
   |
   +--> Bedrock Agent / AgentCore pattern
   |
   v
AWS Tools / Lambda / APIs / Data Sources
   |
   v
CloudWatch / CloudTrail / Evidence Store
Bedrock in This Lab

In this private lab, Bedrock is represented as a platform path.

Phase 1 does not require a live AWS account.

The goal is to understand:

Why Bedrock exists
When Bedrock is the right choice
What Bedrock is not meant for
How Bedrock fits into RAG and agent workflows
How Bedrock maps to enterprise governance
How Bedrock integrates with AWS security and observability services
Bedrock Step Guide for a Future Live Demo

A future Bedrock live demo would follow these steps:

Confirm AWS account and region
Enable Bedrock model access
Create an IAM execution role
Create an S3 bucket for approved documents
Upload enterprise knowledge documents
Create a Bedrock Knowledge Base
Configure embeddings and vector storage
Select a foundation model
Create an agent or application backend
Add action groups through Lambda or API integration
Add Bedrock Guardrails
Enable CloudWatch logging
Validate CloudTrail visibility
Capture evidence for model calls, retrieval, tool calls, and policy decisions
IAM Design Notes

A Bedrock application should not run with broad administrator permissions.

Recommended IAM principles:

Use least privilege
Separate human admin roles from application execution roles
Restrict Bedrock model invocation to approved models
Restrict S3 document access to approved buckets
Restrict Lambda action groups to approved functions
Use CloudTrail for audit
Use KMS for encryption where required
Avoid embedding long-lived secrets in code

Example IAM design goal:

The agent runtime can invoke approved Bedrock models, retrieve approved knowledge base content, and call approved Lambda tools, but it cannot modify IAM, access unrelated S3 buckets, or call unapproved services.
RAG Design on Bedrock

Bedrock Knowledge Bases can support the RAG layer.

RAG flow:

User Question
   |
   v
Application / Agent
   |
   v
Bedrock Knowledge Base Retrieval
   |
   v
Relevant Enterprise Context
   |
   v
Foundation Model
   |
   v
Grounded Answer with Sources

Enterprise RAG controls:

Approved data sources only
Document classification metadata
Source tracking
Access filtering
Confidence threshold
Prompt injection checks
Audit evidence
Agentic Workflow on Bedrock

Bedrock can support agentic workflows where the model uses tools or action groups.

Agent flow:

User Request
   |
   v
Agent interprets task
   |
   v
Agent retrieves knowledge if needed
   |
   v
Agent selects approved action group
   |
   v
Policy check or application guardrail
   |
   v
Lambda/API tool executes if allowed
   |
   v
Agent returns governed response
What to Watch Carefully

Bedrock reduces infrastructure burden, but it does not remove the need for architecture discipline.

Watch for:

Overly broad IAM permissions
Uncontrolled document ingestion
Missing data classification
Missing audit evidence
No cost monitoring
No fallback path
No human approval for high-risk actions
Treating guardrails as the only governance layer
Allowing agents to call tools without policy checks
Responsible AI Controls

A Bedrock-based enterprise agent should include:

Guardrails
Source grounding
PII detection or redaction where required
Human approval for sensitive actions
Evaluation of model responses
Logging of retrieved context
Logging of tool calls
Clear disclosure when confidence is low
Evidence records for audit
Observability

Track:

Model selected
Prompt size
Completion size
Token usage if available
Latency
Retrieval time
Tool call time
Guardrail decision
Policy decision
Error rate
Cost estimate
Trace ID
Strong Interview Explanation

Amazon Bedrock is a strong fit when a client wants to build generative AI applications quickly on AWS without managing model infrastructure. I would use it for managed model access, RAG, agents, and guardrail patterns, especially when the client already uses AWS security and observability services. I would still evaluate SageMaker or self-hosted open-source models if the client needs deeper model customization, custom training, or full runtime control.
