# Phase 17 Evidence - Cloud Platform Mapping and Deployment Readiness

## Phase Name

Phase 17 - Cloud Platform Mapping and Deployment Readiness

## Status

Complete

## Purpose

Phase 17 added cloud platform mapping and deployment readiness artifacts to the Enterprise Agentic Workflow Consulting Lab.

The purpose of this phase was to package the local governed agentic AI architecture into an enterprise-ready deployment pattern with Dockerfiles, Docker Compose, service contracts, environment configuration, readiness checklist, and cloud platform mapping.

## Why This Phase Matters

Before Phase 17:

```text
The lab demonstrated a local governed agentic workflow.

After Phase 17:

The lab demonstrates a deployable enterprise reference architecture with service boundaries, container packaging, and cloud platform mapping.

This makes the lab easier to explain in consulting, architecture review, and interview settings.

Built Components
Environment Template
.env.example
Docker Compose
docker-compose.yml
Service Dockerfiles
services/ai-gateway/Dockerfile
services/rag-service/Dockerfile
services/mcp-server/Dockerfile
services/policy-engine/Dockerfile
services/evidence-store/Dockerfile
services/agent-registry/Dockerfile
services/approval-service/Dockerfile
services/agent-orchestrator/Dockerfile
Deployment Documentation
deployment/README.md
deployment/SERVICE_CONTRACTS.md
deployment/DEPLOYMENT_READINESS_CHECKLIST.md
Platform Mapping
deployment/platform-mapping/aws-bedrock-mapping.md
deployment/platform-mapping/azure-openai-foundry-mapping.md
deployment/platform-mapping/openai-api-mapping.md
deployment/platform-mapping/local-open-source-mapping.md
Docker Compose Services

The Docker Compose configuration defines:

Service	Port	Purpose
ai-gateway	8001	Request intake, risk scoring, routing
rag-service	8002	Trusted retrieval and grounding
mcp-server	8003	MCP-style tool layer
policy-engine	8004	Governance decision service
evidence-store	8005	Persistent evidence and integrity
agent-registry	8006	Governed agent registry
approval-service	8007	Human approval workflow
agent-orchestrator	8008	End-to-end agent workflow orchestration
Validation Performed

The following validation commands were run:

find deployment -type f | sort
find services -name Dockerfile | sort
test -f docker-compose.yml && echo "docker-compose.yml present"
test -f .env.example && echo ".env.example present"
docker compose config
Validation Result

The files were present and Docker Compose configuration rendered successfully.

docker-compose.yml present
.env.example present
docker compose config succeeded
Platform Mapping Summary
AWS Bedrock Mapping

The lab maps to AWS using:

Amazon Bedrock
Bedrock Knowledge Bases
API Gateway
Lambda action groups
Step Functions
DynamoDB
S3 / S3 Object Lock
CloudWatch
X-Ray
EventBridge
ServiceNow or approval integration
Azure OpenAI / Microsoft Foundry Mapping

The lab maps to Azure using:

Azure OpenAI
Microsoft Foundry
Azure API Management
Azure AI Search
Azure Functions
Azure Container Apps or AKS
Azure Monitor
Application Insights
Logic Apps
Power Automate
Teams approvals
OpenAI API Mapping

The lab maps to OpenAI API using:

Enterprise AI Gateway
Custom orchestrator or LangGraph
OpenAI API tool/function calling
MCP-compatible tool servers
Vector database RAG layer
Policy service
Approval workflow
Evidence store
OpenTelemetry and SIEM
Local Open-Source Mapping

The lab maps to self-hosted open-source platforms using:

vLLM
Ollama
TGI
llama.cpp
Ray Serve
LangGraph
CrewAI
AutoGen
OPA/Rego
Qdrant, Weaviate, Milvus, OpenSearch, or pgvector
Prometheus
Grafana
Jaeger
OpenTelemetry
Enterprise Pattern Demonstrated

This phase demonstrates the following enterprise architecture pattern:

Local Governed Agentic AI Platform
   |
   v
Containerized Services
   |
   v
Service Contracts
   |
   v
Deployment Readiness Checklist
   |
   v
Cloud Platform Mapping
   |
   +--> AWS Bedrock
   +--> Azure OpenAI / Microsoft Foundry
   +--> OpenAI API
   +--> Local Open-Source Models
Service Boundary Pattern

The platform now has explicit boundaries for:

AI Gateway
RAG Service
MCP Tool Layer
Policy Engine
Evidence Store
Agent Registry
Approval Service
Agent Orchestrator

This supports modular deployment, independent scaling, better governance, clearer ownership, and cleaner interview explanation.

What This Phase Does Not Do Yet

This phase does not yet include:

Kubernetes manifests
Terraform modules
GitHub Actions CI/CD
Live AWS deployment
Live Azure deployment
Live OpenAI provider integration
Runtime service-to-service API calls replacing local mounts
Production secrets manager integration
OpenTelemetry collector deployment

These can be added in a later production-hardening version of the lab.

JD Alignment

This phase maps to the job description areas below:

JD Area	Phase 17 Alignment
Enterprise AI Gateway	Documents gateway deployment mapping
Local Execution Gateway	Adds Dockerized local service pattern
MCP Interoperability	Maps MCP server to enterprise tool layer
Agentic Workflows	Packages orchestrator and services for deployment
Cloud Platforms	Maps architecture to AWS, Azure, OpenAI, and local models
DevOps	Adds Dockerfiles and Docker Compose
Governance	Documents service contracts and readiness checklist
Consulting Delivery	Converts lab into explainable enterprise reference architecture
Interview Explanation

Phase 17 converts the local governed agentic AI lab into a deployment-ready reference architecture. I added Dockerfiles, Docker Compose, environment templates, service contracts, deployment readiness documentation, and platform mapping for AWS Bedrock, Azure OpenAI/Microsoft Foundry, OpenAI API, and local open-source model deployments. This shows how the same governed agentic workflow can be implemented locally and mapped to enterprise cloud platforms.

Phase 17 Closure Statement

Phase 17 is complete.

The lab now includes deployment readiness artifacts, container boundaries, service contracts, and cloud platform mapping. The next phase should create the final consulting demo package and interview story that ties the full lab back to the Infosys Senior Consultant Agent Developer job description.
