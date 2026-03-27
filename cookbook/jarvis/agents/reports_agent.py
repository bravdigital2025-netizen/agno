"""Jarvis — Agente de Relatórios Executivos."""

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.models.anthropic import Claude
from agno.tools.sql import SQLTools

from cookbook.jarvis.config import TenantConfig


def get_reports_agent(tenant: TenantConfig) -> Agent:
    """Retorna o agente de relatórios executivos para o tenant informado."""
    db = PostgresDb(
        id=f"reports-agent-db-{tenant.tenant_id}",
        db_url=tenant.db_url,
    )
    return Agent(
        name="Agente de Relatórios",
        agent_id=f"reports-agent-{tenant.tenant_id}",
        model=Claude(id="claude-sonnet-4-6"),
        db=db,
        tools=[SQLTools(db_url=tenant.db_url)],
        update_memory_on_run=True,
        add_history_to_context=True,
        num_history_runs=5,
        enable_session_summaries=True,
        description=(
            "Você é o analista de dados e relatórios da "
            f"{tenant.store_name}, uma loja de materiais de construção. "
            "Sua função é gerar relatórios executivos que ajudem o dono da loja "
            "a tomar decisões estratégicas com base em dados reais de vendas, estoque e clientes."
        ),
        instructions=[
            "Acesse o banco de dados para coletar os dados necessários para cada relatório.",
            "Relatório diário de vendas:",
            "  - Total de vendas do dia em reais.",
            "  - Número de pedidos e ticket médio.",
            "  - Top 5 produtos mais vendidos.",
            "  - Comparação com o mesmo dia da semana anterior.",
            "Relatório semanal de tendências:",
            "  - Evolução de vendas por dia da semana.",
            "  - Produtos com crescimento e queda de demanda.",
            "  - Desempenho por categoria (cimento, aço, cerâmica, tintas, etc.).",
            "  - Clientes novos vs. recorrentes.",
            "Relatório mensal de gestão:",
            "  - Faturamento total e margem de contribuição.",
            "  - Comparação com o mês anterior e mesmo mês do ano anterior.",
            "  - Ranking de clientes por volume de compras.",
            "  - Produtos com maior e menor margem.",
            "  - Análise de inadimplência e contas a receber.",
            "Identificação de oportunidades:",
            "  - Clientes que não compram há mais de 30 dias.",
            "  - Produtos com alta demanda mas estoque baixo.",
            "  - Horários de pico de vendas para melhor alocação de equipe.",
            "Apresente os relatórios com tabelas, listas e destaques em markdown.",
            "Adicione interpretação gerencial: o que os números significam para o negócio.",
            "Aponte no mínimo 3 ações recomendadas ao final de cada relatório.",
            "Nunca invente dados; se não encontrar informação no banco, informe claramente.",
        ],
        markdown=True,
        add_datetime_to_context=True,
    )


async def get_reports_agent_async(tenant: TenantConfig) -> Agent:
    """Retorna o agente de relatórios executivos (versão assíncrona)."""
    return get_reports_agent(tenant)
