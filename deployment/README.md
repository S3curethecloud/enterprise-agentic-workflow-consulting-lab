# Deployment Readiness

## Purpose

This folder documents how the Enterprise Agentic Workflow Consulting Lab maps from local services to deployable enterprise platform components.

The lab remains local-first, but Phase 17 adds deployment readiness artifacts so the architecture can be explained as a production-grade pattern.

## Services

| Service | Local Port | Purpose |
|---|---:|---|
| ai-gateway | 8001 | Request intake, risk scoring, model route decision |
| rag-service | 8002 | Trusted knowledge retrieval and grounding |
| mcp-server | 8003 | MCP-style enterprise tool layer |
| policy-engine | 8004 | Governance decision service |
| evidence-store | 8005 | Persistent evidence and hash-chain storage |
| agent-registry | 8006 | Persistent governed agent registry |
| approval-service | 8007 | Human approval workflow |
| agent-orchestrator | 8008 | End-to-end governed agent workflow |

## Local Docker Run

From the repository root:

```bash
docker compose build
docker compose up

Health checks:

curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health
curl http://localhost:8005/health
curl http://localhost:8006/health
curl http://localhost:8007/health
curl http://localhost:8008/health
Production Direction

In production, local JSON files should be replaced with managed persistence:

PostgreSQL
DynamoDB
Azure Cosmos DB
Google Firestore
S3/Object Storage for evidence bundles
Managed workflow engine for approvals

Service-to-service communication should replace shared local file mounts.
