"""
EXTRAS — Comandos Adicionais para a Demo
=========================================
Cada funcao abaixo e um comando pronto para usar ao vivo.

Comandos disponíveis:
    python demo_alphaville/extras.py cadencia
    python demo_alphaville/extras.py copy
    python demo_alphaville/extras.py objecao
    python demo_alphaville/extras.py memoria
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from config import AUTH_TOKEN, MODEL_FAST, MODEL_MAIN
from agno.agent import Agent
from agno.models.anthropic import Claude
from agno.db.sqlite import SqliteDb
from agno.memory import MemoryManager

db = SqliteDb(db_file=os.path.join(os.path.dirname(__file__), "tmp", "demo.db"))

# ---------------------------------------------------------------------------
# Agente unico reutilizavel para os extras
# ---------------------------------------------------------------------------
agente_comercial = Agent(
    name="Assistente Comercial Alphaville",
    model=Claude(id=MODEL_MAIN, auth_token=AUTH_TOKEN),
    markdown=True,
    instructions="""\
Voce e o assistente comercial senior da Argamassa Alphaville.
Especialista em vendas B2B para construcao civil.
Resposta sempre pratica, direta, pronta para usar pelo representante.
Sem teorias. Sem enrolacao. Conteudo executavel.
""",
)

# ---------------------------------------------------------------------------
# Agente com MEMORIA — lembra do cliente entre conversas
# ---------------------------------------------------------------------------
memory_manager = MemoryManager(
    model=Claude(id=MODEL_FAST, auth_token=AUTH_TOKEN),
    db=db,
    additional_instructions="""
    Capture: nome do cliente, tipo de obra, problema relatado,
    quem e o decisor, produto de interesse, historico de contato.
    """,
)

agente_com_memoria = Agent(
    name="Assistente com Memoria",
    model=Claude(id=MODEL_FAST, auth_token=AUTH_TOKEN),
    markdown=True,
    db=db,
    memory_manager=memory_manager,
    enable_agentic_memory=True,
    add_history_to_context=True,
    num_history_runs=5,
    instructions="""\
Voce e o assistente comercial da Argamassa Alphaville com memoria persistente.
Voce lembra de cada cliente, cada conversa anterior, cada detalhe compartilhado.
Use esse contexto para personalizar cada resposta.
""",
)


# ---------------------------------------------------------------------------
# COMANDO 1: Cadencia de Follow-up
# ---------------------------------------------------------------------------
def cadencia():
    prompt = """\
Crie uma cadencia de 5 touchpoints para o representante
dar seguimento apos o primeiro contato com a Construtora Horizonte.

Para cada touchpoint:
- Dia: (quando executar)
- Canal: (ligacao / WhatsApp / e-mail / visita)
- Objetivo: (o que quero conseguir nesse contato)
- Mensagem pronta: (texto ja escrito, pronto para enviar)
- Duração: (quanto tempo dedicar)
"""
    print("\n" + "=" * 60)
    print("  CADENCIA DE FOLLOW-UP — 5 TOUCHPOINTS")
    print("=" * 60 + "\n")
    agente_comercial.print_response(prompt, stream=True)


# ---------------------------------------------------------------------------
# COMANDO 2: Copy para abordagem ao mestre de obras
# ---------------------------------------------------------------------------
def copy_abertura():
    prompt = """\
Escreva 3 variacoes de mensagem de abertura para um representante
da Argamassa Alphaville entrar em contato com o mestre de obras
Joao Carlos, da Construtora Horizonte, que teve problemas de fissuramento.

Para cada variacao:
- Canal: (qual canal usar)
- Tom: (ex: tecnico, informal, consultivo)
- Mensagem: (pronta para enviar, max 4 linhas)
- Por que funciona: (1 linha de justificativa)
"""
    print("\n" + "=" * 60)
    print("  3 COPYS DE ABERTURA — PRONTAS PARA ENVIAR")
    print("=" * 60 + "\n")
    agente_comercial.print_response(prompt, stream=True)


# ---------------------------------------------------------------------------
# COMANDO 3: Tratamento de Objecao
# ---------------------------------------------------------------------------
def objecao():
    prompt = """\
O Eng. Marcos da Construtora Horizonte disse:
"O produto de voces e mais caro que o do concorrente. Nao consigo justificar."

Crie 3 respostas para o representante usar nessa situacao.
Para cada resposta:
- Abordagem: (ex: custo total de obra / qualidade / suporte tecnico)
- Resposta pronta: (texto natural, max 5 linhas, para falar ou mandar por WhatsApp)
- Quando usar: (em qual contexto essa resposta funciona melhor)
"""
    print("\n" + "=" * 60)
    print("  TRATAMENTO DE OBJECAO DE PRECO — 3 RESPOSTAS")
    print("=" * 60 + "\n")
    agente_comercial.print_response(prompt, stream=True)


# ---------------------------------------------------------------------------
# COMANDO 4: Demonstracao de Memoria
# ---------------------------------------------------------------------------
def demo_memoria():
    user_id = "representante@alphaville.com"

    print("\n" + "=" * 60)
    print("  MEMORIA PERSISTENTE — A IA LEMBRA DO CLIENTE")
    print("=" * 60 + "\n")

    # Primeira interacao — registra informacoes
    print("--- Primeiro contato (registrando informacoes) ---\n")
    agente_com_memoria.print_response(
        "Acabei de visitar a Construtora Horizonte. "
        "Conversei com o Eng. Marcos Ferreira, muito exigente tecnicamente. "
        "Eles tiveram fissuramento nas obras de Cotia. "
        "Interesse em AC-III. Proximo contato em 15 dias.",
        user_id=user_id,
        stream=True,
    )

    print("\n--- Segunda interacao (testando a memoria) ---\n")
    agente_com_memoria.print_response(
        "Que cliente eu deveria priorizar agora?",
        user_id=user_id,
        stream=True,
    )

    # Mostra as memorias salvas
    from rich.pretty import pprint
    from rich.console import Console
    console = Console()
    memories = agente_com_memoria.get_user_memories(user_id=user_id)
    console.print("\n[bold yellow]Memorias salvas sobre seus clientes:[/bold yellow]")
    pprint(memories)


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------
COMANDOS = {
    "cadencia": cadencia,
    "copy": copy_abertura,
    "objecao": objecao,
    "memoria": demo_memoria,
}

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else None

    if cmd not in COMANDOS:
        print("\nUso: python demo_alphaville/extras.py <comando>")
        print("\nComandos disponiveis:")
        for nome in COMANDOS:
            print(f"  {nome}")
        sys.exit(1)

    COMANDOS[cmd]()
