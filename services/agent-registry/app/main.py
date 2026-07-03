from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
from uuid import uuid4
import json

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent.parent
AGENTS_PATH = BASE_DIR / "data" / "agents.json"


RiskTier = Literal["low", "medium", "high"]
AgentStatus = Literal["draft", "active", "deprecated", "disabled"]


app = FastAPI(
    title="Persistent Agent Registry",
    description="Local persistent registry for governed enterprise AI agents.",
    version="0.1.0",
)


class AgentCreateRequest(BaseModel):
    agent_name: str = Field(..., examples=["policy-support-agent"])
    version: str = Field(..., examples=["1.0.0"])
    owner: str = Field(..., examples=["ai-platform-team"])
    description: str = Field(..., examples=["Agent that supports policy lookup and controlled ticket creation."])
    capabilities: list[str] = Field(default_factory=list)
    allowed_tools: list[str] = Field(default_factory=list)
    risk_tier: RiskTier = "medium"
    data_access_scope: list[str] = Field(default_factory=list)
    status: AgentStatus = "draft"


class AgentRecord(BaseModel):
    agent_id: str
    agent_name: str
    version: str
    owner: str
    description: str
    capabilities: list[str]
    allowed_tools: list[str]
    risk_tier: RiskTier
    data_access_scope: list[str]
    status: AgentStatus
    created_at: str
    updated_at: str


class AgentListResponse(BaseModel):
    count: int
    agents: list[AgentRecord]


class AgentStatusUpdateRequest(BaseModel):
    status: AgentStatus


def read_agents() -> list[dict]:
    if not AGENTS_PATH.exists():
        AGENTS_PATH.parent.mkdir(parents=True, exist_ok=True)
        AGENTS_PATH.write_text("[]", encoding="utf-8")

    return json.loads(AGENTS_PATH.read_text(encoding="utf-8"))


def write_agents(agents: list[dict]) -> None:
    AGENTS_PATH.write_text(json.dumps(agents, indent=2), encoding="utf-8")


def find_agent(agents: list[dict], agent_id: str) -> dict | None:
    return next((agent for agent in agents if agent["agent_id"] == agent_id), None)


def agent_name_version_exists(agents: list[dict], agent_name: str, version: str) -> bool:
    return any(
        agent["agent_name"] == agent_name and agent["version"] == version
        for agent in agents
    )


@app.get("/health")
def health_check():
    agents = read_agents()

    return {
        "service": "agent-registry",
        "status": "healthy",
        "agent_count": len(agents),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/agents", response_model=AgentRecord)
def create_agent(payload: AgentCreateRequest):
    agents = read_agents()

    if agent_name_version_exists(agents, payload.agent_name, payload.version):
        raise HTTPException(
            status_code=409,
            detail=f"Agent already exists with name {payload.agent_name} and version {payload.version}",
        )

    now = datetime.now(timezone.utc).isoformat()

    agent = AgentRecord(
        agent_id=f"agent-{uuid4()}",
        agent_name=payload.agent_name,
        version=payload.version,
        owner=payload.owner,
        description=payload.description,
        capabilities=payload.capabilities,
        allowed_tools=payload.allowed_tools,
        risk_tier=payload.risk_tier,
        data_access_scope=payload.data_access_scope,
        status=payload.status,
        created_at=now,
        updated_at=now,
    )

    agents.append(agent.model_dump())
    write_agents(agents)

    return agent


@app.get("/agents", response_model=AgentListResponse)
def list_agents(status: AgentStatus | None = None, risk_tier: RiskTier | None = None):
    agents = read_agents()

    if status:
        agents = [agent for agent in agents if agent["status"] == status]

    if risk_tier:
        agents = [agent for agent in agents if agent["risk_tier"] == risk_tier]

    return AgentListResponse(
        count=len(agents),
        agents=[AgentRecord(**agent) for agent in agents],
    )


@app.get("/agents/{agent_id}", response_model=AgentRecord)
def get_agent(agent_id: str):
    agents = read_agents()
    agent = find_agent(agents, agent_id)

    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent not found: {agent_id}")

    return AgentRecord(**agent)


@app.patch("/agents/{agent_id}/status", response_model=AgentRecord)
def update_agent_status(agent_id: str, payload: AgentStatusUpdateRequest):
    agents = read_agents()
    agent = find_agent(agents, agent_id)

    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent not found: {agent_id}")

    agent["status"] = payload.status
    agent["updated_at"] = datetime.now(timezone.utc).isoformat()

    write_agents(agents)

    return AgentRecord(**agent)
