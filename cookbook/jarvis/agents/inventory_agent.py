"""Jarvis — Agente de Controle de Estoque."""

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.sql import SQLTools

from cookbook.jarvis.config import TenantConfig


def get_inventory_agent(tenant: TenantConfig) -> Agent:
    """Retorna o agente de controle de estoque para o tenant informado."""
    return Agent(
        name="Agente de Estoque",
        agent_id=f"inventory-agent-{tenant.tenant_id}",
        model=Claude(id="claude-sonnet-4-6"),
        tools=[
            SQLTools(db_url=tenant.db_url),
        ],
        description=(
            "Você é o agente de controle de estoque da "
            f"{tenant.store_name}, uma loja de materiais de construção. "
            "Sua função é monitorar os níveis de estoque, identificar produtos com "
            "saldo crítico e apoiar as decisões de reposição de mercadorias."
        ),
        instructions=[
            "Consulte o banco de dados para verificar os níveis atuais de estoque.",
            "Identifique produtos cujo saldo atual está abaixo do estoque mínimo configurado.",
            "Calcule a cobertura de dias de estoque com base no histórico de vendas recentes.",
            "Destaque produtos com alta rotatividade (giro rápido) que podem gerar ruptura em breve.",
            "Identifique também produtos com baixo giro (estoque parado) que podem representar capital imobilizado.",
            "Sugira quantidades para pedido de reposição levando em conta o prazo de entrega dos fornecedores.",
            "Liste os principais fornecedores associados a cada produto com saldo crítico.",
            "Apresente os resultados de forma clara, em português, com tabelas quando possível.",
            "Priorize alertas para: cimento, areia, brita, blocos, tijolos, aço, telhas e cerâmica.",
            "Nunca invente dados; se não encontrar informação no banco, informe claramente.",
        ],
        markdown=True,
        add_datetime_to_context=True,
    )


async def get_inventory_agent_async(tenant: TenantConfig) -> Agent:
    """Retorna o agente de controle de estoque (versão assíncrona)."""
    return get_inventory_agent(tenant)
