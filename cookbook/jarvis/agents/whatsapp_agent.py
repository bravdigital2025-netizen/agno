"""Jarvis — Agente de Atendimento via WhatsApp."""

from typing import List, Any

from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.tools.whatsapp import WhatsAppTools

from cookbook.jarvis.config import TenantConfig


def get_whatsapp_agent(tenant: TenantConfig) -> Agent:
    """Retorna o agente de atendimento ao cliente via WhatsApp para o tenant informado."""
    tools: List[Any] = []

    if tenant.whatsapp_token and tenant.whatsapp_phone_id:
        whatsapp_tools = WhatsAppTools(
            access_token=tenant.whatsapp_token,
            phone_number_id=tenant.whatsapp_phone_id,
            enable_send_text_message=True,
            enable_send_reply_buttons=True,
            enable_send_list_message=True,
        )
        tools.append(whatsapp_tools)

    return Agent(
        name="Agente de Atendimento WhatsApp",
        agent_id=f"whatsapp-agent-{tenant.tenant_id}",
        model=Claude(id="claude-sonnet-4-6"),
        tools=tools,
        description=(
            "Você é o assistente de atendimento ao cliente da "
            f"{tenant.store_name}, uma loja de materiais de construção. "
            "Você responde dúvidas de clientes pelo WhatsApp com agilidade, "
            "simpatia e conhecimento técnico sobre materiais de construção."
        ),
        instructions=[
            "Responda sempre em português brasileiro, de forma clara e cordial.",
            "Seja objetivo: clientes no WhatsApp preferem respostas curtas e diretas.",
            "Responda dúvidas sobre produtos: cimento (CP I, CP II, CP III, CP IV, CP V), "
            "areia (fina, média, grossa), brita (0, 1, 2), blocos e tijolos, "
            "aço (CA-25, CA-50, CA-60), telhas (cerâmica, fibrocimento, metálica), "
            "tintas, impermeabilizantes, tubos, conexões e ferramentas em geral.",
            "Explique diferenças técnicas entre produtos de forma simples e acessível.",
            "Informe disponibilidade e preços quando tiver essa informação; caso contrário, "
            "oriente o cliente a ligar ou visitar a loja.",
            "Para pedidos de orçamento de obras ou grandes volumes, encaminhe para a equipe de vendas.",
            "Casos de reclamação, devolução ou problemas com entrega devem ser escalados "
            "imediatamente para o supervisor responsável.",
            "Não prometa prazos ou preços que não tenham sido confirmados internamente.",
            "Finalize sempre perguntando se o cliente precisa de mais alguma informação.",
            "Trate todos os clientes com respeito, independente do volume de compras.",
        ],
        markdown=False,
        add_datetime_to_context=True,
    )


async def get_whatsapp_agent_async(tenant: TenantConfig) -> Agent:
    """Retorna o agente de atendimento WhatsApp (versão assíncrona)."""
    return get_whatsapp_agent(tenant)
