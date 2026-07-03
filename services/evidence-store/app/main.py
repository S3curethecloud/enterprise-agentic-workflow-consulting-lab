from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Literal
from uuid import uuid4
import hashlib
import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent.parent
EVIDENCE_RECORDS_PATH = BASE_DIR / "data" / "evidence-records.json"

Decision = Literal["ALLOW", "DENY", "REDACT", "APPROVAL_REQUIRED"]
HASH_ALGORITHM = "SHA-256"


app = FastAPI(
    title="Persistent Evidence Store",
    description="Local persistent evidence store for governed enterprise agentic workflows.",
    version="0.2.0",
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
    record_hash: str
    previous_record_hash: str | None
    hash_algorithm: str
    integrity_status: str


class EvidenceRecordListResponse(BaseModel):
    count: int
    records: list[EvidenceRecord]


class IntegrityVerificationResponse(BaseModel):
    record_count: int
    integrity_status: str
    verified_records: int
    failed_records: int
    failures: list[dict]


def read_records() -> list[dict]:
    if not EVIDENCE_RECORDS_PATH.exists():
        EVIDENCE_RECORDS_PATH.parent.mkdir(parents=True, exist_ok=True)
        EVIDENCE_RECORDS_PATH.write_text("[]", encoding="utf-8")

    return json.loads(EVIDENCE_RECORDS_PATH.read_text(encoding="utf-8"))


def write_records(records: list[dict]) -> None:
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


def verify_record_integrity(record: dict) -> bool:
    expected_hash = calculate_record_hash(record)
    return record.get("record_hash") == expected_hash


def verify_chain_integrity(records: list[dict]) -> tuple[str, int, int, list[dict]]:
    failures = []
    verified_records = 0

    for index, record in enumerate(records):
        expected_hash = calculate_record_hash(record)
        actual_hash = record.get("record_hash")

        if actual_hash != expected_hash:
            failures.append(
                {
                    "record_id": record.get("record_id"),
                    "failure_type": "record_hash_mismatch",
                    "expected_hash": expected_hash,
                    "actual_hash": actual_hash,
                }
            )
            continue

        expected_previous_hash = None if index == 0 else records[index - 1].get("record_hash")
        actual_previous_hash = record.get("previous_record_hash")

        if actual_previous_hash != expected_previous_hash:
            failures.append(
                {
                    "record_id": record.get("record_id"),
                    "failure_type": "previous_record_hash_mismatch",
                    "expected_previous_hash": expected_previous_hash,
                    "actual_previous_hash": actual_previous_hash,
                }
            )
            continue

        verified_records += 1

    failed_records = len(records) - verified_records
    integrity_status = "verified" if failed_records == 0 else "failed"

    return integrity_status, verified_records, failed_records, failures


@app.get("/health")
def health_check():
    records = read_records()
    integrity_status, verified_records, failed_records, _ = verify_chain_integrity(records)

    return {
        "service": "evidence-store",
        "status": "healthy",
        "record_count": len(records),
        "hash_algorithm": HASH_ALGORITHM,
        "integrity_status": integrity_status,
        "verified_records": verified_records,
        "failed_records": failed_records,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/evidence/records", response_model=EvidenceRecord)
def create_evidence_record(payload: EvidenceRecordCreateRequest):
    records = read_records()

    record = {
        "record_id": f"evidence-{uuid4()}",
        "workflow_id": payload.workflow_id,
        "trace_id": payload.trace_id,
        "user_id": payload.user_id,
        "request": payload.request,
        "final_decision": payload.final_decision,
        "final_status": payload.final_status,
        "grounded_context_found": payload.grounded_context_found,
        "source_count": payload.source_count,
        "policy_id": payload.policy_id,
        "tool_name": payload.tool_name,
        "tool_invoked": payload.tool_invoked,
        "stages": [stage.model_dump() for stage in payload.stages],
        "metadata": payload.metadata,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "previous_record_hash": get_previous_record_hash(records),
    }

    record["record_hash"] = calculate_record_hash(record)
    record["hash_algorithm"] = HASH_ALGORITHM
    record["integrity_status"] = "verified"

    records.append(record)
    write_records(records)

    return EvidenceRecord(**record)


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


@app.get("/evidence/integrity/verify", response_model=IntegrityVerificationResponse)
def verify_evidence_integrity():
    records = read_records()
    integrity_status, verified_records, failed_records, failures = verify_chain_integrity(records)

    return IntegrityVerificationResponse(
        record_count=len(records),
        integrity_status=integrity_status,
        verified_records=verified_records,
        failed_records=failed_records,
        failures=failures,
    )
