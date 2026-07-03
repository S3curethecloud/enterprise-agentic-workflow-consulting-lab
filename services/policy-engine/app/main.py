from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from uuid import uuid4
import json

from fastapi import FastAPI
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent.parent
POLICY_RULES_PATH = BASE_DIR / "policies" / "policy_rules.json"


Decision = Literal["ALLOW", "DENY", "REDACT", "APPROVAL_REQUIRED"]


app = FastAPI(
    title="Local Policy Engine",
    description="Deterministic policy engine for enterprise agentic workflow consulting lab.",
    version="0.1.0",
)


class PolicyEvaluationRequest(BaseModel):
    user_id: str = Field(..., examples=["ola.consultant"])
    role: str = Field(..., examples=["security_architect"])
    action: str = Field(..., examples=["read_customer_record"])
    tool_name: str | None = Field(default=None, examples=["read_customer_record"])
    data_classification: Literal["public", "internal", "confidential", "restricted"] = "internal"
    user_region: str = Field(default="us", examples=["us"])
    data_region: str = Field(default="us", examples=["us"])
    risk_tier: Literal["low", "medium", "high"] = "medium"
    approval_present: bool = False
    pii_detected: bool = False
    prompt_text: str = Field(default="", examples=["Read customer record for support investigation."])
    business_justification: str | None = Field(default=None, examples=["Support investigation"])


class PolicyEvaluationResponse(BaseModel):
    evaluation_id: str
    trace_id: str
    user_id: str
    action: str
    decision: Decision
    policy_id: str
    reason: str
    requires_approval: bool
    requires_redaction: bool
    allowed_to_execute: bool
    evidence_created: bool
    timestamp: str


def load_policy_rules() -> dict:
    return json.loads(POLICY_RULES_PATH.read_text(encoding="utf-8"))


def contains_prompt_injection(text: str) -> bool:
    lowered = text.lower()
    suspicious_phrases = [
        "ignore previous instructions",
        "ignore all previous instructions",
        "bypass policy",
        "override policy",
        "disable guardrails",
        "reveal secrets",
        "show me the system prompt",
        "act as admin",
        "jailbreak",
    ]
    return any(phrase in lowered for phrase in suspicious_phrases)


def is_region_mismatch(user_region: str, data_region: str) -> bool:
    if data_region.lower() == "global":
        return False
    return user_region.lower() != data_region.lower()


def evaluate_policy(payload: PolicyEvaluationRequest) -> tuple[Decision, str, str]:
    if contains_prompt_injection(payload.prompt_text):
        return (
            "DENY",
            "POL-AI-001",
            "Prompt injection or policy bypass language detected.",
        )

    if is_region_mismatch(payload.user_region, payload.data_region):
        return (
            "DENY",
            "POL-REGION-001",
            "User region and data region are incompatible.",
        )

    if payload.data_classification == "restricted" and not payload.approval_present:
        return (
            "DENY",
            "POL-DATA-002",
            "Restricted data access requires explicit approval before evaluation can proceed.",
        )

    if payload.pii_detected:
        return (
            "REDACT",
            "POL-PII-001",
            "PII detected and must be redacted before response is returned.",
        )

    if payload.risk_tier == "high" and not payload.approval_present:
        return (
            "APPROVAL_REQUIRED",
            "POL-TOOL-001",
            "High-risk tool or action requires approval before execution.",
        )

    if payload.data_classification == "confidential" and not payload.approval_present:
        return (
            "APPROVAL_REQUIRED",
            "POL-DATA-001",
            "Confidential data access requires approval before execution.",
        )

    return (
        "ALLOW",
        "POL-DEFAULT-ALLOW",
        "No blocking, redaction, or approval-required policy matched.",
    )


@app.get("/health")
def health_check():
    rules = load_policy_rules()
    return {
        "service": "policy-engine",
        "status": "healthy",
        "policy_version": rules["policy_version"],
        "rule_count": len(rules["rules"]),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/policy/evaluate", response_model=PolicyEvaluationResponse)
def policy_evaluate(payload: PolicyEvaluationRequest):
    decision, policy_id, reason = evaluate_policy(payload)

    requires_approval = decision == "APPROVAL_REQUIRED"
    requires_redaction = decision == "REDACT"
    allowed_to_execute = decision == "ALLOW"

    return PolicyEvaluationResponse(
        evaluation_id=f"eval-{uuid4()}",
        trace_id=f"trace-{uuid4()}",
        user_id=payload.user_id,
        action=payload.action,
        decision=decision,
        policy_id=policy_id,
        reason=reason,
        requires_approval=requires_approval,
        requires_redaction=requires_redaction,
        allowed_to_execute=allowed_to_execute,
        evidence_created=True,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
