from datetime import datetime, timezone
from pathlib import Path
from typing import List
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel, Field


DOCUMENT_DIR = Path(__file__).resolve().parent.parent / "data" / "documents"


app = FastAPI(
    title="Local RAG Service",
    description="Local retrieval service for enterprise agentic workflow consulting lab.",
    version="0.1.0",
)


class RAGQueryRequest(BaseModel):
    query: str = Field(..., examples=["What should an AI agent do before accessing confidential customer data?"])
    user_id: str = Field(..., examples=["ola.consultant"])
    role: str = Field(..., examples=["security_architect"])
    data_region: str = Field(default="us", examples=["us"])
    max_results: int = Field(default=3, ge=1, le=5)


class SourceResult(BaseModel):
    source_file: str
    snippet: str
    score: int
    classification_hint: str


class RAGQueryResponse(BaseModel):
    query_id: str
    trace_id: str
    user_id: str
    query: str
    result_count: int
    confidence: float
    sources: List[SourceResult]
    evidence_created: bool
    timestamp: str
    status: str


def load_documents() -> list[dict]:
    documents = []

    for path in sorted(DOCUMENT_DIR.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        documents.append(
            {
                "source_file": path.name,
                "content": content,
            }
        )

    return documents


def classify_document_hint(content: str) -> str:
    lowered = content.lower()

    if "restricted" in lowered:
        return "restricted"
    if "confidential" in lowered or "customer data" in lowered:
        return "confidential"
    if "internal" in lowered:
        return "internal"
    return "public"


def split_sentences(content: str) -> list[str]:
    normalized = content.replace("\n", " ")
    raw_parts = normalized.split(".")
    return [part.strip() for part in raw_parts if part.strip()]


def score_sentence(query: str, sentence: str) -> int:
    query_terms = {
        term.strip(".,:;!?()[]{}").lower()
        for term in query.split()
        if len(term.strip(".,:;!?()[]{}")) >= 4
    }

    sentence_lower = sentence.lower()
    score = 0

    for term in query_terms:
        if term in sentence_lower:
            score += 10

    important_terms = [
        "agent",
        "policy",
        "confidential",
        "customer",
        "approval",
        "evidence",
        "authorization",
        "retrieval",
        "restricted",
        "human",
    ]

    for term in important_terms:
        if term in query.lower() and term in sentence_lower:
            score += 15

    return score


def retrieve_sources(query: str, max_results: int) -> list[SourceResult]:
    candidates = []

    for document in load_documents():
        classification_hint = classify_document_hint(document["content"])

        for sentence in split_sentences(document["content"]):
            score = score_sentence(query, sentence)

            if score > 0:
                candidates.append(
                    SourceResult(
                        source_file=document["source_file"],
                        snippet=sentence,
                        score=score,
                        classification_hint=classification_hint,
                    )
                )

    candidates.sort(key=lambda item: item.score, reverse=True)
    return candidates[:max_results]


def calculate_confidence(sources: list[SourceResult]) -> float:
    if not sources:
        return 0.0

    top_score = sources[0].score
    confidence = min(top_score / 100, 0.95)
    return round(confidence, 2)


@app.get("/health")
def health_check():
    return {
        "service": "rag-service",
        "status": "healthy",
        "document_count": len(load_documents()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/rag/query", response_model=RAGQueryResponse)
def rag_query(payload: RAGQueryRequest):
    query_id = f"rag-{uuid4()}"
    trace_id = f"trace-{uuid4()}"

    sources = retrieve_sources(payload.query, payload.max_results)
    confidence = calculate_confidence(sources)

    status = "sources_found" if sources else "no_sources_found"

    return RAGQueryResponse(
        query_id=query_id,
        trace_id=trace_id,
        user_id=payload.user_id,
        query=payload.query,
        result_count=len(sources),
        confidence=confidence,
        sources=sources,
        evidence_created=True,
        timestamp=datetime.now(timezone.utc).isoformat(),
        status=status,
    )
