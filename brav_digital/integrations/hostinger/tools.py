"""Hostinger Agno Toolkit for Brav Digital agents."""

import json
from typing import Any

from agno.tools import Toolkit

from .client import HostingerClient


class HostingerTools(Toolkit):
    """Agno toolkit that exposes Hostinger API actions to AI agents.

    Usage::

        from brav_digital.integrations.hostinger.tools import HostingerTools

        agent = Agent(tools=[HostingerTools()], ...)
    """

    def __init__(self, api_token: str | None = None) -> None:
        super().__init__(name="hostinger")
        self._h = HostingerClient(api_token=api_token)
        self.register(self.list_vps)
        self.register(self.get_vps_status)
        self.register(self.list_domains)
        self.register(self.list_dns_records)
        self.register(self.create_dns_record)
        self.register(self.list_subscriptions)

    # ------------------------------------------------------------------
    # VPS
    # ------------------------------------------------------------------

    def list_vps(self) -> str:
        """List all VPS instances in the Hostinger account."""
        try:
            vms = self._h.list_vps()
            result = [
                {
                    "id": v.get("id"),
                    "hostname": v.get("hostname"),
                    "state": v.get("state"),
                    "ip": v.get("main_ip"),
                    "os": v.get("template", {}).get("name") if isinstance(v.get("template"), dict) else v.get("template"),
                    "plan": v.get("plan"),
                    "datacenter": v.get("datacenter", {}).get("location") if isinstance(v.get("datacenter"), dict) else v.get("datacenter"),
                }
                for v in (vms if isinstance(vms, list) else vms.get("data", []))
            ]
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return f"Erro ao listar VPS: {e}"

    def get_vps_status(self, vps_id: int) -> str:
        """Get detailed status and metrics of a specific VPS.

        Args:
            vps_id: The numeric VPS ID from list_vps().
        """
        try:
            vps = self._h.get_vps(vps_id)
            metrics: dict[str, Any] = {}
            try:
                metrics = self._h.get_vps_metrics(vps_id)
            except Exception:
                pass
            return json.dumps({"vps": vps, "metrics": metrics}, ensure_ascii=False)
        except Exception as e:
            return f"Erro ao buscar VPS {vps_id}: {e}"

    # ------------------------------------------------------------------
    # Domains
    # ------------------------------------------------------------------

    def list_domains(self) -> str:
        """List all domains registered in the Hostinger account."""
        try:
            domains = self._h.list_domains()
            items = domains if isinstance(domains, list) else domains.get("data", [])
            result = [
                {
                    "domain": d.get("domain"),
                    "status": d.get("status"),
                    "expires_at": d.get("expires_at"),
                    "auto_renew": d.get("auto_renew"),
                }
                for d in items
            ]
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return f"Erro ao listar dominios: {e}"

    # ------------------------------------------------------------------
    # DNS
    # ------------------------------------------------------------------

    def list_dns_records(self, domain: str) -> str:
        """List all DNS records for a domain.

        Args:
            domain: The domain name, e.g. 'bravdigital.com'.
        """
        try:
            records = self._h.list_dns_records(domain)
            items = records if isinstance(records, list) else records.get("data", [])
            result = [
                {
                    "id": r.get("id"),
                    "type": r.get("type"),
                    "name": r.get("name"),
                    "content": r.get("content"),
                    "ttl": r.get("ttl"),
                }
                for r in items
            ]
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return f"Erro ao listar DNS de {domain}: {e}"

    def create_dns_record(
        self,
        domain: str,
        record_type: str,
        name: str,
        content: str,
        ttl: int = 14400,
    ) -> str:
        """Create a new DNS record for a domain.

        Args:
            domain: The domain name, e.g. 'bravdigital.com'.
            record_type: Record type — A, AAAA, CNAME, MX, TXT, etc.
            name: Record name (use '@' for root).
            content: Record value (IP address, hostname, text, etc.).
            ttl: Time to live in seconds (default 14400 = 4 hours).
        """
        try:
            record = self._h.create_dns_record(
                domain=domain,
                record_type=record_type,
                name=name,
                content=content,
                ttl=ttl,
            )
            return json.dumps(record, ensure_ascii=False)
        except Exception as e:
            return f"Erro ao criar registro DNS: {e}"

    # ------------------------------------------------------------------
    # Billing
    # ------------------------------------------------------------------

    def list_subscriptions(self) -> str:
        """List active subscriptions and hosting plans in the Hostinger account."""
        try:
            subs = self._h.list_subscriptions()
            items = subs if isinstance(subs, list) else subs.get("data", [])
            result = [
                {
                    "id": s.get("id"),
                    "name": s.get("name"),
                    "status": s.get("status"),
                    "next_billing": s.get("next_billing_at"),
                    "price": s.get("price"),
                }
                for s in items
            ]
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return f"Erro ao listar assinaturas: {e}"
