"""
Jarvis — Cotacao de obra a partir de imagem ou PDF

Demonstra como enviar uma planta baixa ou foto de obra para o agente
de projetos e receber um orcamento estruturado (ProjectQuote).

Uso:
    # A partir de um arquivo local
    .venvs/demo/bin/python cookbook/jarvis/quote_from_image.py planta.jpg

    # A partir de uma URL
    .venvs/demo/bin/python cookbook/jarvis/quote_from_image.py https://...

    # Demo sem imagem real (usa descricao textual)
    .venvs/demo/bin/python cookbook/jarvis/quote_from_image.py
"""

import json
import sys
from pathlib import Path
from typing import Optional

from agno.media import Image

from cookbook.jarvis.agents.projects_agent import ProjectQuote, get_projects_agent
from cookbook.jarvis.config import DEMO_TENANT

# ---------------------------------------------------------------------------
# Core function
# ---------------------------------------------------------------------------


def quote_from_image(
    image_path: Optional[str] = None,
    image_url: Optional[str] = None,
    project_description: Optional[str] = None,
) -> Optional[ProjectQuote]:
    """
    Gera um orcamento de obra a partir de uma imagem ou descricao textual.

    Args:
        image_path: Caminho local para a imagem (JPG, PNG, PDF).
        image_url:  URL publica da imagem.
        project_description: Descricao textual do projeto (fallback sem imagem).

    Returns:
        ProjectQuote com materiais, quantidades e valores estimados.
    """
    agent = get_projects_agent(DEMO_TENANT)

    images = []
    if image_path:
        images.append(Image(filepath=image_path))
    elif image_url:
        images.append(Image(url=image_url))

    prompt = project_description or (
        "Analise o projeto arquitetonico enviado e gere um orcamento completo "
        "de materiais de construcao. Identifique todos os materiais necessarios, "
        "calcule as quantidades usando os indices tecnicos corretos e estime "
        "o custo total para a regiao de Sao Paulo, SP."
    )

    response = agent.run(
        prompt,
        images=images if images else None,
    )

    if response and response.content:
        if isinstance(response.content, ProjectQuote):
            return response.content
        # If returned as dict (structured output)
        if isinstance(response.content, dict):
            return ProjectQuote(**response.content)

    return None


async def quote_from_image_async(
    image_path: Optional[str] = None,
    image_url: Optional[str] = None,
    project_description: Optional[str] = None,
) -> Optional[ProjectQuote]:
    """Versao assincrona de quote_from_image."""
    agent = get_projects_agent(DEMO_TENANT)

    images = []
    if image_path:
        images.append(Image(filepath=image_path))
    elif image_url:
        images.append(Image(url=image_url))

    prompt = project_description or (
        "Analise o projeto arquitetonico enviado e gere um orcamento completo "
        "de materiais de construcao. Identifique todos os materiais necessarios, "
        "calcule as quantidades usando os indices tecnicos corretos e estime "
        "o custo total para a regiao de Sao Paulo, SP."
    )

    response = await agent.arun(
        prompt,
        images=images if images else None,
    )

    if response and response.content:
        if isinstance(response.content, ProjectQuote):
            return response.content
        if isinstance(response.content, dict):
            return ProjectQuote(**response.content)

    return None


# ---------------------------------------------------------------------------
# Demo runner
# ---------------------------------------------------------------------------

DEMO_DESCRIPTION = """
Casa terrea de alvenaria com 80m2 de area construida.
Projeto: sala de estar (20m2), 2 quartos (12m2 cada), banheiro (6m2),
cozinha/area de servico (18m2) e area externa coberta (12m2).
Fundacao em sapata corrida. Estrutura em concreto armado.
Cobertura com telha ceramica. Piso ceramico em todos os ambientes.
Paredes com reboco e pintura. Instalacoes hidraulicas completas.
Localizacao: Sao Paulo, SP.
"""


def _print_quote(quote: ProjectQuote) -> None:
    print(f"\nProjeto: {quote.project_name}")
    print(f"Descricao: {quote.descricao}")
    if quote.area_total_m2:
        print(f"Area total: {quote.area_total_m2:.1f} m2")
    print(f"\n{'Material':<40} {'Un':>6} {'Qtd':>10} {'Unit':>10} {'Total':>12}")
    print("-" * 82)
    for item in quote.materials:
        print(
            f"{item.nome:<40} {item.unidade:>6} {item.quantidade:>10.2f} "
            f"R${item.preco_unitario:>9.2f} R${item.subtotal:>11.2f}"
        )
    print("-" * 82)
    print(f"{'TOTAL ESTIMADO':>70} R${quote.total_estimate:>11.2f}")
    if quote.prazo_estimado_dias:
        print(f"\nPrazo estimado: {quote.prazo_estimado_dias} dias uteis")
    if quote.observacoes_gerais:
        print(f"\nObservacoes: {quote.observacoes_gerais}")


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None

    if arg and Path(arg).exists():
        print(f"Analisando imagem local: {arg}")
        quote = quote_from_image(image_path=arg)
    elif arg and arg.startswith("http"):
        print(f"Analisando imagem URL: {arg}")
        quote = quote_from_image(image_url=arg)
    else:
        print("Demo: gerando orcamento a partir de descricao textual")
        quote = quote_from_image(project_description=DEMO_DESCRIPTION)

    if quote:
        _print_quote(quote)
        output_file = "orcamento_jarvis.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(quote.model_dump(), f, ensure_ascii=False, indent=2)
        print(f"\nOrcamento salvo em: {output_file}")
    else:
        print("Nao foi possivel gerar o orcamento.")
