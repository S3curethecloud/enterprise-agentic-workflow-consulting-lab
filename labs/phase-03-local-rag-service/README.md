# Phase 3 - Local RAG Service

## Purpose

This phase creates a local Retrieval-Augmented Generation service for the Enterprise Agentic Workflow Consulting Lab.

The RAG service is the trusted knowledge layer that retrieves approved enterprise context before an agent generates an answer or calls a tool.

## Why This Matters

The AI Gateway controls the request.

The RAG service grounds the answer.

Together:

```text
AI Gateway = control point
RAG Service = trusted knowledge point

This creates the foundation for secure enterprise agentic workflows before MCP tool execution and OPA policy evaluation are introduced.

What This Phase Builds

This phase builds a local FastAPI service with:

GET /health
POST /rag/query

The RAG service can:

Load approved markdown documents
Search document content
Return source snippets
Return source file names
Return classification hints
Return confidence score
Return query_id and trace_id
Create an evidence flag
What This Phase Does Not Build Yet

This phase does not yet include:

Real embeddings
Vector database
Live LLM generation
Amazon Bedrock Knowledge Bases
Azure AI Search
OpenAI embeddings
MCP tool execution
OPA/Rego policy evaluation

Those will be added or mapped in later phases.

Why We Start Simple

This phase intentionally starts with deterministic local retrieval.

The goal is to understand the RAG architecture before introducing platform-specific services or paid APIs.

This helps explain:

Why RAG exists
What knowledge sources the agent used
Whether sources were found
What confidence was returned
Why source grounding matters
Why RAG does not replace policy controls
Interview Explanation

RAG is the trusted knowledge layer for enterprise agents. I would use it when answers need to come from approved internal policies, runbooks, or knowledge bases. In this lab, the RAG service retrieves source snippets, confidence, and metadata so the agent does not rely only on model memory. This supports governance, source grounding, and audit evidence.
