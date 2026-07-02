# RAG Design Guide

## Purpose

This guide explains how Retrieval-Augmented Generation should be designed for enterprise agentic workflows.

RAG is used when the agent needs to answer using trusted enterprise knowledge instead of relying only on the model's training data.

## What RAG Means

RAG stands for Retrieval-Augmented Generation.

It combines:

- Retrieval: finding relevant information from approved sources
- Augmentation: adding that information to the model prompt
- Generation: producing an answer grounded in the retrieved context

## Basic RAG Flow

```text
User Question
   |
   v
Query Processing
   |
   v
Retriever
   |
   v
Relevant Document Chunks
   |
   v
Prompt Builder
   |
   v
LLM
   |
   v
Answer + Sources + Confidence + Evidence
Why Use RAG

Use RAG when:

The answer must come from enterprise-approved documents
The knowledge changes often
The model should provide citations or sources
The organization wants to reduce unsupported answers
The workflow involves policies, runbooks, procedures, or internal knowledge
Fine-tuning would be too expensive, slow, or unnecessary
Why RAG Before Fine-Tuning

RAG should usually come before fine-tuning for enterprise knowledge workflows.

Reasons:

Enterprise documents change frequently
RAG can update knowledge without retraining the model
RAG supports citations and provenance
RAG is easier to govern and audit
RAG is faster for early validation
RAG avoids putting sensitive knowledge directly into model weights
What RAG Is Best For

RAG is best for:

Policy Q&A
Compliance lookup
Runbook assistant workflows
Internal documentation search
Support triage
Architecture knowledge assistants
Customer service knowledge bases
Governance and control evidence lookup
What RAG Is Not Best For

RAG is not best for:

Replacing systems of record
Making high-risk decisions without validation
Handling sensitive data without access control
Answering from outdated or low-quality documents
Performing calculations without verified tools
Autonomous action without policy and approval controls
Enterprise RAG Design Decisions
1. Document Source

Start with approved local markdown files.

Future options:

S3
SharePoint
Confluence
Git repositories
Databases
Knowledge management systems
2. Chunking Strategy

Chunking splits documents into retrievable sections.

Good chunks should be:

Large enough to preserve meaning
Small enough to retrieve accurately
Linked to source metadata
Versioned where possible
3. Metadata

Every document chunk should include metadata.

Recommended metadata:

source_file
document_owner
classification
region
version
last_updated
business_domain
approved_for_ai_use
4. Retrieval Filtering

Retrieval should not only be based on semantic similarity.

It should also consider:

User role
Department
Data classification
Region
Business purpose
Policy restrictions
5. Confidence Scoring

The RAG service should return a confidence score or relevance score.

If confidence is low, the agent should:

Ask a clarifying question
Say the source is insufficient
Avoid making unsupported claims
Escalate to human review where needed
6. Source Grounding

For policy or compliance answers, the response should include source references.

The model should not answer policy questions without retrieved context unless clearly marked as general guidance.

7. Evidence

Every RAG response should generate evidence.

Evidence should include:

User question
Retrieved source names
Chunk IDs
Confidence score
Final answer
Timestamp
Trace ID
Policy decision if applicable
RAG Security Controls

Enterprise RAG requires:

Document classification
Access control
Retrieval filtering
PII detection
Source provenance
Prompt injection checks
Output validation
Evidence logging
RAG Anti-Patterns

Avoid these patterns:

Sending all documents directly into the prompt
Retrieving confidential data without checking user access
Trusting the highest similarity result blindly
Using outdated documents without version metadata
Allowing the LLM to invent sources
Treating RAG as a replacement for governance
Assuming RAG eliminates hallucinations completely
Strong Interview Explanation

RAG helps ground model responses in approved enterprise knowledge, but it does not automatically make an AI system trustworthy. A production RAG design still needs access control, document quality management, metadata, confidence thresholds, source citations, prompt injection protection, and audit evidence.
