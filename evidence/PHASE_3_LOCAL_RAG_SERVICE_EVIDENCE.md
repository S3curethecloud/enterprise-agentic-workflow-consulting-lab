# Phase 3 Evidence - Local RAG Service

## Phase Name

Phase 3 - Local RAG Service

## Status

Complete

## Purpose

Phase 3 created a local Retrieval-Augmented Generation service for the Enterprise Agentic Workflow Consulting Lab.

The purpose of this phase was to build the trusted knowledge retrieval layer that enterprise agents use before generating answers or calling tools.

This phase supports the Senior Consultant - Agent Developer role by demonstrating how enterprise AI agents can retrieve grounded context from approved internal policies, runbooks, and standards without relying only on model memory.

## Why This Phase Matters

The AI Gateway controls the request.

The RAG service grounds the answer.

Together:

```text
AI Gateway = control point
RAG Service = trusted knowledge point

This creates the foundation for governed enterprise agentic workflows before MCP tool execution and OPA/Rego policy evaluation are introduced.

Built Components
Service
services/rag-service/app/main.py
Tests
services/rag-service/tests/test_rag.py
Requirements
services/rag-service/requirements.txt
Mock Enterprise Documents
services/rag-service/data/documents/internal-ai-policy.md
services/rag-service/data/documents/data-classification-standard.md
services/rag-service/data/documents/incident-response-runbook.md
services/rag-service/data/documents/customer-data-handling-policy.md
Lab Notes
labs/phase-03-local-rag-service/README.md
API Endpoints
GET /health

Purpose:

Validate that the RAG service is running and can load approved enterprise documents.

Example response includes:

service
status
document_count
timestamp
POST /rag/query

Purpose:

Accept an enterprise knowledge query and return relevant source snippets, source files, confidence score, trace ID, query ID, and evidence flag.

The RAG service currently simulates:

Local document loading
Deterministic keyword retrieval
Source snippet matching
Source file attribution
Classification hint assignment
Confidence scoring
Trace ID generation
Query ID generation
Evidence creation flag
Example Request
{
  "query": "What should an AI agent do before accessing confidential customer data?",
  "user_id": "ola.consultant",
  "role": "security_architect",
  "data_region": "us",
  "max_results": 3
}
Example Response Shape
{
  "query_id": "rag-generated-id",
  "trace_id": "trace-generated-id",
  "user_id": "ola.consultant",
  "query": "What should an AI agent do before accessing confidential customer data?",
  "result_count": 3,
  "confidence": 0.65,
  "sources": [
    {
      "source_file": "customer-data-handling-policy.md",
      "snippet": "AI agents may only access customer data when the user is authorized...",
      "score": 65,
      "classification_hint": "confidential"
    }
  ],
  "evidence_created": true,
  "timestamp": "generated-timestamp",
  "status": "sources_found"
}
Validation Result

The local RAG service passed tests.

3 passed in 0.46s
Test Coverage

The current test suite validates:

Health check endpoint returns healthy status
Service can load at least four approved enterprise documents
Confidential customer data query returns relevant sources
RAG response includes confidence score
RAG response includes evidence flag
Unrelated query returns no sources and zero confidence
Enterprise Pattern Demonstrated

This phase demonstrates the following pattern:

Enterprise Query
   |
   v
RAG Service
   |
   +--> Load approved documents
   +--> Search relevant content
   +--> Return source snippets
   +--> Return source file names
   +--> Return classification hints
   +--> Return confidence score
   +--> Create evidence stub
   |
   v
Grounded context for future agent response
What This Phase Does Not Do Yet

This phase does not yet include:

Real embeddings
Vector database
OpenAI embeddings
Amazon Bedrock Knowledge Bases
Azure AI Search
Live LLM response generation
MCP tool execution
OPA/Rego policy evaluation
OpenTelemetry export
Persistent evidence storage

These are intentionally deferred to later phases.

Why Deterministic Retrieval Was Used First

This phase intentionally starts with deterministic local retrieval.

The purpose is to make the RAG architecture easy to inspect, explain, test, and govern before introducing platform-specific retrieval services, embeddings, vector databases, or paid APIs.

This supports the lab philosophy:

Understand the enterprise architecture first.
Add managed platforms and advanced retrieval later.
JD Alignment

This phase maps to the job description areas below:

JD Area	Phase 3 Alignment
RAG	Builds local retrieval service over approved enterprise documents
Agent Development	Provides trusted context layer for future agent runtime
Enterprise Workflows	Uses policies, standards, and runbooks as enterprise knowledge
Responsible AI	Adds source grounding, confidence, and evidence placeholders
Governance	Includes classification hints and retrieval boundaries
API & Contracts	Uses FastAPI and structured Pydantic models
Observability	Adds query_id and trace_id for future trace correlation
Cloud-Neutral Design	Avoids live cloud dependency in early architecture phase
Interview Explanation

The RAG service is the trusted knowledge layer for enterprise agents. I built it after the AI Gateway because the gateway controls whether a request should proceed, while RAG controls what trusted context the agent can use to answer. In this lab, the RAG service retrieves approved policy and runbook snippets with source metadata, confidence, and evidence fields. That helps reduce unsupported answers and prepares the workflow for policy enforcement, MCP tools, and observability.

Phase 3 Closure Statement

Phase 3 is complete.

The lab now has a working local RAG service with tests passing. The next phase should introduce an MCP-style tool layer so the agent workflow can call approved tools through controlled contracts instead of directly accessing enterprise systems.
