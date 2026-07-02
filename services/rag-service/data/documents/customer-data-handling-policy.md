# Customer Data Handling Policy

## Purpose

This policy defines how customer data should be handled in enterprise AI workflows.

## Customer Data Rules

Customer data must be protected using least privilege, access control, encryption, monitoring, and audit logging.

## AI Agent Access

AI agents may only access customer data when:

- The user is authorized
- The business purpose is approved
- The request is policy checked
- Data classification permits access
- Evidence is logged

## Prohibited Actions

AI agents must not:

- Expose customer data in logs
- Send customer data to unapproved providers
- Retrieve customer records without authorization
- Use customer data for model training without approval
- Perform customer-impacting actions without validation

## Required Controls

Customer data access requires:

- Role validation
- Data classification check
- Region validation
- Policy decision
- Evidence record
- Output review when sensitive content is involved

## Policy Decision

Access to customer records should default to approval required unless a policy explicitly allows the workflow.
