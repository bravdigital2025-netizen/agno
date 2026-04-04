"""Jarvis — Agente de Marketing e Campanhas."""

from typing import Any, List

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.anthropic import Claude
from agno.tools.whatsapp import WhatsAppTools

from cookbook.jarvis.config import TenantConfig


def get_marketing_agent(tenant: TenantConfig) -> Agent:
    """Retorna o agente de marketing para o tenant informado."""
    db = PostgresDb(
        id=f"marketing-agent-db-{tenant.tenant_id}",
        db_url=tenant.db_url,
    )
    tools: List[Any] = []

    if tenant.whatsapp_token and tenant.whatsapp_phone_id:
        whatsapp_tools = WhatsAppTools(
            access_token=tenant.whatsapp_token,
            phone_number_id=tenant.whatsapp_phone_id,
            enable_send_text_message=True,
            enable_send_template_message=True,
            enable_send_reply_buttons=True,
            enable_send_list_message=True,
        )
        tools.append(whatsapp_tools)

    return Agent(
        name="Agente de Marketing",
        agent_id=f"marketing-agent-{tenant.tenant_id}",
        model=Claude(id="claude-sonnet-4-6"),
        db=db,
        tools=tools,
        update_memory_on_run=True,
        add_history_to_context=True,
        num_history_runs=5,
        enable_session_summaries=True,
        description=(
            "Você é o agente de marketing da "
            f"{tenant.store_name}, uma loja de materiais de construção. "
            "Sua função é criar e gerenciar campanhas promocionais via WhatsApp, "
            "segmentar a base de clientes e aumentar as vendas por meio de comunicação direcionada."
        ),
        instructions=[
            "Segmente os clientes com base no histórico de compras: construtoras, reformadores, "
            "pedreiros autônomos e clientes pessoa física.",
            "Crie mensagens promocionais personalizadas de acordo com o perfil de cada segmento.",
            "Use linguagem próxima e profissional, adequada ao público da construção civil no Brasil.",
            "Proponha campanhas sazonais relevantes: Dia do Trabalhador, São João, fim de ano, etc.",
            "Para clientes que compraram cimento nos últimos 30 dias, sugira produtos complementares "
            "como areia, brita, blocos e ferramentas.",
            "Para clientes que não compram há mais de 60 dias, crie mensagens de reativação com ofertas especiais.",
            "Programe envios em horários adequados: dias úteis entre 9h e 18h.",
            "Respeite as preferências de contato e não envie mensagens repetitivas para o mesmo cliente.",
            "Mensure a efetividade sugerindo métricas: taxa de abertura, retorno em vendas, conversão.",
            "Nunca invente dados de clientes; utilize apenas informações fornecidas ou disponíveis.",
            "Sempre confirme antes de enviar mensagens em massa.",
        ],
        markdown=True,
        add_datetime_to_context=True,
    )


async def get_marketing_agent_async(tenant: TenantConfig) -> Agent:
    """Retorna o agente de marketing (versão assíncrona)."""
    return get_marketing_agent(tenant)
