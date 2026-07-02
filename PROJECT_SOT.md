# Project Source of Truth

## Project Name

Enterprise Agentic Workflow Consulting Lab

## Purpose

This private lab is designed to prepare for the Senior Consultant - Agent Developer role focused on LLMs, agentic workflows, enterprise AI gateways, RAG, MCP interoperability, governance, Responsible AI, observability, and cloud deployment patterns.

The goal is to build a practical, consulting-grade reference architecture that explains not only how to build AI agents, but why each design choice matters in an enterprise environment.

## What We Are Building

We are building a private enterprise-grade agentic AI workflow lab that demonstrates how an AI agent can:

- Receive enterprise user requests through an AI Gateway
- Use RAG to retrieve trusted internal knowledge
- Call approved tools through an MCP-style tool layer
- Apply OPA/Rego-style policy decisions before sensitive actions
- Generate audit evidence for every agent run
- Capture observability signals such as traces, latency, cost, tool calls, and policy decisions
- Explain platform choices across AWS Bedrock, Amazon SageMaker, Azure OpenAI / Microsoft Foundry, OpenAI, and local open-source models

## Why We Are Building This

This lab exists because enterprise AI agents must be more than chatbot demos.

In real consulting environments, AI agents need:

- Identity and access control
- Retrieval grounding
- Tool-use boundaries
- Governance policies
- Responsible AI controls
- Observability
- Audit evidence
- Deployment repeatability
- Platform decision clarity

This lab helps demonstrate how to move from AI experimentation to trusted enterprise agentic AI adoption.

## What This Lab Is

This lab is:

- A private hands-on learning environment
- A consulting-grade reference architecture
- A platform decision guide
- A practical interview preparation asset
- A secure agentic workflow design pattern
- A place to document why, when, when not, and how to use key platforms and frameworks

## What This Lab Is Not

This lab is not:

- A production customer system
- A live customer data processing environment
- A replacement for enterprise approval workflows
- A model training platform by default
- A generic chatbot demo
- A system where agents have unrestricted tool access
- A system where LLM decisions override security controls
- A system that requires live AWS, Azure, or OpenAI accounts in Phase 1

## Core Architecture Principle

Every agent action must be:

- Authenticated
- Authorized
- Policy checked
- Grounded where needed
- Observable
- Auditable
- Reproducible

## Build Philosophy

This lab starts cloud-neutral and local-first.

The purpose is to understand the architecture before connecting to paid or managed cloud services. Platform-specific guides will explain how the same pattern maps to AWS Bedrock, Amazon SageMaker, Azure OpenAI / Microsoft Foundry, OpenAI, and local open-source models.

Live cloud deployment is optional and should only happen after architecture, governance, cost boundaries, and security controls are understood.

## Interview Positioning

This lab supports the following interview message:

I do not treat AI agents as simple chatbot demos. I treat them as enterprise services that require identity, policy, retrieval, tool contracts, observability, and governance from the beginning. This lab demonstrates how I would design and explain trusted agentic workflows for enterprise clients.
