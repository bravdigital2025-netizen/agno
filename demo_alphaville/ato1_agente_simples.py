"""
ATO 1 — Agente Simples: Perfil de Prospect
===========================================
Em segundos, a IA transforma o nome de uma construtora
em um perfil comercial pronto para abordar.

Como usar na demo:
    python demo_alphaville/ato1_agente_simples.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config import AUTH_TOKEN, MODEL_FAST
from agno.agent import Agent
from agno.models.anthropic import Claude

# ---------------------------------------------------------------------------
# Agente: Analista de Prospect
# ---------------------------------------------------------------------------
analista_prospect = Agent(
    name="Analista de Prospect",
    model=Claude(id=MODEL_FAST, auth_token=AUTH_TOKEN),
    markdown=True,
    instructions="""\
Voce e um especialista em vendas B2B para a industria da construcao civil.
Sua funcao e analisar prospects para a Argamassa Alphaville,
fabricante premium de argamassas e revestimentos.

Ao receber o nome ou descricao de um cliente, retorne:

## Perfil do Prospect

**Segmento:** (ex: construtora de residenciais populares, incorporadora de alto padrao, empreiteira de obras publicas)
**Porte estimado:** (Pequeno / Medio / Grande)
**Consumo mensal estimado de argamassa:** (ex: 50-200 sacos/mes)
**Produto mais indicado:** (ex: Argamassa AC-III Alphaville Premium)

## Oportunidade Comercial

**Dor principal:** (problema que eles provavelmente enfrentam)
**Gancho de abertura:** (frase de entrada para o representante)
**Melhor canal de contato:** (visita tecnica / ligacao / WhatsApp)
**Urgencia:** (Alta / Media / Baixa) com justificativa rapida

## Proximos Passos

1. (acao imediata do representante)
2. (acao de follow-up)
3. (material para enviar)
""",
)


if __name__ == "__main__":
    prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else (
        "Construtora Horizonte — constroe condominios de medio padrao "
        "em Alphaville e Cotia, SP. Tiveram problemas com fissuramento "
        "em obras recentes e estao revisando fornecedores de argamassa."
    )

    print("\n" + "=" * 60)
    print("  ATO 1 — ANALISE DE PROSPECT AO VIVO")
    print("=" * 60 + "\n")

    analista_prospect.print_response(prompt, stream=True)
