"""
Jarvis — Configuracao de schedules automaticos

Cria os schedules recorrentes do Jarvis via API REST do AgentOS.
Execute uma vez apos o app estar rodando para registrar os jobs.

Schedules criados:
  - Alerta de estoque critico: diario as 07:00
  - Relatorio executivo diario: diario as 08:00
  - Resumo semanal de vendas: toda segunda-feira as 08:30
  - Varredura de campanhas pendentes: diario as 09:00

Uso:
    # Com o app rodando em localhost:7777:
    .venvs/demo/bin/python cookbook/jarvis/scheduler_setup.py

    # Apontando para outra URL:
    JARVIS_URL=https://meu-jarvis.com .venvs/demo/bin/python cookbook/jarvis/scheduler_setup.py
"""

import os
import sys
from typing import Any, Dict, List

import httpx

BASE_URL = os.getenv("JARVIS_URL", "http://localhost:7777")
TENANT_ID = os.getenv("JARVIS_TENANT_ID", "demo")

# AgentOS team endpoint pattern: /v1/teams/{team_id}/runs
JARVIS_TEAM_ID = f"jarvis-{TENANT_ID}"
TEAM_ENDPOINT = f"/v1/teams/{JARVIS_TEAM_ID}/runs"

# ---------------------------------------------------------------------------
# Schedule definitions
# ---------------------------------------------------------------------------

SCHEDULES: List[Dict[str, Any]] = [
    {
        "name": "jarvis-alerta-estoque-critico",
        "cron_expr": "0 7 * * *",  # diario as 07:00
        "endpoint": TEAM_ENDPOINT,
        "payload": {
            "message": (
                "Verifique o estoque de todos os produtos e liste aqueles "
                "com saldo igual ou abaixo do estoque minimo. "
                "Inclua sugestao de quantidade para reposicao e fornecedor responsavel. "
                "Priorize cimento, areia, brita, blocos e aco."
            )
        },
    },
    {
        "name": "jarvis-relatorio-diario",
        "cron_expr": "0 8 * * *",  # diario as 08:00
        "endpoint": TEAM_ENDPOINT,
        "payload": {
            "message": (
                "Gere o relatorio executivo do dia anterior. "
                "Inclua: total de vendas, numero de pedidos, ticket medio, "
                "produtos mais vendidos e comparacao com a media dos ultimos 7 dias. "
                "Destaque oportunidades e alertas relevantes para o dono da loja."
            )
        },
    },
    {
        "name": "jarvis-resumo-semanal",
        "cron_expr": "30 8 * * 1",  # toda segunda as 08:30
        "endpoint": TEAM_ENDPOINT,
        "payload": {
            "message": (
                "Gere o resumo semanal de desempenho da loja. "
                "Analise a semana anterior: evolucao de vendas por dia, "
                "categorias de produto com melhor e pior desempenho, "
                "clientes mais ativos, campanhas realizadas e seus resultados. "
                "Sugira acoes para a semana atual com base nos dados."
            )
        },
    },
    {
        "name": "jarvis-campanhas-pendentes",
        "cron_expr": "0 9 * * *",  # diario as 09:00
        "endpoint": TEAM_ENDPOINT,
        "payload": {
            "message": (
                "Verifique se ha campanhas de marketing agendadas para hoje. "
                "Para cada campanha pendente, confirme se os dados estao corretos "
                "e sugira ajustes na mensagem se necessario antes do disparo."
            )
        },
    },
]


# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------


def setup_schedules(base_url: str = BASE_URL) -> None:
    """Register all Jarvis schedules via the AgentOS REST API."""
    schedules_url = f"{base_url}/schedules"

    print(f"Connecting to Jarvis at {base_url}")
    print(f"Registering {len(SCHEDULES)} schedules...\n")

    with httpx.Client(timeout=30) as client:
        # List existing schedules to avoid duplicates
        try:
            existing = client.get(schedules_url).json()
            existing_names = {
                s.get("name") for s in existing if isinstance(existing, list)
            }
        except Exception:
            existing_names = set()

        for schedule in SCHEDULES:
            name = schedule["name"]
            if name in existing_names:
                print(f"  SKIP  {name} (already exists)")
                continue

            try:
                resp = client.post(schedules_url, json=schedule)
                resp.raise_for_status()
                data = resp.json()
                print(
                    f"  OK    {name} — id={data.get('id', '?')} cron={schedule['cron_expr']}"
                )
            except httpx.HTTPStatusError as exc:
                print(
                    f"  FAIL  {name} — HTTP {exc.response.status_code}: {exc.response.text}"
                )
            except Exception as exc:
                print(f"  FAIL  {name} — {exc}")

    print("\nSchedule setup complete.")
    print(f"View schedules: GET {schedules_url}")


async def setup_schedules_async(base_url: str = BASE_URL) -> None:
    """Versao assincrona de setup_schedules."""
    schedules_url = f"{base_url}/schedules"

    async with httpx.AsyncClient(timeout=30) as client:
        try:
            existing_resp = await client.get(schedules_url)
            existing = existing_resp.json()
            existing_names = {
                s.get("name") for s in existing if isinstance(existing, list)
            }
        except Exception:
            existing_names = set()

        for schedule in SCHEDULES:
            name = schedule["name"]
            if name in existing_names:
                continue
            try:
                resp = await client.post(schedules_url, json=schedule)
                resp.raise_for_status()
            except Exception:
                pass


if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else BASE_URL
    setup_schedules(base_url=url)
