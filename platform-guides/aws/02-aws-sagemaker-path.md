# Amazon SageMaker Path

## Purpose

This guide explains how the enterprise agentic workflow pattern maps to Amazon SageMaker.

Amazon SageMaker is best suited for custom machine learning and model engineering workflows. It is useful when a team needs deeper control over model training, fine-tuning, deployment, experiments, model registry, custom inference endpoints, and MLOps lifecycle management.

SageMaker is not usually the first choice for a simple managed GenAI application if Amazon Bedrock can satisfy the requirement with less operational burden.

## When to Use Amazon SageMaker

Use SageMaker when:

- The client needs custom model training
- The client needs fine-tuning workflows
- The client needs custom inference endpoints
- The team needs experiment tracking
- The team needs model registry and model lifecycle management
- The client needs custom model packaging
- The team has ML engineering and MLOps maturity
- The model must be optimized for a specific use case
- The client needs more deployment control than Bedrock provides

## When Not to Use Amazon SageMaker First

Do not use SageMaker as the first choice when:

- The client only needs a managed foundation model
- The client is building a basic RAG assistant
- The client wants fast GenAI application validation
- The team does not have ML engineering capacity
- The team wants to avoid managing model endpoints
- The workload can be handled by Bedrock with less complexity

## SageMaker Versus Bedrock

Simple distinction:

```text
Use Bedrock when you want to build GenAI applications with managed foundation models.

Use SageMaker when you need to build, train, tune, host, and manage models.
Bedrock-First Reasoning

For many enterprise agentic AI workflows, Bedrock should be evaluated first because it reduces operational burden.

Good Bedrock-first use cases:

Enterprise chatbot
Policy assistant
RAG assistant
Support summarization
Knowledge search
Agentic workflow with managed models
Guardrail-enabled GenAI app
SageMaker-First Reasoning

SageMaker becomes stronger when the problem is no longer just application development.

Good SageMaker-first use cases:

Custom model training
Domain-specific model fine-tuning
Custom inference container
Model benchmarking
Batch inference at scale
Model registry and approval workflows
ML pipeline automation
Bring-your-own-model hosting
SageMaker Enterprise Agent Pattern
Enterprise User
   |
   v
Enterprise AI Gateway
   |
   v
Agent Runtime
   |
   +--> RAG Service
   |
   +--> Policy Engine
   |
   +--> Custom SageMaker Endpoint
   |
   v
Model Response
   |
   v
Evidence and Observability
SageMaker in This Lab

In this private lab, SageMaker is represented as a platform path.

Phase 1 does not require a live AWS account.

The goal is to understand:

Why SageMaker exists
When SageMaker is the right choice
What SageMaker is not meant for
How SageMaker differs from Bedrock
How SageMaker fits into enterprise model lifecycle management
How SageMaker can serve a custom model behind an agent runtime
Future Live Demo Step Guide

A future SageMaker live demo would follow these steps:

Confirm AWS account and region
Create SageMaker execution role
Prepare model artifact or select a deployable model
Create model package or model definition
Create endpoint configuration
Deploy real-time endpoint
Connect application or agent runtime to endpoint
Add IAM controls
Add CloudWatch monitoring
Add model registry if lifecycle governance is required
Add approval workflow for model promotion
Capture endpoint invocation evidence
IAM Design Notes

A SageMaker workload should follow least privilege.

Recommended IAM principles:

Separate data scientist roles from runtime execution roles
Restrict access to approved S3 model artifacts
Restrict endpoint invocation to approved applications
Limit who can create, update, or delete endpoints
Use CloudWatch logs for operational visibility
Use KMS for encryption where required
Avoid broad administrative permissions in execution roles

Example IAM design goal:

The agent runtime can invoke an approved SageMaker endpoint, but it cannot create new endpoints, modify model artifacts, or access unrelated S3 buckets.
Where SageMaker Fits in Agentic Workflows

SageMaker can serve as the model hosting layer for an agent runtime.

Example:

User Request
   |
   v
AI Gateway
   |
   v
Agent Runtime
   |
   v
Policy Check
   |
   v
RAG Context Retrieval
   |
   v
SageMaker Inference Endpoint
   |
   v
Response Validation
   |
   v
Evidence Record
What to Watch Carefully

SageMaker gives more control, but it also creates more operational responsibility.

Watch for:

Endpoint cost
Scaling configuration
Model drift
Model versioning
Patch management
Container vulnerabilities
Data leakage through training data
Weak model approval workflows
Missing monitoring
Unclear rollback strategy
Overengineering when Bedrock would be enough
Responsible AI Controls

A SageMaker-based AI workflow should include:

Model documentation
Training data lineage
Evaluation results
Bias and safety evaluation
Model approval workflow
Endpoint monitoring
Human approval for high-risk actions
Logging of prompt, context, output, and tool calls where appropriate
Evidence records for audit
Observability

Track:

Endpoint latency
Invocation count
Error rate
Model version
Input/output size
Cost estimate
RAG retrieval latency
Tool call latency
Policy decision
Trace ID
Final response status
Strong Interview Explanation

I would use SageMaker when the client needs deeper model engineering capabilities such as custom training, fine-tuning, model registry, custom endpoints, and MLOps. I would not start with SageMaker for every GenAI use case. If the client only needs managed model access, RAG, and agent workflows, Bedrock may be a faster and simpler starting point. SageMaker becomes the better fit when the client needs more control over the model lifecycle.
