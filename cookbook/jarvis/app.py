"""
Jarvis — AgentOS App

Exposes the Jarvis team via a REST API using AgentOS.

Run:
    .venvs/demo/bin/python -m uvicorn cookbook.jarvis.app:app --host 0.0.0.0 --port 7777 --reload

Or:
    .venvs/demo/bin/python cookbook/jarvis/app.py

API available at:
    http://localhost:7777/v1/
    http://localhost:7777/docs
"""

import os

from agno.db.postgres import PostgresDb
from agno.os import AgentOS

from cookbook.jarvis.config import get_tenant_config
from cookbook.jarvis.jarvis import get_jarvis_team

# ---------------------------------------------------------------------------
# Tenant — load from environment (multi-tenant: one process per tenant,
# or extend this to load multiple tenants dynamically)
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
# AgentOS — REST API
# ---------------------------------------------------------------------------

agent_os = AgentOS(
    id=f"jarvis-{tenant.tenant_id}",
    description=(
        f"Jarvis — Sistema Operacional de Inteligência para {tenant.store_name}. "
        "API REST para interacao com os agentes especializados da loja."
    ),
    teams=[jarvis_team],
)
app = agent_os.get_app()


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
