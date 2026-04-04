"""Jarvis — Orquestrador principal (Team)."""

from agno.models.anthropic import Claude
from agno.team import Team

from cookbook.jarvis.agents.inventory_agent import get_inventory_agent
from cookbook.jarvis.agents.marketing_agent import get_marketing_agent
from cookbook.jarvis.agents.projects_agent import get_projects_agent
from cookbook.jarvis.agents.reports_agent import get_reports_agent
from cookbook.jarvis.agents.whatsapp_agent import get_whatsapp_agent
from cookbook.jarvis.config import TenantConfig


def get_jarvis_team(tenant: TenantConfig) -> Team:
    """Retorna o time Jarvis completo para o tenant informado."""
    inventory_agent = get_inventory_agent(tenant)
    marketing_agent = get_marketing_agent(tenant)
    whatsapp_agent = get_whatsapp_agent(tenant)
    projects_agent = get_projects_agent(tenant)
    reports_agent = get_reports_agent(tenant)

    return Team(
        name="Jarvis",
        team_id=f"jarvis-{tenant.tenant_id}",
        model=Claude(id="claude-sonnet-4-6"),
        members=[
            inventory_agent,
            marketing_agent,
            whatsapp_agent,
            projects_agent,
            reports_agent,
        ],
        description=(
            f"Jarvis - Sistema Operacional de Inteligência para {tenant.store_name}. "
            "Coordeno uma equipe de agentes especializados para apoiar todas as áreas "
            "da sua loja de materiais de construção: estoque, marketing, atendimento, "
            "análise de projetos e relatórios gerenciais."
        ),
        instructions=[
            "Você é o coordenador do Jarvis, o sistema de inteligência da loja.",
            "Analise cada solicitação e encaminhe para o agente especialista mais adequado:",
            "  - Dúvidas sobre estoque, rupturas e reposição -> Agente de Estoque.",
            "  - Campanhas, promoções e comunicação com clientes -> Agente de Marketing.",
            "  - Atendimento de clientes via WhatsApp -> Agente de Atendimento WhatsApp.",
            "  - Análise de plantas, projetos e orçamentos de obra -> Agente de Projetos.",
            "  - Relatórios de vendas, desempenho e gestão -> Agente de Relatórios.",
            "Quando uma solicitação envolver múltiplas áreas, coordene os agentes necessários "
            "e sintetize as respostas em uma única resposta coerente.",
            "Sempre responda em português brasileiro.",
            "Seja objetivo e prático: o dono da loja precisa de respostas acionáveis.",
            "Ao sintetizar respostas, destaque os pontos mais importantes e ações recomendadas.",
            "Se não souber ou não tiver dados suficientes, informe claramente e sugira como obter a informação.",
        ],
        markdown=True,
        add_datetime_to_context=True,
        show_members_responses=True,
    )


async def get_jarvis_team_async(tenant: TenantConfig) -> Team:
    """Retorna o time Jarvis completo (versão assíncrona)."""
    return get_jarvis_team(tenant)
