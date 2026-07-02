# Roadmap

## Phase 1 - Source of Truth and Learning Notes

Goal: Define what the lab is, why it exists, and how it maps to the Senior Consultant - Agent Developer role.

Deliverables:

- PROJECT_SOT.md
- README.md
- ROADMAP.md
- ARCHITECTURE.md
- DECISION_GUIDE.md
- Initial docs and visuals

Status: In progress

## Phase 2 - AI Gateway Skeleton

Goal: Build the controlled entry point for agent requests.

Capabilities:

- Request intake
- Identity simulation
- Prompt risk scoring
- Model routing placeholder
- Audit ID generation
- Policy handoff

Status: Not started

## Phase 3 - RAG Service

Goal: Build trusted enterprise knowledge retrieval.

Capabilities:

- Local documents
- Chunking
- Embeddings placeholder
- Retrieval
- Source citations
- Confidence metadata
- RAG evidence

Status: Not started

## Phase 4 - LLM Provider Decision Layer

Goal: Explain and simulate when to use Bedrock, SageMaker, OpenAI, Azure OpenAI / Foundry, or local open-source models.

Status: Not started

## Phase 5 - MCP Tool Layer

Goal: Expose approved tools through an MCP-style interface.

Tools:

- search_internal_docs
- query_policy
- read_customer_record
- create_ticket

Status: Not started

## Phase 6 - Policy Engine

Goal: Add OPA/Rego-style policy decisions.

Decisions:

- ALLOW
- DENY
- REDACT
- APPROVAL_REQUIRED

Status: Not started

## Phase 7 - Responsible AI Controls

Goal: Add safety, provenance, explainability, and human approval controls.

Status: Not started

## Phase 8 - Observability and Evidence

Goal: Capture trace, metrics, cost, token usage, latency, policy decisions, and tool calls.

Status: Not started

## Phase 9 - Platform Guides

Goal: Document how this pattern maps to real platforms.

Platforms:

- AWS Bedrock
- Amazon SageMaker
- Azure OpenAI / Microsoft Foundry
- OpenAI API
- Local open-source Llama-style models

Status: Not started

## Phase 10 - Interview Story Pack

Goal: Convert lab work into STAR stories and simple interview explanations.

Status: Not started
