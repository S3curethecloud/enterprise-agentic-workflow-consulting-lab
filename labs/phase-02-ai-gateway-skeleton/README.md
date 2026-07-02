# Phase 2 - Local AI Gateway Skeleton

## Purpose

This phase creates a local AI Gateway skeleton for the enterprise agentic workflow lab.

The gateway is the control point before the agent runtime, RAG service, MCP tools, policy engine, and LLM provider are called.

## Why This Matters

Enterprise AI applications should not allow users or applications to call models and tools directly without a control layer.

The AI Gateway provides a place to enforce:

- Request intake
- User context
- Prompt risk scoring
- Routing decisions
- Policy handoff
- Evidence creation
- Observability correlation through trace IDs

## What This Phase Builds

This phase builds a local FastAPI service with:

- GET /health
- POST /gateway/request

## What This Phase Does Not Build Yet

This phase does not yet include:

- Real LLM calls
- Real Bedrock calls
- Real OpenAI calls
- Real RAG retrieval
- Real MCP tool execution
- Real OPA/Rego policy evaluation

Those will be added in later phases.

## Interview Explanation

The AI Gateway is the front door for enterprise agentic workflows. It gives the organization a consistent place to apply identity, risk scoring, routing, policy handoff, observability, and evidence before an agent retrieves data or calls tools.
