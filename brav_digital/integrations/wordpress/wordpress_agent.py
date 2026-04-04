"""Agente WordPress da Brav Digital.

Agente conversacional que gerencia o site bravdigital.com via WordPress REST API.
Pode listar, criar e publicar posts, gerenciar midia e consultar paginas.

Uso:
    cp .env.example .env
    .venvs/demo/bin/python brav_digital/integrations/wordpress/wordpress_agent.py
"""

import os

from dotenv import load_dotenv

load_dotenv()

from agno.agent import Agent  # noqa: E402
from agno.models.anthropic import Claude  # noqa: E402

from brav_digital.integrations.wordpress.tools import WordPressTools  # noqa: E402

wp_tools = WordPressTools()

agent = Agent(
    name="WordPress Brav Digital",
    model=Claude(id="claude-sonnet-4-6"),
    tools=[wp_tools],
    instructions=[
        "Voce gerencia o site WordPress da Brav Digital (http://bravdigital.com).",
        "Voce pode listar posts, paginas e midias, criar e atualizar posts.",
        "Sempre confirme antes de publicar (status=publish) — prefira criar como rascunho (draft).",
        "Ao criar posts, use HTML basico para formatar o conteudo.",
        "Responda sempre em portugues.",
    ],
    show_tool_calls=True,
    markdown=True,
)


def main() -> None:
    print("Agente WordPress Brav Digital")
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
