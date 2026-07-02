from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(
    title="Enterprise AI Gateway Skeleton",
    description="Local AI Gateway skeleton for enterprise agentic workflow consulting lab.",
    version="0.1.0",
)


class GatewayRequest(BaseModel):
    user_id: str = Field(..., examples=["ola.consultant"])
    role: str = Field(..., examples=["security_architect"])
    department: str = Field(..., examples=["ai_platform"])
    request: str = Field(..., examples=["Search the internal AI policy and create a ticket if non-compliant."])
    data_region: str = Field(..., examples=["us"])
    risk_tier: Literal["low", "medium", "high"] = "medium"


class GatewayResponse(BaseModel):
    request_id: str
    trace_id: str
    user_id: str
    role: str
    department: str
    prompt_risk_score: int
    risk_label: Literal["low", "medium", "high"]
    routing_decision: str
    policy_handoff_required: bool
    evidence_created: bool
    timestamp: str
    status: str


def score_prompt_risk(request_text: str, risk_tier: str) -> tuple[int, str]:
    text = request_text.lower()

    score = 10

    sensitive_keywords = [
        "customer",
        "confidential",
        "pii",
        "delete",
        "payment",
        "credential",
        "secret",
        "production",
        "admin",
        "create ticket",
        "non-compliant",
    ]

    for keyword in sensitive_keywords:
        if keyword in text:
            score += 8

    if risk_tier == "medium":
        score += 20
    elif risk_tier == "high":
        score += 40

    score = min(score, 100)

    if score >= 70:
        return score, "high"
    if score >= 35:
        return score, "medium"
    return score, "low"


def choose_route(risk_label: str) -> str:
    if risk_label == "high":
        return "agent_runtime_with_policy_review"
    if risk_label == "medium":
        return "agent_runtime"
    return "direct_response_or_agent_runtime"


def requires_policy_handoff(risk_label: str, request_text: str) -> bool:
    text = request_text.lower()
    action_keywords = ["create", "update", "delete", "approve", "submit", "ticket", "customer", "payment"]
    return risk_label in ["medium", "high"] or any(keyword in text for keyword in action_keywords)


@app.get("/health")
def health_check():
    return {
        "service": "ai-gateway",
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/gateway/request", response_model=GatewayResponse)
def gateway_request(payload: GatewayRequest):
    request_id = f"req-{uuid4()}"
    trace_id = f"trace-{uuid4()}"

    score, risk_label = score_prompt_risk(payload.request, payload.risk_tier)
    route = choose_route(risk_label)
    policy_required = requires_policy_handoff(risk_label, payload.request)

    return GatewayResponse(
        request_id=request_id,
        trace_id=trace_id,
        user_id=payload.user_id,
        role=payload.role,
        department=payload.department,
        prompt_risk_score=score,
        risk_label=risk_label,
        routing_decision=route,
        policy_handoff_required=policy_required,
        evidence_created=True,
        timestamp=datetime.now(timezone.utc).isoformat(),
        status="accepted_for_agent_processing",
    )
