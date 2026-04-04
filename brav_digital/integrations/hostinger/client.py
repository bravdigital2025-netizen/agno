"""Hostinger REST API client for Brav Digital.

Authentication:
    Bearer token — generate at:
    hPanel > ícone do perfil > Informações da conta > API > Gerar token
"""

import os
from typing import Any

import httpx

HOSTINGER_API_BASE = "https://api.hostinger.com"


class HostingerClient:
    """Low-level HTTP client for the Hostinger API."""

    def __init__(self, api_token: str | None = None) -> None:
        token = api_token or os.getenv("HOSTINGER_API_TOKEN", "")
        if not token:
            raise ValueError(
                "HOSTINGER_API_TOKEN nao definido. "
                "Gere em: hPanel > Perfil > Informacoes da conta > API."
            )
        self._client = httpx.Client(
            base_url=HOSTINGER_API_BASE,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=30.0,
            follow_redirects=True,
        )

    # ------------------------------------------------------------------
    # Account
    # ------------------------------------------------------------------

    def get_ssh_keys(self) -> list[dict[str, Any]]:
        resp = self._client.get("/api/account/v1/ssh-keys")
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # VPS
    # ------------------------------------------------------------------

    def list_vps(self) -> list[dict[str, Any]]:
        resp = self._client.get("/api/vps/v1/virtual-machines")
        resp.raise_for_status()
        return resp.json()

    def get_vps(self, vps_id: int) -> dict[str, Any]:
        resp = self._client.get(f"/api/vps/v1/virtual-machines/{vps_id}")
        resp.raise_for_status()
        return resp.json()

    def get_vps_metrics(self, vps_id: int) -> dict[str, Any]:
        resp = self._client.get(f"/api/vps/v1/virtual-machines/{vps_id}/metrics")
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # Domains
    # ------------------------------------------------------------------

    def list_domains(self) -> list[dict[str, Any]]:
        resp = self._client.get("/api/domains/v1/portfolio")
        resp.raise_for_status()
        return resp.json()

    def list_subdomains(self) -> list[dict[str, Any]]:
        resp = self._client.get("/api/domains/v1/subdomains")
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # DNS
    # ------------------------------------------------------------------

    def list_dns_records(self, domain: str) -> list[dict[str, Any]]:
        resp = self._client.get(f"/api/dns/v1/zones/{domain}/records")
        resp.raise_for_status()
        return resp.json()

    def create_dns_record(
        self,
        domain: str,
        record_type: str,
        name: str,
        content: str,
        ttl: int = 14400,
    ) -> dict[str, Any]:
        payload = {"type": record_type, "name": name, "content": content, "ttl": ttl}
        resp = self._client.post(f"/api/dns/v1/zones/{domain}/records", json=payload)
        resp.raise_for_status()
        return resp.json()

    def delete_dns_record(self, domain: str, record_id: int) -> None:
        resp = self._client.delete(f"/api/dns/v1/zones/{domain}/records/{record_id}")
        resp.raise_for_status()

    # ------------------------------------------------------------------
    # Billing
    # ------------------------------------------------------------------

    def list_orders(self) -> list[dict[str, Any]]:
        resp = self._client.get("/api/billing/v1/orders")
        resp.raise_for_status()
        return resp.json()

    def list_subscriptions(self) -> list[dict[str, Any]]:
        resp = self._client.get("/api/billing/v1/subscriptions")
        resp.raise_for_status()
        return resp.json()

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "HostingerClient":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()
