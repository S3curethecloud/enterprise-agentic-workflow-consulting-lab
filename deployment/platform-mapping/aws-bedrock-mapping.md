# AWS Bedrock Platform Mapping

## Purpose

This document maps the local lab architecture to an AWS Bedrock-based enterprise agentic AI platform.

## Local-to-AWS Mapping

| Local Component | AWS Mapping |
|---|---|
| AI Gateway | API Gateway, Lambda, Amazon Bedrock Guardrails |
| Agent Orchestrator | AWS Step Functions, Lambda, ECS, or EKS |
| RAG Service | Amazon Bedrock Knowledge Bases, OpenSearch Serverless, Aurora pgvector |
| MCP Server | Lambda action groups, API Gateway, private APIs |
| Policy Engine | Cedar, Verified Permissions, OPA on ECS/EKS, Lambda policy service |
| Evidence Store | S3, DynamoDB, S3 Object Lock, CloudTrail Lake |
| Agent Registry | DynamoDB, Service Catalog, internal developer portal |
| Approval Service | Step Functions human approval, SNS, EventBridge, ServiceNow integration |
| Observability | CloudWatch, X-Ray, OpenTelemetry collector |
| Cost Telemetry | Bedrock usage metrics, Cost Explorer, CUR |

## Production Architecture

```text
Enterprise App
   |
   v
API Gateway / AI Gateway
   |
   v
Agent Orchestrator on Step Functions/ECS/EKS
   |
   +--> Bedrock Model / Bedrock Agent
   +--> Bedrock Knowledge Base
   +--> Lambda Action Groups
   +--> Policy Service
   +--> Agent Registry
   +--> Approval Workflow
   +--> Evidence Store
   |
   v
CloudWatch / X-Ray / SIEM
Interview Explanation

On AWS, I would map the local orchestrator to Step Functions, ECS, or EKS depending on runtime complexity. Bedrock provides managed model access, Knowledge Bases provide RAG, Lambda action groups support controlled tool execution, and S3/DynamoDB can preserve evidence. For governance, I would integrate policy evaluation, approval workflow, agent registry, trace telemetry, and Responsible AI controls around the Bedrock runtime.
