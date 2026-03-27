"""
Jarvis — AgentOS App

Exposes the Jarvis team via a REST API using AgentOS.
Includes WhatsApp webhook and daily report scheduler.

Run:
    .venvs/demo/bin/python -m uvicorn cookbook.jarvis.app:app --host 0.0.0.0 --port 7777 --reload

Or:
    .venvs/demo/bin/python cookbook/jarvis/app.py

Endpoints:
    http://localhost:7777/docs              — Swagger UI
    http://localhost:7777/v1/teams/...      — Jarvis team API
    http://localhost:7777/webhook/whatsapp  — WhatsApp webhook
    http://localhost:7777/schedules         — Scheduler API
"""

import logging
import os

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from agno.db.postgres import PostgresDb
from agno.os import AgentOS

from cookbook.jarvis.config import get_tenant_config
from cookbook.jarvis.jarvis import get_jarvis_team
from cookbook.jarvis.webhook import build_whatsapp_router

logger = logging.getLogger("jarvis.app")

# ---------------------------------------------------------------------------
# Tenant — load from environment
# ---------------------------------------------------------------------------

TENANT_ID = os.getenv("JARVIS_TENANT_ID", "demo")
tenant = get_tenant_config(TENANT_ID)

# ---------------------------------------------------------------------------
# Database — shared session/memory store
# ---------------------------------------------------------------------------

db = PostgresDb(
    id=f"jarvis-db-{tenant.tenant_id}",
    db_url=tenant.db_url,
)

# ---------------------------------------------------------------------------
# Jarvis team — coordinator + all specialist agents
# ---------------------------------------------------------------------------

jarvis_team = get_jarvis_team(tenant)

# ---------------------------------------------------------------------------
# AgentOS — REST API + Scheduler
# ---------------------------------------------------------------------------

_SECURITY_KEY = os.getenv("OS_SECURITY_KEY", "")

agent_os = AgentOS(
    id=f"jarvis-{tenant.tenant_id}",
    description=(
        f"Jarvis — Sistema Operacional de Inteligencia para {tenant.store_name}. "
        "API REST para interacao com os agentes especializados da loja."
    ),
    teams=[jarvis_team],
    db=db,
    scheduler=True,
    scheduler_poll_interval=30,
    # Pass the security key so AgentOS validates X-API-Key on protected routes
    security_key=_SECURITY_KEY if _SECURITY_KEY else None,
)
app: FastAPI = agent_os.get_app()

# ---------------------------------------------------------------------------
# CORS — allow the React frontend in dev and configured origins in prod
# ---------------------------------------------------------------------------

_ALLOWED_ORIGINS = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://localhost:3000",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in _ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Simple API-key guard for /v1/* routes when OS_SECURITY_KEY is set
# (AgentOS handles its own auth internally; this layer covers custom routes)
# ---------------------------------------------------------------------------


@app.middleware("http")
async def api_key_guard(request: Request, call_next):  # type: ignore[no-untyped-def]
    """Reject requests to /v1/* without a valid API key when key is configured."""
    if _SECURITY_KEY and request.url.path.startswith("/v1/"):
        provided = request.headers.get("X-API-Key", "")
        if provided != _SECURITY_KEY:
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})
    return await call_next(request)


# ---------------------------------------------------------------------------
# WhatsApp webhook
# ---------------------------------------------------------------------------

app.include_router(build_whatsapp_router())


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    agent_os.serve(
        app="cookbook.jarvis.app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "7777")),
        reload=os.getenv("RELOAD", "true").lower() == "true",
    )
