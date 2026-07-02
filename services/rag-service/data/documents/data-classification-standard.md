# Data Classification Standard

## Purpose

This standard defines how enterprise data should be classified before it is used by AI systems, applications, or agentic workflows.

## Classification Levels

### Public

Information approved for public release.

### Internal

Information intended for employees and approved contractors.

### Confidential

Sensitive business information, customer records, financial data, security architecture, credentials, private operational data, or regulated information.

### Restricted

Highly sensitive data requiring strict access control, human approval, and additional monitoring.

## AI Usage Rules

AI workflows may use public and internal data when approved for AI use.

Confidential data requires:

- User authorization
- Business justification
- Policy check
- Evidence logging
- Output validation

Restricted data requires:

- Human approval
- Explicit policy decision
- Enhanced logging
- Security review

## Retrieval Rules

RAG systems must filter retrieved content based on:

- User role
- Data classification
- Region
- Business purpose
- Approval status

## Policy Decision

If a user requests confidential or restricted information, retrieval must be filtered and the action may require approval.
