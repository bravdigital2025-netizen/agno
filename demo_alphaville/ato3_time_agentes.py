"""
ATO 3 — Time de Agentes: Debate Estrategico
===========================================
Dois agentes com perspectivas opostas debatem a melhor
estrategia comercial. Um lider sintetiza e decide.

Agentes:
  - Agente Agressivo: quer fechar rapido, prioriza volume
  - Agente Consultivo: quer construir relacao, prioriza fidelizacao
  - Lider Comercial: ouve os dois e decide a estrategia ideal

Como usar na demo:
    python demo_alphaville/ato3_time_agentes.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config import AUTH_TOKEN, MODEL_FAST, MODEL_MAIN
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.team.team import Team
from agno.db.sqlite import SqliteDb

db = SqliteDb(db_file=os.path.join(os.path.dirname(__file__), "tmp", "demo.db"))

# ---------------------------------------------------------------------------
# Agente: Estrategia Agressiva
# ---------------------------------------------------------------------------
agente_agressivo = Agent(
    name="Estrategista Agressivo",
    role="Defende abordagem de fechamento rapido e alto volume",
    model=Claude(id=MODEL_FAST, auth_token=AUTH_TOKEN),
    instructions="""\
Voce e um estrategista de vendas agressivo da Argamassa Alphaville.
Voce acredita que velocidade e volume sao os fatores que mais importam.

Sua posicao:
- Foco em fechar logo, antes da concorrencia chegar
- Propor desconto de volume para garantir o contrato agora
- Pressionar sutilmente pelo senso de urgencia
- Priorizar o numero de sacos/mes, nao a relacao de longo prazo

Defenda sua estrategia com argumentos concretos.
Seja direto e objetivo. Maximo 150 palavras.
""",
    db=db,
    add_history_to_context=True,
    num_history_runs=3,
)

# ---------------------------------------------------------------------------
# Agente: Estrategia Consultiva
# ---------------------------------------------------------------------------
agente_consultivo = Agent(
    name="Estrategista Consultivo",
    role="Defende abordagem de construcao de confianca e fidelizacao",
    model=Claude(id=MODEL_FAST, auth_token=AUTH_TOKEN),
    instructions="""\
Voce e um estrategista de vendas consultivo da Argamassa Alphaville.
Voce acredita que confianca e suporte tecnico sao os maiores diferenciais.

Sua posicao:
- Comece com uma visita tecnica sem compromisso
- Oferca uma amostra gratuita para o cliente testar o produto
- Construa relacao com o engenheiro e o mestre de obras
- Preço nao e o principal argumento — qualidade e suporte sao
- Cliente fidelizado compra por anos, nao apenas uma vez

Defenda sua estrategia com argumentos concretos.
Seja direto e objetivo. Maximo 150 palavras.
""",
    db=db,
    add_history_to_context=True,
    num_history_runs=3,
)

# ---------------------------------------------------------------------------
# Lider: Diretor Comercial
# ---------------------------------------------------------------------------
time_comercial = Team(
    name="Time Comercial Alphaville",
    model=Claude(id=MODEL_MAIN, auth_token=AUTH_TOKEN),
    members=[agente_agressivo, agente_consultivo],
    instructions="""\
Voce e o Diretor Comercial da Argamassa Alphaville.
Voce tem um Estrategista Agressivo e um Estrategista Consultivo na sua equipe.

Processo:
1. Peca para os dois apresentarem suas estrategias
2. Avalie os argumentos de cada um
3. Decida a melhor abordagem para esse cliente especifico

Formato da sua sintese final:

## Estrategia Decidida: [nome]

**Por que essa abordagem:** (1-2 linhas)

**O que aproveitar da estrategia oposta:** (1 elemento)

**Plano de acao em 3 passos:**
1. ...
2. ...
3. ...

**Mensagem inicial para o cliente:** (pronta para enviar por WhatsApp, max 3 linhas)

Seja decisivo. Nao fique em cima do muro.
""",
    db=db,
    show_members_responses=True,
    add_history_to_context=True,
    num_history_runs=3,
    markdown=True,
)


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else (
        "Qual a melhor estrategia para abordar a Construtora Horizonte? "
        "Eles tiveram problemas com fissuramento e estao revisando fornecedores. "
        "O decisor e o Eng. Marcos Ferreira, que e tecnicamente exigente."
    )

    print("\n" + "=" * 60)
    print("  ATO 3 — TIME DE AGENTES DEBATENDO AO VIVO")
    print("  Agressivo vs Consultivo -> Decisao do Diretor")
    print("=" * 60 + "\n")

    time_comercial.print_response(prompt, stream=True)
