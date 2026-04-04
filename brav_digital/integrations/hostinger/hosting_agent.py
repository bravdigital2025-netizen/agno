"""Agente de hosting da Brav Digital.

Combina acesso ao Hostinger (dominios, VPS, DNS) e ao WordPress (posts, midia),
tudo em um unico agente conversacional.

Uso:
    cp .env.example .env
    .venvs/demo/bin/python brav_digital/integrations/hostinger/hosting_agent.py
"""

from dotenv import load_dotenv

load_dotenv()

from agno.agent import Agent  # noqa: E402
from agno.models.anthropic import Claude  # noqa: E402

from brav_digital.integrations.hostinger.tools import HostingerTools  # noqa: E402
from brav_digital.integrations.wordpress.tools import WordPressTools  # noqa: E402

agent = Agent(
    name="Hosting Agent Brav Digital",
    model=Claude(id="claude-sonnet-4-6"),
    tools=[HostingerTools(), WordPressTools()],
    instructions=[
        "Voce gerencia a infraestrutura de hosting e o site WordPress da Brav Digital.",
        "Hostinger: consulte dominios, VPS, DNS e assinaturas.",
        "WordPress (bravdigital.com): consulte e publique posts, paginas e midias.",
        "Nunca publique posts sem confirmacao do usuario — crie sempre como rascunho primeiro.",
        "Nunca altere registros DNS ou delete recursos sem confirmacao explicita.",
        "Responda sempre em portugues.",
    ],
    show_tool_calls=True,
    markdown=True,
)


def main() -> None:
    print("Hosting Agent — Brav Digital")
    print("Comandos: dominios, VPS, DNS, posts, paginas, midia")
    print("Digite 'sair' para encerrar.\n")

    while True:
        query = input("Voce: ").strip()
        if query.lower() in ("sair", "exit", "quit"):
            break
        if not query:
            continue
        agent.print_response(query, stream=True)
        print()


if __name__ == "__main__":
    main()
