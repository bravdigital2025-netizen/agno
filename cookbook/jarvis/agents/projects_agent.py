"""Jarvis — Agente de Análise de Projetos de Obras."""

from typing import List

from pydantic import BaseModel, Field

from agno.agent import Agent
from agno.models.anthropic import Claude

from cookbook.jarvis.config import TenantConfig


class MaterialItem(BaseModel):
    """Item de material em um orçamento de obra."""

    nome: str = Field(..., description="Nome do material (ex: Cimento CP II-E-32).")
    unidade: str = Field(
        ..., description="Unidade de medida (ex: sc 50kg, m², m³, kg, un)."
    )
    quantidade: float = Field(..., description="Quantidade necessária.")
    preco_unitario: float = Field(..., description="Preço unitário estimado em reais.")
    subtotal: float = Field(
        ..., description="Subtotal calculado (quantidade * preço unitário)."
    )
    observacao: str = Field(
        "", description="Observações técnicas sobre o material ou especificação."
    )


class ProjectQuote(BaseModel):
    """Orçamento gerado a partir da análise de um projeto de obra."""

    project_name: str = Field(..., description="Nome ou identificação do projeto.")
    descricao: str = Field(..., description="Breve descrição da obra analisada.")
    area_total_m2: float = Field(
        0.0, description="Área total da obra em metros quadrados, se aplicável."
    )
    materials: List[MaterialItem] = Field(
        ..., description="Lista de materiais com quantidades e preços."
    )
    total_estimate: float = Field(
        ..., description="Valor total estimado do orçamento em reais."
    )
    prazo_estimado_dias: int = Field(
        0, description="Prazo estimado de execução em dias úteis."
    )
    observacoes_gerais: str = Field(
        "", description="Observações gerais sobre o orçamento ou a obra."
    )


def get_projects_agent(tenant: TenantConfig) -> Agent:
    """Retorna o agente de análise de projetos para o tenant informado."""
    return Agent(
        name="Agente de Projetos",
        agent_id=f"projects-agent-{tenant.tenant_id}",
        model=Claude(id="claude-sonnet-4-6"),
        description=(
            "Você é o especialista em análise de projetos de obras da "
            f"{tenant.store_name}, uma loja de materiais de construção. "
            "Sua função é analisar plantas baixas, projetos arquitetônicos e memoriais descritivos "
            "para extrair a lista de materiais necessários e gerar orçamentos precisos."
        ),
        instructions=[
            "Analise projetos arquitetônicos, plantas baixas, cortes e memoriais descritivos "
            "fornecidos como imagens ou documentos PDF.",
            "Identifique e quantifique os principais materiais de construção necessários:",
            "  - Fundação: cimento, areia, brita, aço, fôrmas, blocos de fundação.",
            "  - Estrutura: cimento, areia, brita, aço CA-50, CA-25, fôrmas de madeira.",
            "  - Alvenaria: tijolos, blocos cerâmicos ou de concreto, argamassa, cimento.",
            "  - Cobertura: telhas, ripas, caibros, vigas, cumeeira, calhas.",
            "  - Revestimento: argamassa, cerâmica, porcelanato, rejunte, tinta.",
            "  - Instalações: tubos PVC, conexões, caixas d'água, registros.",
            "Aplique os índices técnicos corretos para o cálculo de materiais:",
            "  - Cimento para fundação corrida: 8 sc/m³ de concreto.",
            "  - Tijolos cerâmicos 9x19x19: ~35 unidades/m².",
            "  - Cerâmica para piso: área + 10% de perda.",
            "  - Tinta látex: 1 galão (3,6L) para 40m² (2 demãos).",
            "Use os preços da tabela de produtos da loja se disponíveis; caso contrário, "
            "utilize preços de mercado atualizados para a região do estado informado.",
            "Apresente o orçamento detalhado com subtotais por etapa da obra.",
            "Inclua observações técnicas relevantes sobre especificações e substituições possíveis.",
            "Sempre informe a margem de erro do orçamento estimada (ex: ±10%).",
            "Responda em português brasileiro.",
        ],
        output_model=ProjectQuote,
        markdown=True,
        add_datetime_to_context=True,
    )


async def get_projects_agent_async(tenant: TenantConfig) -> Agent:
    """Retorna o agente de análise de projetos (versão assíncrona)."""
    return get_projects_agent(tenant)
