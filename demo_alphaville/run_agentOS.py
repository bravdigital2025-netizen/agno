"""
AgentOS — Interface Web para todos os agentes da demo
======================================================
Inicia um servidor local com interface grafica em os.agno.com

Como usar:
    python demo_alphaville/run_agentOS.py

Em seguida:
    1. Acesse https://os.agno.com
    2. Clique em "Add new OS"
    3. Selecione "Local"
    4. Coloque: http://localhost:7777
    5. Nome: "Demo Argamassa Alphaville"
    6. Clique Connect
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config import AUTH_TOKEN, MODEL_FAST, MODEL_MAIN
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.team.team import Team
from agno.workflow import Step, Workflow
from agno.db.sqlite import SqliteDb
from agno.os import AgentOS

db = SqliteDb(db_file=os.path.join(os.path.dirname(__file__), "tmp", "agentOS.db"))

# ---------------------------------------------------------------------------
# Agente 1: Analista de Prospect
# ---------------------------------------------------------------------------
agente_prospect = Agent(
    name="Analista de Prospect",
    model=Claude(id=MODEL_FAST, auth_token=AUTH_TOKEN),
    markdown=True,
    db=db,
    add_history_to_context=True,
    num_history_runs=5,
    description="Analisa construtoras e gera perfil comercial em segundos",
    instructions="""\
Voce e um especialista em vendas B2B para a industria da construcao civil,
trabalhando para a Argamassa Alphaville.

Ao receber descricao de um cliente, retorne um perfil comercial completo:
- Segmento e porte
- Produto indicado
- Dor principal
- Gancho de abertura
- Proximos passos para o representante

Seja objetivo e pratico. O representante precisa sair da conversa com um plano.
""",
)

# ---------------------------------------------------------------------------
# Agente 2: Redator Comercial
# ---------------------------------------------------------------------------
agente_proposta = Agent(
    name="Redator de Proposta",
    model=Claude(id=MODEL_MAIN, auth_token=AUTH_TOKEN),
    markdown=True,
    db=db,
    add_history_to_context=True,
    num_history_runs=5,
    description="Escreve propostas, e-mails e mensagens comerciais personalizadas",
    instructions="""\
Voce e o redator comercial da Argamassa Alphaville.
Especialista em comunicacao persuasiva para construcao civil.

Crie qualquer material de comunicacao comercial:
- Propostas por e-mail
- Mensagens de WhatsApp
- Scripts de ligacao
- Cadencias de follow-up
- Respostas a objecoes

Sempre: linguagem direta, foco no valor, pronto para usar.
""",
)

# ---------------------------------------------------------------------------
# Agente 3: Treinador de Vendas
# ---------------------------------------------------------------------------
agente_treinamento = Agent(
    name="Treinador de Vendas",
    model=Claude(id=MODEL_FAST, auth_token=AUTH_TOKEN),
    markdown=True,
    db=db,
    add_history_to_context=True,
    num_history_runs=5,
    description="Treina representantes com simulacoes e respostas a objecoes",
    instructions="""\
Voce e o treinador de vendas da Argamassa Alphaville.
Seu papel: preparar representantes comerciais para situacoes reais.

Voce pode:
- Simular objecoes de clientes e ensinar como responder
- Criar scripts para diferentes perfis de comprador
- Dar feedback sobre abordagens comerciais
- Sugerir melhorias em mensagens e propostas

Tom: didatico, pratico, direto. Nada de teoria — so o que funciona na rua.
""",
)

# ---------------------------------------------------------------------------
# Time: Comite Estrategico de Vendas
# ---------------------------------------------------------------------------
agente_volume = Agent(
    name="Foco em Volume",
    role="Estrategia para maximizar volume e velocidade de fechamento",
    model=Claude(id=MODEL_FAST, auth_token=AUTH_TOKEN),
    db=db,
    add_history_to_context=True,
    num_history_runs=3,
    instructions="""\
Voce defende estrategias de alto volume e fechamento rapido.
Argumente a favor de: descontos por volume, senso de urgencia,
proposta agressiva de preco, foco no curto prazo.
Maximo 120 palavras. Seja direto e persuasivo.
""",
)

agente_fidelizacao = Agent(
    name="Foco em Fidelizacao",
    role="Estrategia para construir relacoes duradouras e alta margem",
    model=Claude(id=MODEL_FAST, auth_token=AUTH_TOKEN),
    db=db,
    add_history_to_context=True,
    num_history_runs=3,
    instructions="""\
Voce defende estrategias de fidelizacao e valor percebido.
Argumente a favor de: suporte tecnico diferenciado, amostras gratuitas,
construcao de confianca, foco na margem e no longo prazo.
Maximo 120 palavras. Seja direto e persuasivo.
""",
)

comite_estrategico = Team(
    name="Comite Estrategico de Vendas",
    model=Claude(id=MODEL_MAIN, auth_token=AUTH_TOKEN),
    members=[agente_volume, agente_fidelizacao],
    description="Debate estrategias e decide a melhor abordagem para cada cliente",
    instructions="""\
Voce lidera o Comite Estrategico de Vendas da Argamassa Alphaville.
Peca para os dois especialistas apresentarem suas perspectivas,
depois decida a melhor estrategia para o caso especifico.

Formato da decisao:
- Estrategia escolhida e justificativa (2-3 linhas)
- Plano de acao em 3 passos
- Mensagem inicial para o cliente (pronta para enviar)
""",
    db=db,
    show_members_responses=True,
    add_history_to_context=True,
    num_history_runs=3,
    markdown=True,
)

# ---------------------------------------------------------------------------
# Workflow: Pipeline Comercial Completo
# ---------------------------------------------------------------------------
pesquisador_wf = Agent(
    name="Pesquisador",
    model=Claude(id=MODEL_FAST, auth_token=AUTH_TOKEN),
    db=db,
    instructions="Pesquise e organize o contexto do cliente: tipo de obra, porte, decisor, situacao atual.",
)

analista_wf = Agent(
    name="Analista",
    model=Claude(id=MODEL_FAST, auth_token=AUTH_TOKEN),
    db=db,
    instructions="Com base no contexto do pesquisador, identifique: oportunidade, dor principal, estrategia de abordagem e produto indicado.",
)

redator_wf = Agent(
    name="Redator",
    model=Claude(id=MODEL_MAIN, auth_token=AUTH_TOKEN),
    db=db,
    markdown=True,
    instructions="Com base na pesquisa e analise, escreva uma proposta comercial personalizada, pronta para enviar. Linguagem direta, foco no valor, max 300 palavras.",
)

pipeline_wf = Workflow(
    name="Pipeline Comercial",
    description="Pesquisa -> Analise -> Proposta: gera proposta completa a partir do nome do cliente",
    steps=[
        Step(name="Pesquisa", agent=pesquisador_wf, description="Coleta contexto do cliente"),
        Step(name="Analise", agent=analista_wf, description="Identifica oportunidade e estrategia"),
        Step(name="Proposta", agent=redator_wf, description="Escreve proposta personalizada"),
    ],
)

# ---------------------------------------------------------------------------
# AgentOS
# ---------------------------------------------------------------------------
agent_os = AgentOS(
    id="Demo Argamassa Alphaville",
    agents=[agente_prospect, agente_proposta, agente_treinamento],
    teams=[comite_estrategico],
    workflows=[pipeline_wf],
    tracing=True,
)

app = agent_os.get_app()

if __name__ == "__main__":
    agent_os.serve(app="run_agentOS:app", reload=False, port=7777)
