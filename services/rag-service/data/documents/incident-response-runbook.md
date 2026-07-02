# Incident Response Runbook

## Purpose

This runbook defines how teams should respond to security and operational incidents involving AI systems, cloud services, or enterprise applications.

## Incident Severity

### Low

Minor issue with no customer or production impact.

### Medium

Issue affecting internal users, non-critical systems, or degraded service.

### High

Production impact, customer data exposure risk, security control failure, or unauthorized access.

### Critical

Active breach, confirmed data exposure, privilege escalation, production compromise, or regulatory reporting concern.

## AI Agent Incident Handling

If an AI agent detects a possible incident, it should:

- Collect relevant context
- Retrieve approved runbook guidance
- Avoid making unauthorized changes
- Create a ticket if allowed
- Escalate high-risk events to a human operator
- Log evidence for review

## Restricted Actions

AI agents must not independently:

- Disable security controls
- Rotate production credentials
- Delete logs
- Modify production infrastructure
- Approve their own remediation actions

## Policy Decision

High and critical incidents require human review before remediation actions are executed.
