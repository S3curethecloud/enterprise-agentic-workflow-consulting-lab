from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Literal
from uuid import uuid4
import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent.parent
EVIDENCE_RECORDS_PATH = BASE_DIR / "data" / "evidence-records.json"

Decision = Literal["ALLOW", "DENY", "REDACT", "APPROVAL_REQUIRED"]


app = FastAPI(
    title="Persistent Evidence Store",
    description="Local persistent evidence store for governed enterprise agentic workflows.",
    version="0.1.0",
)


class WorkflowStageEvidence(BaseModel):
    stage_name: str
    status: str
    details: Dict[str, Any]


class EvidenceRecordCreateRequest(BaseModel):
    workflow_id: str = Field(..., examples=["workflow-123"])
    trace_id: str = Field(..., examples=["trace-123"])
    user_id: str = Field(..., examples=["ola.consultant"])
    request: str = Field(..., examples=["Create a ticket after policy review."])
    final_decision: Decision
    final_status: str = Field(..., examples=["workflow_completed"])
    grounded_context_found: bool = False
    source_count: int = 0
    policy_id: str | None = Field(default=None, examples=["POL-DEFAULT-ALLOW"])
    tool_name: str | None = Field(default=None, examples=["create_ticket"])
    tool_invoked: bool = False
    stages: list[WorkflowStageEvidence]
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EvidenceRecord(BaseModel):
    record_id: str
    workflow_id: str
    trace_id: str
    user_id: str
    request: str
    final_decision: Decision
    final_status: str
    grounded_context_found: bool
    source_count: int
    policy_id: str | None
    tool_name: str | None
    tool_invoked: bool
    stages: list[WorkflowStageEvidence]
    metadata: Dict[str, Any]
    created_at: str


class EvidenceRecordListResponse(BaseModel):
    count: int
    records: list[EvidenceRecord]


def read_records() -> list[dict]:
    if not EVIDENCE_RECORDS_PATH.exists():
        EVIDENCE_RECORDS_PATH.parent.mkdir(parents=True, exist_ok=True)
        EVIDENCE_RECORDS_PATH.write_text("[]", encoding="utf-8")

    return json.loads(EVIDENCE_RECORDS_PATH.read_text(encoding="utf-8"))


def write_records(records: list[dict]) -> None:
    EVIDENCE_RECORDS_PATH.write_text(json.dumps(records, indent=2), encoding="utf-8")


@app.get("/health")
def health_check():
    records = read_records()

    return {
        "service": "evidence-store",
        "status": "healthy",
        "record_count": len(records),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/evidence/records", response_model=EvidenceRecord)
def create_evidence_record(payload: EvidenceRecordCreateRequest):
    records = read_records()

    record = EvidenceRecord(
        record_id=f"evidence-{uuid4()}",
        workflow_id=payload.workflow_id,
        trace_id=payload.trace_id,
        user_id=payload.user_id,
        request=payload.request,
        final_decision=payload.final_decision,
        final_status=payload.final_status,
        grounded_context_found=payload.grounded_context_found,
        source_count=payload.source_count,
        policy_id=payload.policy_id,
        tool_name=payload.tool_name,
        tool_invoked=payload.tool_invoked,
        stages=payload.stages,
        metadata=payload.metadata,
        created_at=datetime.now(timezone.utc).isoformat(),
    )

    records.append(record.model_dump())
    write_records(records)

    return record


@app.get("/evidence/records", response_model=EvidenceRecordListResponse)
def list_evidence_records():
    records = read_records()

    return EvidenceRecordListResponse(
        count=len(records),
        records=[EvidenceRecord(**record) for record in records],
    )


@app.get("/evidence/records/{record_id}", response_model=EvidenceRecord)
def get_evidence_record(record_id: str):
    records = read_records()

    for record in records:
        if record["record_id"] == record_id:
            return EvidenceRecord(**record)

    raise HTTPException(status_code=404, detail=f"Evidence record not found: {record_id}")


@app.get("/evidence/workflows/{workflow_id}", response_model=EvidenceRecordListResponse)
def get_records_by_workflow(workflow_id: str):
    records = read_records()
    matching_records = [
        EvidenceRecord(**record)
        for record in records
        if record["workflow_id"] == workflow_id
    ]

    return EvidenceRecordListResponse(
        count=len(matching_records),
        records=matching_records,
    )
