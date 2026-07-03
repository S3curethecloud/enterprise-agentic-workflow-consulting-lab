from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Literal
from uuid import uuid4
import hashlib
import json

from fastapi import FastAPI
from pydantic import BaseModel, Field


Decision = Literal["ALLOW", "DENY", "REDACT", "APPROVAL_REQUIRED"]

BASE_DIR = Path(__file__).resolve().parents[2]
EVIDENCE_RECORDS_PATH = BASE_DIR / "evidence-store" / "data" / "evidence-records.json"
AGENT_REGISTRY_PATH = BASE_DIR / "agent-registry" / "data" / "agents.json"
APPROVALS_PATH = BASE_DIR / "approval-service" / "data" / "approvals.json"


app = FastAPI(
    title="Local Agent Workflow Orchestrator",
    description="End-to-end local agent workflow simulation for enterprise agentic AI.",
    version="0.2.0",
)


class AgentWorkflowRequest(BaseModel):
    agent_id: str = Field(default="agent-policy-support-v1", examples=["agent-policy-support-v1"])
    user_id: str = Field(..., examples=["ola.consultant"])
    role: str = Field(..., examples=["security_architect"])
    department: str = Field(default="ai_platform", examples=["ai_platform"])
    request: str = Field(..., examples=["Search policy and create a ticket if confidential data access requires approval."])
    action: str = Field(default="search_internal_docs", examples=["create_ticket"])
    tool_name: str = Field(default="search_internal_docs", examples=["create_ticket"])
    data_classification: Literal["public", "internal", "confidential", "restricted"] = "internal"
    user_region: str = Field(default="us", examples=["us"])
    data_region: str = Field(default="us", examples=["us"])
    risk_tier: Literal["low", "medium", "high"] = "medium"
    approval_present: bool = False
    pii_detected: bool = False
    business_justification: str | None = Field(default=None, examples=["Policy review"])


class WorkflowStage(BaseModel):
    stage_name: str
    status: str
    details: Dict[str, Any]


class WorkflowTraceEvent(BaseModel):
    event_id: str
    trace_id: str
    workflow_id: str
    stage_name: str
    event_type: str
    status: str
    latency_ms: int
    timestamp: str
    details: Dict[str, Any]


class PerformanceTelemetry(BaseModel):
    gateway_latency_ms: int
    rag_latency_ms: int
    policy_latency_ms: int
    tool_latency_ms: int
    evidence_latency_ms: int
    total_latency_ms: int
    performance_slo_ms: int
    performance_slo_status: str


class CostTelemetry(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost_usd: float
    cost_model: str
    cost_note: str


class ResponsibleAIEvaluation(BaseModel):
    safety_risk: str
    bias_risk: str
    explainability_score: float
    source_provenance_status: str
    human_review_required: bool
    rai_decision: str
    rai_reason: str


class AgentWorkflowResponse(BaseModel):
    workflow_id: str
    trace_id: str
    user_id: str
    agent_id: str
    agent_name: str | None
    agent_version: str | None
    agent_registry_status: str
    agent_registry_decision: str
    agent_registry_reason: str
    final_decision: Decision
    final_status: str
    grounded_context_found: bool
    tool_invoked: bool
    tool_name: str | None
    stages: list[WorkflowStage]
    evidence_summary: Dict[str, Any]
    trace_timeline: list[WorkflowTraceEvent]
    stage_event_count: int
    total_latency_ms: int
    performance_telemetry: PerformanceTelemetry
    cost_telemetry: CostTelemetry
    performance_slo_status: str
    responsible_ai_evaluation: ResponsibleAIEvaluation
    rai_decision: str
    rai_reason: str
    human_review_required: bool
    approval_required: bool
    approval_id: str | None
    approval_status: str | None
    approval_reason: str | None
    approval_service_status: str
    approval_record_created: bool
    evidence_record_id: str
    evidence_persisted: bool
    record_hash: str
    previous_record_hash: str | None
    hash_algorithm: str
    integrity_status: str
    timestamp: str


def score_gateway_risk(request_text: str, risk_tier: str) -> tuple[int, str, bool, str]:
    lowered = request_text.lower()
    score = 20

    if risk_tier == "medium":
        score += 25
    elif risk_tier == "high":
        score += 50

    sensitive_terms = [
        "customer",
        "confidential",
        "restricted",
        "credential",
        "production",
        "delete",
        "disable",
        "override",
        "ticket",
    ]

    for term in sensitive_terms:
        if term in lowered:
            score += 8

    score = min(score, 100)

    if score >= 70:
        risk_label = "high"
    elif score >= 40:
        risk_label = "medium"
    else:
        risk_label = "low"

    policy_handoff_required = risk_label in ["medium", "high"]

    if risk_label == "high":
        route = "agent_runtime_with_policy_review"
    elif risk_label == "medium":
        route = "agent_runtime"
    else:
        route = "direct_response_or_agent_runtime"

    return score, risk_label, policy_handoff_required, route


def retrieve_grounded_context(query: str) -> tuple[bool, float, list[dict]]:
    lowered = query.lower()

    sources = []

    if "policy" in lowered or "confidential" in lowered or "customer" in lowered:
        sources.append(
            {
                "source_file": "customer-data-handling-policy.md",
                "snippet": "Customer data access requires role validation, data classification check, policy decision, evidence record, and output review.",
                "classification_hint": "confidential",
                "score": 85,
            }
        )

    if "ticket" in lowered or "incident" in lowered or "approval" in lowered:
        sources.append(
            {
                "source_file": "internal-ai-policy.md",
                "snippet": "AI agents must produce audit evidence and require human approval for high-risk actions.",
                "classification_hint": "internal",
                "score": 72,
            }
        )

    if not sources:
        return False, 0.0, []

    confidence = min(sources[0]["score"] / 100, 0.95)
    return True, round(confidence, 2), sources[:3]


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


def evaluate_policy(payload: AgentWorkflowRequest) -> tuple[Decision, str, str]:
    if contains_prompt_injection(payload.request):
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
            "Restricted data access requires explicit approval before execution.",
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


def invoke_tool_if_allowed(tool_name: str, payload: AgentWorkflowRequest) -> tuple[bool, dict]:
    if tool_name == "search_internal_docs":
        return True, {
            "tool_name": tool_name,
            "result": "Internal document search completed through controlled tool contract.",
            "query": payload.request,
        }

    if tool_name == "query_policy":
        return True, {
            "tool_name": tool_name,
            "result": "Policy query completed through controlled tool contract.",
            "action": payload.action,
            "data_classification": payload.data_classification,
        }

    if tool_name == "create_ticket":
        return True, {
            "tool_name": tool_name,
            "ticket_id": f"ticket-{uuid4()}",
            "status": "created",
            "title": "Agent workflow policy review",
            "severity": payload.risk_tier,
        }

    if tool_name == "read_customer_record":
        return True, {
            "tool_name": tool_name,
            "customer_id": "cust-001",
            "status": "read_simulated",
            "warning": "Synthetic lab response only. Real access requires enterprise authorization.",
        }

    return False, {
        "tool_name": tool_name,
        "error": "Tool not found in orchestrator simulation.",
    }


def read_evidence_records() -> list[dict]:
    EVIDENCE_RECORDS_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not EVIDENCE_RECORDS_PATH.exists():
        EVIDENCE_RECORDS_PATH.write_text("[]", encoding="utf-8")

    return json.loads(EVIDENCE_RECORDS_PATH.read_text(encoding="utf-8"))


def write_evidence_records(records: list[dict]) -> None:
    EVIDENCE_RECORDS_PATH.write_text(json.dumps(records, indent=2), encoding="utf-8")

def canonical_record_payload(record: dict) -> dict:
    excluded_fields = {
        "record_hash",
        "hash_algorithm",
        "integrity_status",
    }

    return {
        key: value
        for key, value in record.items()
        if key not in excluded_fields
    }


def calculate_record_hash(record: dict) -> str:
    canonical_payload = canonical_record_payload(record)
    serialized = json.dumps(canonical_payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def get_previous_record_hash(records: list[dict]) -> str | None:
    if not records:
        return None

    return records[-1].get("record_hash")




def persist_evidence_record(
    workflow_id: str,
    trace_id: str,
    payload: AgentWorkflowRequest,
    final_decision: Decision,
    final_status: str,
    grounded_context_found: bool,
    source_count: int,
    policy_id: str,
    tool_invoked: bool,
    stages: list[WorkflowStage],
    trace_timeline: list[WorkflowTraceEvent],
    performance_telemetry: PerformanceTelemetry,
    cost_telemetry: CostTelemetry,
    agent: dict | None,
    agent_registry_status: str,
    agent_registry_decision: str,
    agent_registry_reason: str,
    responsible_ai_evaluation: ResponsibleAIEvaluation,
    approval_required: bool,
    approval_id: str | None,
    approval_status: str | None,
    approval_reason: str | None,
    approval_service_status: str,
    approval_record_created: bool,
) -> str:
    records = read_evidence_records()
    record_id = f"evidence-{uuid4()}"

    record = {
        "record_id": record_id,
        "workflow_id": workflow_id,
        "trace_id": trace_id,
        "user_id": payload.user_id,
        "request": payload.request,
        "final_decision": final_decision,
        "final_status": final_status,
        "grounded_context_found": grounded_context_found,
        "source_count": source_count,
        "policy_id": policy_id,
        "tool_name": payload.tool_name if tool_invoked else None,
        "tool_invoked": tool_invoked,
        "stages": [stage.model_dump() for stage in stages],
        "metadata": {
            "service": "agent-orchestrator",
            "phase": "phase-14",
            "department": payload.department,
            "role": payload.role,
            "business_justification": payload.business_justification,
            "agent_id": payload.agent_id,
            "agent_name": agent["agent_name"] if agent else None,
            "agent_version": agent["version"] if agent else None,
            "agent_registry_status": agent_registry_status,
            "agent_registry_decision": agent_registry_decision,
            "agent_registry_reason": agent_registry_reason,
                "responsible_ai_evaluation": responsible_ai_evaluation.model_dump(),
                "rai_decision": responsible_ai_evaluation.rai_decision,
                "rai_reason": responsible_ai_evaluation.rai_reason,
                "human_review_required": responsible_ai_evaluation.human_review_required,
            "approval_required": approval_required,
            "approval_id": approval_id,
            "approval_status": approval_status,
            "approval_reason": approval_reason,
            "approval_service_status": approval_service_status,
            "approval_record_created": approval_record_created,
            "stage_event_count": len(trace_timeline),
            "total_latency_ms": calculate_total_latency(trace_timeline),
            "trace_timeline": [event.model_dump() for event in trace_timeline],
            "performance_telemetry": performance_telemetry.model_dump(),
            "cost_telemetry": cost_telemetry.model_dump(),
            "performance_slo_status": performance_telemetry.performance_slo_status,
        },
        "created_at": datetime.now(timezone.utc).isoformat(),
        "previous_record_hash": get_previous_record_hash(records),
    }

    record["record_hash"] = calculate_record_hash(record)
    record["hash_algorithm"] = "SHA-256"
    record["integrity_status"] = "verified"

    records.append(record)
    write_evidence_records(records)

    return record_id


def read_agent_registry() -> list[dict]:
    if not AGENT_REGISTRY_PATH.exists():
        AGENT_REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
        AGENT_REGISTRY_PATH.write_text("[]", encoding="utf-8")

    return json.loads(AGENT_REGISTRY_PATH.read_text(encoding="utf-8"))


def find_registered_agent(agent_id: str) -> dict | None:
    agents = read_agent_registry()
    return next((agent for agent in agents if agent["agent_id"] == agent_id), None)


def risk_rank(risk_tier: str) -> int:
    ranks = {
        "low": 1,
        "medium": 2,
        "high": 3,
    }
    return ranks.get(risk_tier, 0)


def evaluate_agent_registry_access(payload: AgentWorkflowRequest) -> tuple[str, str, str, dict | None]:
    agent = find_registered_agent(payload.agent_id)

    if not agent:
        return (
            "DENY",
            "agent_not_found",
            f"Agent not found in registry: {payload.agent_id}",
            None,
        )

    if agent["status"] != "active":
        return (
            "DENY",
            "agent_not_active",
            f"Agent status is {agent['status']}; only active agents may execute workflows.",
            agent,
        )

    if payload.tool_name not in agent["allowed_tools"]:
        return (
            "DENY",
            "tool_not_allowed",
            f"Tool {payload.tool_name} is not allowed for agent {agent['agent_name']}.",
            agent,
        )

    if payload.data_classification not in agent["data_access_scope"]:
        return (
            "DENY",
            "data_scope_not_allowed",
            f"Data classification {payload.data_classification} is not in agent data access scope.",
            agent,
        )

    if risk_rank(payload.risk_tier) > risk_rank(agent["risk_tier"]):
        return (
            "DENY",
            "risk_tier_exceeded",
            f"Workflow risk tier {payload.risk_tier} exceeds agent risk tier {agent['risk_tier']}.",
            agent,
        )

    return (
        "ALLOW",
        "agent_registry_allowed",
        "Agent is active and authorized for requested tool, data scope, and risk tier.",
        agent,
    )


def build_trace_event(
    workflow_id: str,
    trace_id: str,
    stage_name: str,
    event_type: str,
    status: str,
    latency_ms: int,
    details: dict,
) -> WorkflowTraceEvent:
    return WorkflowTraceEvent(
        event_id=f"event-{uuid4()}",
        trace_id=trace_id,
        workflow_id=workflow_id,
        stage_name=stage_name,
        event_type=event_type,
        status=status,
        latency_ms=latency_ms,
        timestamp=datetime.now(timezone.utc).isoformat(),
        details=details,
    )


def calculate_total_latency(trace_timeline: list[WorkflowTraceEvent]) -> int:
    return sum(event.latency_ms for event in trace_timeline)


def read_approval_records() -> list[dict]:
    if not APPROVALS_PATH.exists():
        APPROVALS_PATH.parent.mkdir(parents=True, exist_ok=True)
        APPROVALS_PATH.write_text("[]", encoding="utf-8")

    return json.loads(APPROVALS_PATH.read_text(encoding="utf-8"))


def write_approval_records(approvals: list[dict]) -> None:
    APPROVALS_PATH.write_text(json.dumps(approvals, indent=2), encoding="utf-8")


def create_approval_record(
    workflow_id: str,
    trace_id: str,
    payload: AgentWorkflowRequest,
    decision: Decision,
    responsible_ai_evaluation: ResponsibleAIEvaluation,
) -> dict:
    approvals = read_approval_records()
    now = datetime.now(timezone.utc).isoformat()

    approval = {
        "approval_id": f"approval-{uuid4()}",
        "workflow_id": workflow_id,
        "trace_id": trace_id,
        "agent_id": payload.agent_id,
        "requested_by": payload.user_id,
        "approver": "ai-governance-reviewer",
        "review_reason": responsible_ai_evaluation.rai_reason,
        "rai_decision": responsible_ai_evaluation.rai_decision,
        "policy_decision": decision,
        "risk_tier": payload.risk_tier,
        "data_classification": payload.data_classification,
        "requested_action": payload.action,
        "requested_tool": payload.tool_name,
        "approval_status": "pending",
        "decision_reason": None,
        "created_at": now,
        "updated_at": now,
        "decided_at": None,
    }

    approvals.append(approval)
    write_approval_records(approvals)

    return approval


def evaluate_responsible_ai(
    payload: AgentWorkflowRequest,
    decision: Decision,
    grounded_context_found: bool,
    source_count: int,
) -> ResponsibleAIEvaluation:
    request_lower = payload.request.lower()

    unsafe_terms = [
        "bypass",
        "ignore policy",
        "disable guardrail",
        "exfiltrate",
        "secret",
        "credential",
        "password",
    ]

    bias_terms = [
        "race",
        "religion",
        "gender",
        "age",
        "nationality",
        "ethnicity",
        "disability",
    ]

    safety_risk = "low"
    bias_risk = "low"
    human_review_required = False

    if any(term in request_lower for term in unsafe_terms):
        safety_risk = "high"
        human_review_required = True

    if any(term in request_lower for term in bias_terms):
        bias_risk = "medium"
        human_review_required = True

    if payload.data_classification == "restricted":
        safety_risk = "high"
        human_review_required = True

    if decision in ["DENY", "APPROVAL_REQUIRED"]:
        human_review_required = True

    if grounded_context_found and source_count > 0:
        source_provenance_status = "grounded_sources_available"
        explainability_score = 0.91
    else:
        source_provenance_status = "insufficient_source_provenance"
        explainability_score = 0.42
        human_review_required = True

    if safety_risk == "high":
        rai_decision = "BLOCK"
        rai_reason = "Responsible AI evaluation blocked the workflow due to high safety risk."
    elif human_review_required:
        rai_decision = "REVIEW_REQUIRED"
        rai_reason = "Responsible AI evaluation requires human review due to risk, approval, or provenance conditions."
    else:
        rai_decision = "PASS"
        rai_reason = "Responsible AI evaluation passed with acceptable safety, bias, explainability, and provenance signals."

    return ResponsibleAIEvaluation(
        safety_risk=safety_risk,
        bias_risk=bias_risk,
        explainability_score=explainability_score,
        source_provenance_status=source_provenance_status,
        human_review_required=human_review_required,
        rai_decision=rai_decision,
        rai_reason=rai_reason,
    )


def estimate_tokens(text: str) -> int:
    # Simple deterministic local estimate: roughly 1 token per 4 characters.
    return max(1, round(len(text) / 4))


def estimate_cost_usd(input_tokens: int, output_tokens: int) -> float:
    # Local placeholder based on a generic low-cost model estimate.
    # This is intentionally not tied to a live provider price.
    input_rate_per_1k = 0.00015
    output_rate_per_1k = 0.00060

    cost = (input_tokens / 1000 * input_rate_per_1k) + (output_tokens / 1000 * output_rate_per_1k)
    return round(cost, 6)


def build_performance_telemetry(trace_timeline: list[WorkflowTraceEvent]) -> PerformanceTelemetry:
    latency_by_stage = {event.stage_name: event.latency_ms for event in trace_timeline}
    evidence_latency_ms = 6
    total_latency_ms = calculate_total_latency(trace_timeline) + evidence_latency_ms
    performance_slo_ms = 250

    if total_latency_ms <= performance_slo_ms:
        slo_status = "within_slo"
    else:
        slo_status = "slo_breached"

    return PerformanceTelemetry(
        gateway_latency_ms=latency_by_stage.get("ai_gateway", 0) + latency_by_stage.get("agent_registry_enforcement", 0) + latency_by_stage.get("responsible_ai_evaluation", 0),
        rag_latency_ms=latency_by_stage.get("rag_retrieval", 0),
        policy_latency_ms=latency_by_stage.get("policy_evaluation", 0),
        tool_latency_ms=latency_by_stage.get("mcp_tool_invocation", 0),
        evidence_latency_ms=evidence_latency_ms,
        total_latency_ms=total_latency_ms,
        performance_slo_ms=performance_slo_ms,
        performance_slo_status=slo_status,
    )


def build_cost_telemetry(payload: AgentWorkflowRequest, grounded_context_found: bool, tool_invoked: bool) -> CostTelemetry:
    input_tokens = estimate_tokens(payload.request)

    # Output tokens are simulated based on whether the workflow retrieved context and invoked a tool.
    output_tokens = 80
    if grounded_context_found:
        output_tokens += 45
    if tool_invoked:
        output_tokens += 35

    total_tokens = input_tokens + output_tokens
    estimated_cost_usd = estimate_cost_usd(input_tokens, output_tokens)

    return CostTelemetry(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        total_tokens=total_tokens,
        estimated_cost_usd=estimated_cost_usd,
        cost_model="local-placeholder-generic-llm",
        cost_note="Deterministic local cost estimate for lab use only. Not tied to live provider pricing.",
    )


@app.get("/health")
def health_check():
    return {
        "service": "agent-orchestrator",
        "status": "healthy",
        "workflow": "gateway-rag-policy-mcp-evidence-trace-telemetry",
        "evidence_store_path": str(EVIDENCE_RECORDS_PATH),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/agent/workflow", response_model=AgentWorkflowResponse)
def agent_workflow(payload: AgentWorkflowRequest):
    workflow_id = f"workflow-{uuid4()}"
    trace_id = f"trace-{uuid4()}"
    stages: list[WorkflowStage] = []
    trace_timeline: list[WorkflowTraceEvent] = []

    agent_registry_decision, agent_registry_status, agent_registry_reason, agent = evaluate_agent_registry_access(payload)

    agent_registry_details = {
        "agent_id": payload.agent_id,
        "agent_name": agent["agent_name"] if agent else None,
        "agent_version": agent["version"] if agent else None,
        "agent_status": agent["status"] if agent else None,
        "agent_risk_tier": agent["risk_tier"] if agent else None,
        "agent_allowed_tools": agent["allowed_tools"] if agent else [],
        "agent_data_access_scope": agent["data_access_scope"] if agent else [],
        "agent_registry_decision": agent_registry_decision,
        "agent_registry_status": agent_registry_status,
        "agent_registry_reason": agent_registry_reason,
        "evidence_created": True,
    }

    stages.append(
        WorkflowStage(
            stage_name="agent_registry_enforcement",
            status="completed",
            details=agent_registry_details,
        )
    )

    trace_timeline.append(
        build_trace_event(
            workflow_id=workflow_id,
            trace_id=trace_id,
            stage_name="agent_registry_enforcement",
            event_type="agent_authorization_check",
            status="completed",
            latency_ms=7,
            details={
                "agent_id": payload.agent_id,
                "agent_registry_decision": agent_registry_decision,
                "agent_registry_status": agent_registry_status,
            },
        )
    )

    risk_score, risk_label, policy_handoff_required, routing_decision = score_gateway_risk(
        payload.request,
        payload.risk_tier,
    )

    gateway_details = {
        "prompt_risk_score": risk_score,
        "risk_label": risk_label,
        "policy_handoff_required": policy_handoff_required,
        "routing_decision": routing_decision,
        "evidence_created": True,
    }

    stages.append(
        WorkflowStage(
            stage_name="ai_gateway",
            status="completed",
            details=gateway_details,
        )
    )

    trace_timeline.append(
        build_trace_event(
            workflow_id=workflow_id,
            trace_id=trace_id,
            stage_name="ai_gateway",
            event_type="request_risk_routing",
            status="completed",
            latency_ms=12,
            details=gateway_details,
        )
    )

    grounded_context_found, confidence, sources = retrieve_grounded_context(payload.request)

    rag_details = {
        "grounded_context_found": grounded_context_found,
        "confidence": confidence,
        "source_count": len(sources),
        "sources": sources,
        "evidence_created": True,
    }

    stages.append(
        WorkflowStage(
            stage_name="rag_retrieval",
            status="completed",
            details=rag_details,
        )
    )

    trace_timeline.append(
        build_trace_event(
            workflow_id=workflow_id,
            trace_id=trace_id,
            stage_name="rag_retrieval",
            event_type="source_grounding",
            status="completed",
            latency_ms=18,
            details={
                "grounded_context_found": grounded_context_found,
                "confidence": confidence,
                "source_count": len(sources),
            },
        )
    )

    if agent_registry_decision == "DENY":
        decision = "DENY"
        policy_id = f"REGISTRY-{agent_registry_status.upper()}"
        reason = agent_registry_reason
    else:
        decision, policy_id, reason = evaluate_policy(payload)

    policy_details = {
        "decision": decision,
        "policy_id": policy_id,
        "reason": reason,
        "allowed_to_execute": decision == "ALLOW",
        "requires_approval": decision == "APPROVAL_REQUIRED",
        "requires_redaction": decision == "REDACT",
        "evidence_created": True,
    }

    stages.append(
        WorkflowStage(
            stage_name="policy_evaluation",
            status="completed",
            details=policy_details,
        )
    )

    trace_timeline.append(
        build_trace_event(
            workflow_id=workflow_id,
            trace_id=trace_id,
            stage_name="policy_evaluation",
            event_type="governance_decision",
            status="completed",
            latency_ms=9,
            details={
                "decision": decision,
                "policy_id": policy_id,
                "allowed_to_execute": decision == "ALLOW",
            },
        )
    )

    tool_invoked = False
    tool_result: dict[str, Any] = {}

    if decision == "ALLOW":
        tool_invoked, tool_result = invoke_tool_if_allowed(payload.tool_name, payload)
        tool_status = "completed" if tool_invoked else "failed"
    else:
        tool_status = "skipped"
        tool_result = {
            "message": "Tool invocation skipped because policy decision did not allow execution.",
            "decision": decision,
        }

    tool_details = {
        "tool_name": payload.tool_name,
        "tool_invoked": tool_invoked,
        "result": tool_result,
        "evidence_created": True,
    }

    stages.append(
        WorkflowStage(
            stage_name="mcp_tool_invocation",
            status=tool_status,
            details=tool_details,
        )
    )

    trace_timeline.append(
        build_trace_event(
            workflow_id=workflow_id,
            trace_id=trace_id,
            stage_name="mcp_tool_invocation",
            event_type="controlled_tool_execution",
            status=tool_status,
            latency_ms=15 if tool_invoked else 3,
            details={
                "tool_name": payload.tool_name,
                "tool_invoked": tool_invoked,
                "decision": decision,
            },
        )
    )

    if decision == "ALLOW":
        final_status = "workflow_completed"
    elif decision == "APPROVAL_REQUIRED":
        final_status = "workflow_waiting_for_approval"
    elif decision == "REDACT":
        final_status = "workflow_requires_redaction"
    else:
        final_status = "workflow_denied"

    responsible_ai_evaluation = evaluate_responsible_ai(
        payload=payload,
        decision=decision,
        grounded_context_found=grounded_context_found,
        source_count=len(sources),
    )

    rai_details = {
        "safety_risk": responsible_ai_evaluation.safety_risk,
        "bias_risk": responsible_ai_evaluation.bias_risk,
        "explainability_score": responsible_ai_evaluation.explainability_score,
        "source_provenance_status": responsible_ai_evaluation.source_provenance_status,
        "human_review_required": responsible_ai_evaluation.human_review_required,
        "rai_decision": responsible_ai_evaluation.rai_decision,
        "rai_reason": responsible_ai_evaluation.rai_reason,
        "evidence_created": True,
    }

    stages.append(
        WorkflowStage(
            stage_name="responsible_ai_evaluation",
            status="completed",
            details=rai_details,
        )
    )

    trace_timeline.append(
        build_trace_event(
            workflow_id=workflow_id,
            trace_id=trace_id,
            stage_name="responsible_ai_evaluation",
            event_type="rai_safety_provenance_review",
            status="completed",
            latency_ms=11,
            details={
                "rai_decision": responsible_ai_evaluation.rai_decision,
                "human_review_required": responsible_ai_evaluation.human_review_required,
                "source_provenance_status": responsible_ai_evaluation.source_provenance_status,
            },
        )
    )

    # Phase 14 final Responsible AI enforcement gate.
    # This ensures Responsible AI controls are applied before telemetry,
    # evidence persistence, and the final response are built.
    if responsible_ai_evaluation.rai_decision != "PASS":
        tool_invoked = False
        tool_status = "skipped"
        tool_result = {
            "message": "Tool invocation skipped because Responsible AI did not pass the workflow.",
            "decision": decision,
            "rai_decision": responsible_ai_evaluation.rai_decision,
        }

        for stage in stages:
            if stage.stage_name == "mcp_tool_invocation":
                stage.status = "skipped"
                stage.details["tool_invoked"] = False
                stage.details["tool_result"] = tool_result

        for event in trace_timeline:
            if event.stage_name == "mcp_tool_invocation":
                event.status = "skipped"
                event.latency_ms = 3
                event.details["tool_invoked"] = False
                event.details["rai_decision"] = responsible_ai_evaluation.rai_decision

    stage_order = {
        "agent_registry_enforcement": 1,
        "ai_gateway": 2,
        "rag_retrieval": 3,
        "policy_evaluation": 4,
        "responsible_ai_evaluation": 5,
        "mcp_tool_invocation": 6,
    }

    stages.sort(key=lambda stage: stage_order.get(stage.stage_name, 99))
    trace_timeline.sort(key=lambda event: stage_order.get(event.stage_name, 99))

    if responsible_ai_evaluation.rai_decision == "BLOCK":
        final_status = "workflow_blocked_by_responsible_ai"
    elif decision == "ALLOW" and responsible_ai_evaluation.rai_decision == "PASS":
        final_status = "workflow_completed"
    elif responsible_ai_evaluation.rai_decision == "REVIEW_REQUIRED":
        final_status = "workflow_waiting_for_approval"
    elif decision == "APPROVAL_REQUIRED":
        final_status = "workflow_waiting_for_approval"
    elif decision == "REDACT":
        final_status = "workflow_completed_with_redaction"
    else:
        final_status = "workflow_denied"

    approval_required = responsible_ai_evaluation.human_review_required
    approval_record_created = False
    approval_service_status = "not_required"
    approval_id = None
    approval_status = None
    approval_reason = None

    if approval_required:
        approval_record = create_approval_record(
            workflow_id=workflow_id,
            trace_id=trace_id,
            payload=payload,
            decision=decision,
            responsible_ai_evaluation=responsible_ai_evaluation,
        )

        approval_id = approval_record["approval_id"]
        approval_status = approval_record["approval_status"]
        approval_reason = approval_record["review_reason"]
        approval_service_status = "approval_created"
        approval_record_created = True

        approval_details = {
            "approval_required": approval_required,
            "approval_id": approval_id,
            "approval_status": approval_status,
            "approval_reason": approval_reason,
            "approval_service_status": approval_service_status,
            "approval_record_created": approval_record_created,
            "evidence_created": True,
        }

        stages.append(
            WorkflowStage(
                stage_name="human_approval_workflow",
                status="pending",
                details=approval_details,
            )
        )

        trace_timeline.append(
            build_trace_event(
                workflow_id=workflow_id,
                trace_id=trace_id,
                stage_name="human_approval_workflow",
                event_type="approval_request_created",
                status="pending",
                latency_ms=8,
                details={
                    "approval_id": approval_id,
                    "approval_status": approval_status,
                    "approval_record_created": approval_record_created,
                },
            )
        )

    stage_order = {
        "agent_registry_enforcement": 1,
        "ai_gateway": 2,
        "rag_retrieval": 3,
        "policy_evaluation": 4,
        "responsible_ai_evaluation": 5,
        "human_approval_workflow": 6,
        "mcp_tool_invocation": 7,
    }

    stages.sort(key=lambda stage: stage_order.get(stage.stage_name, 99))
    trace_timeline.sort(key=lambda event: stage_order.get(event.stage_name, 99))

    performance_telemetry = build_performance_telemetry(trace_timeline)
    cost_telemetry = build_cost_telemetry(
        payload=payload,
        grounded_context_found=grounded_context_found,
        tool_invoked=tool_invoked,
    )

    evidence_record_id = persist_evidence_record(
        workflow_id=workflow_id,
        trace_id=trace_id,
        payload=payload,
        final_decision=decision,
        final_status=final_status,
        grounded_context_found=grounded_context_found,
        source_count=len(sources),
        policy_id=policy_id,
        tool_invoked=tool_invoked,
        stages=stages,
        trace_timeline=trace_timeline,
        performance_telemetry=performance_telemetry,
        cost_telemetry=cost_telemetry,
        agent=agent,
        agent_registry_status=agent_registry_status,
        agent_registry_decision=agent_registry_decision,
        agent_registry_reason=agent_registry_reason,
        responsible_ai_evaluation=responsible_ai_evaluation,
        approval_required=approval_required,
        approval_id=approval_id,
        approval_status=approval_status,
        approval_reason=approval_reason,
        approval_service_status=approval_service_status,
        approval_record_created=approval_record_created,
    )

    evidence_records = read_evidence_records()
    persisted_record = next(record for record in evidence_records if record["record_id"] == evidence_record_id)

    evidence_summary = {
        "workflow_id": workflow_id,
        "trace_id": trace_id,
        "gateway_evidence": True,
        "rag_evidence": True,
        "policy_evidence": True,
        "tool_evidence": True,
        "source_count": len(sources),
        "final_policy_id": policy_id,
        "final_decision": decision,
        "agent_id": payload.agent_id,
        "agent_registry_status": agent_registry_status,
        "agent_registry_decision": agent_registry_decision,
        "agent_registry_reason": agent_registry_reason,
        "rai_decision": responsible_ai_evaluation.rai_decision,
        "rai_reason": responsible_ai_evaluation.rai_reason,
        "human_review_required": responsible_ai_evaluation.human_review_required,
        "approval_required": approval_required,
        "approval_id": approval_id,
        "approval_status": approval_status,
        "approval_reason": approval_reason,
        "approval_service_status": approval_service_status,
        "approval_record_created": approval_record_created,
        "evidence_record_id": evidence_record_id,
        "evidence_persisted": True,
        "stage_event_count": len(trace_timeline),
        "total_latency_ms": performance_telemetry.total_latency_ms,
        "performance_slo_status": performance_telemetry.performance_slo_status,
        "input_tokens": cost_telemetry.input_tokens,
        "output_tokens": cost_telemetry.output_tokens,
        "total_tokens": cost_telemetry.total_tokens,
        "estimated_cost_usd": cost_telemetry.estimated_cost_usd,
        "record_hash": persisted_record["record_hash"],
        "previous_record_hash": persisted_record["previous_record_hash"],
        "hash_algorithm": persisted_record["hash_algorithm"],
        "integrity_status": persisted_record["integrity_status"],
    }

    return AgentWorkflowResponse(
        workflow_id=workflow_id,
        trace_id=trace_id,
        user_id=payload.user_id,
        agent_id=payload.agent_id,
        agent_name=agent["agent_name"] if agent else None,
        agent_version=agent["version"] if agent else None,
        agent_registry_status=agent_registry_status,
        agent_registry_decision=agent_registry_decision,
        agent_registry_reason=agent_registry_reason,
        final_decision=decision,
        final_status=final_status,
        grounded_context_found=grounded_context_found,
        tool_invoked=tool_invoked,
        tool_name=payload.tool_name if tool_invoked else None,
        stages=stages,
        evidence_summary=evidence_summary,
        trace_timeline=trace_timeline,
        stage_event_count=len(trace_timeline),
        total_latency_ms=performance_telemetry.total_latency_ms,
        performance_telemetry=performance_telemetry,
        cost_telemetry=cost_telemetry,
        performance_slo_status=performance_telemetry.performance_slo_status,
        responsible_ai_evaluation=responsible_ai_evaluation,
        rai_decision=responsible_ai_evaluation.rai_decision,
        rai_reason=responsible_ai_evaluation.rai_reason,
        human_review_required=responsible_ai_evaluation.human_review_required,
        approval_required=approval_required,
        approval_id=approval_id,
        approval_status=approval_status,
        approval_reason=approval_reason,
        approval_service_status=approval_service_status,
        approval_record_created=approval_record_created,
        evidence_record_id=evidence_record_id,
        evidence_persisted=True,
        record_hash=persisted_record["record_hash"],
        previous_record_hash=persisted_record["previous_record_hash"],
        hash_algorithm=persisted_record["hash_algorithm"],
        integrity_status=persisted_record["integrity_status"],
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
