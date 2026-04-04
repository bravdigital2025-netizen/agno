"""Jarvis — Configuração central."""

import os
from dataclasses import dataclass


# Tenant config: each store is a tenant
@dataclass
class TenantConfig:
    tenant_id: str
    store_name: str
    db_url: str
    whatsapp_phone_id: str = ""
    whatsapp_token: str = ""


def get_tenant_config(tenant_id: str) -> TenantConfig:
    """Load tenant config from env variables."""
    return TenantConfig(
        tenant_id=tenant_id,
        store_name=os.getenv(f"TENANT_{tenant_id}_STORE_NAME", "Loja Demo"),
        db_url=os.getenv(
            "DATABASE_URL", "postgresql+psycopg://ai:ai@localhost:5532/ai"
        ),
        whatsapp_phone_id=os.getenv("WHATSAPP_PHONE_NUMBER_ID", ""),
        whatsapp_token=os.getenv("WHATSAPP_ACCESS_TOKEN", ""),
    )


# Default demo tenant
DEMO_TENANT = get_tenant_config("demo")
