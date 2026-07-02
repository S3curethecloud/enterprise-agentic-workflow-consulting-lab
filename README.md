# Enterprise Agentic Workflow Consulting Lab

Private consulting-grade lab for designing, explaining, and implementing secure enterprise AI agents using LLMs, RAG, MCP-style interoperability, OPA/Rego-style governance, Responsible AI controls, and observability.

## Why This Lab Exists

This lab prepares for enterprise agent developer and AI consulting roles where the goal is not just to build a chatbot, but to build agentic workflows that can be trusted by real organizations.

The lab focuses on:

- LLM-powered agent development
- Retrieval-Augmented Generation
- Tool use and function calling
- MCP-style interoperability
- Enterprise AI Gateway patterns
- OPA/Rego-style policy controls
- Responsible AI controls
- OpenTelemetry-style observability
- Platform decision guides across AWS, Azure, OpenAI, and local open-source models

## Core Question

How do we design AI agents that are useful, interoperable, governable, observable, and safe enough for enterprise workflows?

## High-Level Architecture

```text
User / Business Application
   |
   v
Enterprise AI Gateway
   |
   v
Agent Runtime
   |---- RAG Service
   |---- MCP Tool Layer
   |---- Policy Engine
   |---- Evidence Service
   |
   v
Approved Enterprise Tools and Data Sources
Build Approach

This lab starts with notes, architecture, and local mock services before any live cloud deployment.

The first goal is to understand the why, when, when not, and how behind each architecture choice.

Phases
Phase	Name	Goal
1	Source of Truth and Learning Notes	Define the architecture and decision logic
2	AI Gateway Skeleton	Create a local gateway pattern
3	RAG Service	Add trusted enterprise retrieval
4	LLM Provider Decision Layer	Compare Bedrock, SageMaker, OpenAI, Azure OpenAI, and local models
5	MCP Tool Layer	Expose tools through controlled interfaces
6	Policy Engine	Add OPA/Rego-style governance decisions
7	Responsible AI Controls	Add provenance, safety, explainability, and approval patterns
8	Observability and Evidence	Trace agent runs, cost, latency, tools, and policy decisions
9	Platform Guides	Map the same pattern to AWS, Azure, OpenAI, and local stacks
10	Interview Story Pack	Convert lab work into STAR stories
Repository Status

Current phase: Phase 1 - Source of Truth and Learning Notes

Project Source of Truth

See PROJECT_SOT.md.
