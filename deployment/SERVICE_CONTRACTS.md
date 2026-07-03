# Service Contracts

## Purpose

This document captures the service boundaries for the Enterprise Agentic Workflow Consulting Lab.

Each service has a clear responsibility so the platform can be mapped to enterprise deployment patterns.

## AI Gateway

### Responsibility

- Accept user/application request
- Score request risk
- Route to approved model or workflow path
- Attach request_id and trace_id

### Production Mapping

- API Gateway
- Azure API Management
- Apigee
- Kong
- Envoy
- Enterprise AI Gateway

## RAG Service

### Responsibility

- Retrieve grounded enterprise context
- Return sources
- Return confidence/provenance metadata

### Production Mapping

- Bedrock Knowledge Bases
- Azure AI Search
- OpenSearch
- Pinecone
- pgvector
- LlamaIndex/LangChain retriever

## MCP Server

### Responsibility

- Expose approved tools
- Validate tool contract
- Simulate enterprise tool invocation

### Production Mapping

- MCP server
- Internal tool gateway
- Lambda-backed action groups
- API Gateway actions
- ServiceNow/Jira/Salesforce connectors

## Policy Engine

### Responsibility

- Evaluate governance rules
- Return ALLOW, DENY, REDACT, or APPROVAL_REQUIRED

### Production Mapping

- OPA/Rego
- Cedar
- Sentinel
- Azure Policy
- Custom authorization service

## Evidence Store

### Responsibility

- Persist workflow evidence
- Store trace and telemetry metadata
- Maintain tamper-evident hash chain

### Production Mapping

- S3 Object Lock
- DynamoDB
- PostgreSQL
- Immutable audit log
- SIEM evidence export

## Agent Registry

### Responsibility

- Register governed agents
- Track owner, version, status, capabilities, tools, and data scope

### Production Mapping

- Internal developer portal
- Service catalog
- Agent registry database
- Governance CMDB

## Approval Service

### Responsibility

- Create approval request
- Track pending, approved, rejected status
- Preserve decision reason and approver

### Production Mapping

- ServiceNow
- Jira Service Management
- Slack workflow
- Microsoft Teams approval
- Custom governance workflow engine

## Agent Orchestrator

### Responsibility

- Coordinate registry, gateway, RAG, policy, RAI, approval, tool execution, telemetry, and evidence

### Production Mapping

- LangGraph
- AutoGen
- CrewAI
- Step Functions
- Durable Functions
- Temporal
- Kubernetes service workflow
