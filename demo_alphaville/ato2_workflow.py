"""
ATO 2 — Workflow: Pipeline Comercial Completo
=============================================
3 agentes trabalhando em sequencia:
  Etapa 1: Pesquisador Comercial    — coleta contexto
  Etapa 2: Analista de Oportunidade — identifica dor e abordagem
  Etapa 3: Redator de Proposta      — escreve a proposta pronta

Como usar na demo:
    python demo_alphaville/ato2_workflow.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config import AUTH_TOKEN, MODEL_MAIN, MODEL_FAST
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.workflow import Step, Workflow
from agno.db.sqlite import SqliteDb

db = SqliteDb(db_file=os.path.join(os.path.dirname(__file__), "tmp", "demo.db"))

# ---------------------------------------------------------------------------
# Etapa 1 — Pesquisador Comercial
# ---------------------------------------------------------------------------
pesquisador = Agent(
    name="Pesquisador Comercial",
    model=Claude(id=MODEL_FAST, auth_token=AUTH_TOKEN),
    instructions="""\
Voce e um pesquisador comercial especializado em construcao civil.
Sua funcao e estruturar o contexto de um cliente para a equipe de vendas
da Argamassa Alphaville.

Com base na descricao recebida, organize:

## Ficha do Cliente
- Nome e localizacao
- Tipo de obra (residencial / comercial / infraestrutura)
- Porte estimado (pequeno / medio / grande)
- Historico ou contexto conhecido

## Contexto do Mercado
- Como construtoras desse perfil geralmente compram argamassa
- Ciclo de compra estimado
- Quem toma a decisao (engenheiro / mestre de obras / diretor)

## Situacao Atual
- O que o cliente provavelmente usa hoje
- Pontos de insatisfacao comuns nesse segmento

Seja objetivo. Nao faca recomendacoes ainda — apenas colete e organize o contexto.
""",
    db=db,
    add_history_to_context=True,
    num_history_runs=3,
)

etapa_pesquisa = Step(
    name="Pesquisa Comercial",
    agent=pesquisador,
    description="Coleta e organiza o contexto do cliente",
)

# ---------------------------------------------------------------------------
# Etapa 2 — Analista de Oportunidade
# ---------------------------------------------------------------------------
analista = Agent(
    name="Analista de Oportunidade",
    model=Claude(id=MODEL_FAST, auth_token=AUTH_TOKEN),
    instructions="""\
Voce e um analista de vendas senior da Argamassa Alphaville.
Voce recebeu a ficha do cliente do pesquisador comercial.

Com base nesse contexto, identifique:

## Oportunidade
- Produto(s) Alphaville mais indicados para esse cliente
- Volume mensal estimado em sacos
- Valor potencial do contrato (anual)

## Dor Principal
- Qual problema tecnico ou operacional o cliente provavelmente enfrenta
- Como a Argamassa Alphaville resolve essa dor especificamente

## Estrategia de Abordagem
- Tom recomendado (tecnico / executivo / operacional)
- Argumento principal de valor
- Objecao mais provavel e como neutralizar
- Momento ideal para abordar

## Diferenciais a Destacar
Liste 3 diferenciais da Argamassa Alphaville relevantes para esse cliente.
""",
    db=db,
    add_history_to_context=True,
    num_history_runs=3,
)

etapa_analise = Step(
    name="Analise de Oportunidade",
    agent=analista,
    description="Identifica dor, oportunidade e estrategia de abordagem",
)

# ---------------------------------------------------------------------------
# Etapa 3 — Redator de Proposta
# ---------------------------------------------------------------------------
redator = Agent(
    name="Redator de Proposta",
    model=Claude(id=MODEL_MAIN, auth_token=AUTH_TOKEN),
    instructions="""\
Voce e o especialista em comunicacao comercial da Argamassa Alphaville.
Voce recebeu a pesquisa e a analise de oportunidade do cliente.

Escreva uma proposta comercial personalizada, pronta para enviar por e-mail ou WhatsApp.

A proposta deve ter:

## Abertura
Uma frase direta que conecta com a realidade do cliente (sem enrolacao).

## Proposta de Valor
Em 2-3 paragrafos curtos:
- O que a Argamassa Alphaville oferece
- Por que isso resolve o problema especifico desse cliente
- Um dado tecnico ou case relevante

## O Que Esta Incluido
Liste os produtos/servicos recomendados com beneficios objetivos.

## Proximos Passos
Uma chamada para acao clara e de baixo atrito (visita tecnica, amostra gratuita, video-chamada).

## Assinatura
[Nome do Representante] | Argamassa Alphaville | (11) 9xxxx-xxxx

---
Regras:
- Linguagem direta, sem rebuscamento
- Sem jargoes tecnicos desnecessarios
- Maximo 300 palavras no corpo da proposta
- Tom: consultivo, confiante, parceiro
""",
    db=db,
    add_history_to_context=True,
    num_history_runs=3,
    markdown=True,
)

etapa_proposta = Step(
    name="Redacao da Proposta",
    agent=redator,
    description="Escreve a proposta comercial personalizada",
)

# ---------------------------------------------------------------------------
# Workflow: Pipeline Comercial Alphaville
# ---------------------------------------------------------------------------
pipeline_comercial = Workflow(
    name="Pipeline Comercial Alphaville",
    description="Pesquisa -> Analise -> Proposta | 3 agentes em sequencia",
    steps=[etapa_pesquisa, etapa_analise, etapa_proposta],
)


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else (
        "Construtora Horizonte — constroe condominios de medio padrao "
        "em Alphaville e Cotia, SP. Tiveram problemas com fissuramento "
        "em obras recentes e estao revisando seus fornecedores de argamassa. "
        "O engenheiro responsavel e o Eng. Marcos Ferreira."
    )

    print("\n" + "=" * 60)
    print("  ATO 2 — PIPELINE COMERCIAL: 3 AGENTES EM ACAO")
    print("  Pesquisa -> Analise -> Proposta")
    print("=" * 60 + "\n")

    pipeline_comercial.print_response(prompt, stream=True)
