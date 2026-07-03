from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from uuid import uuid4
import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent.parent
APPROVALS_PATH = BASE_DIR / "data" / "approvals.json"


ApprovalStatus = Literal["pending", "approved", "rejected"]


app = FastAPI(
    title="Human Approval Workflow Service",
    description="Local approval service for review-required agent workflows.",
    version="0.1.0",
)


class ApprovalCreateRequest(BaseModel):
    workflow_id: str = Field(..., examples=["workflow-123"])
    trace_id: str = Field(..., examples=["trace-123"])
    agent_id: str = Field(..., examples=["agent-policy-support-v1"])
    requested_by: str = Field(..., examples=["ola.consultant"])
    approver: str = Field(..., examples=["ai-governance-reviewer"])
    review_reason: str = Field(..., examples=["Responsible AI review required."])
    rai_decision: str = Field(..., examples=["REVIEW_REQUIRED"])
    policy_decision: str = Field(..., examples=["APPROVAL_REQUIRED"])
    risk_tier: str = Field(..., examples=["medium"])
    data_classification: str = Field(..., examples=["confidential"])
    requested_action: str = Field(..., examples=["read_customer_record"])
    requested_tool: str = Field(..., examples=["query_policy"])


class ApprovalDecisionRequest(BaseModel):
    approver: str = Field(..., examples=["ai-governance-reviewer"])
    decision_reason: str = Field(..., examples=["Approved with business justification and source grounding."])


class ApprovalRecord(BaseModel):
    approval_id: str
    workflow_id: str
    trace_id: str
    agent_id: str
    requested_by: str
    approver: str
    review_reason: str
    rai_decision: str
    policy_decision: str
    risk_tier: str
    data_classification: str
    requested_action: str
    requested_tool: str
    approval_status: ApprovalStatus
    decision_reason: str | None
    created_at: str
    updated_at: str
    decided_at: str | None


class ApprovalListResponse(BaseModel):
    count: int
    approvals: list[ApprovalRecord]


def read_approvals() -> list[dict]:
    if not APPROVALS_PATH.exists():
        APPROVALS_PATH.parent.mkdir(parents=True, exist_ok=True)
        APPROVALS_PATH.write_text("[]", encoding="utf-8")

    return json.loads(APPROVALS_PATH.read_text(encoding="utf-8"))


def write_approvals(approvals: list[dict]) -> None:
    APPROVALS_PATH.write_text(json.dumps(approvals, indent=2), encoding="utf-8")


def find_approval(approvals: list[dict], approval_id: str) -> dict | None:
    return next(
        (approval for approval in approvals if approval["approval_id"] == approval_id),
        None,
    )


@app.get("/health")
def health_check():
    approvals = read_approvals()

    return {
        "service": "approval-service",
        "status": "healthy",
        "approval_count": len(approvals),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/approvals", response_model=ApprovalRecord)
def create_approval_request(payload: ApprovalCreateRequest):
    approvals = read_approvals()
    now = datetime.now(timezone.utc).isoformat()

    approval = ApprovalRecord(
        approval_id=f"approval-{uuid4()}",
        workflow_id=payload.workflow_id,
        trace_id=payload.trace_id,
        agent_id=payload.agent_id,
        requested_by=payload.requested_by,
        approver=payload.approver,
        review_reason=payload.review_reason,
        rai_decision=payload.rai_decision,
        policy_decision=payload.policy_decision,
        risk_tier=payload.risk_tier,
        data_classification=payload.data_classification,
        requested_action=payload.requested_action,
        requested_tool=payload.requested_tool,
        approval_status="pending",
        decision_reason=None,
        created_at=now,
        updated_at=now,
        decided_at=None,
    )

    approvals.append(approval.model_dump())
    write_approvals(approvals)

    return approval


@app.get("/approvals", response_model=ApprovalListResponse)
def list_approvals(status: ApprovalStatus | None = None):
    approvals = read_approvals()

    if status:
        approvals = [
            approval for approval in approvals
            if approval["approval_status"] == status
        ]

    return ApprovalListResponse(
        count=len(approvals),
        approvals=[ApprovalRecord(**approval) for approval in approvals],
    )


@app.get("/approvals/{approval_id}", response_model=ApprovalRecord)
def get_approval(approval_id: str):
    approvals = read_approvals()
    approval = find_approval(approvals, approval_id)

    if not approval:
        raise HTTPException(status_code=404, detail=f"Approval not found: {approval_id}")

    return ApprovalRecord(**approval)


@app.patch("/approvals/{approval_id}/approve", response_model=ApprovalRecord)
def approve_request(approval_id: str, payload: ApprovalDecisionRequest):
    approvals = read_approvals()
    approval = find_approval(approvals, approval_id)

    if not approval:
        raise HTTPException(status_code=404, detail=f"Approval not found: {approval_id}")

    if approval["approval_status"] != "pending":
        raise HTTPException(
            status_code=409,
            detail=f"Approval is already {approval['approval_status']}",
        )

    now = datetime.now(timezone.utc).isoformat()
    approval["approval_status"] = "approved"
    approval["approver"] = payload.approver
    approval["decision_reason"] = payload.decision_reason
    approval["updated_at"] = now
    approval["decided_at"] = now

    write_approvals(approvals)

    return ApprovalRecord(**approval)


@app.patch("/approvals/{approval_id}/reject", response_model=ApprovalRecord)
def reject_request(approval_id: str, payload: ApprovalDecisionRequest):
    approvals = read_approvals()
    approval = find_approval(approvals, approval_id)

    if not approval:
        raise HTTPException(status_code=404, detail=f"Approval not found: {approval_id}")

    if approval["approval_status"] != "pending":
        raise HTTPException(
            status_code=409,
            detail=f"Approval is already {approval['approval_status']}",
        )

    now = datetime.now(timezone.utc).isoformat()
    approval["approval_status"] = "rejected"
    approval["approver"] = payload.approver
    approval["decision_reason"] = payload.decision_reason
    approval["updated_at"] = now
    approval["decided_at"] = now

    write_approvals(approvals)

    return ApprovalRecord(**approval)
