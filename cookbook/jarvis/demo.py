"""
Jarvis Demo - Construction Intelligence OS

Run: .venvs/demo/bin/python cookbook/jarvis/demo.py
"""

from cookbook.jarvis.config import DEMO_TENANT
from cookbook.jarvis.jarvis import get_jarvis_team

jarvis = get_jarvis_team(DEMO_TENANT)

# Demo interactions
demo_queries = [
    "Quais produtos estão com estoque crítico esta semana?",
    "Crie uma campanha de WhatsApp para clientes que compraram cimento nos últimos 30 dias.",
    "Gere um relatório executivo de vendas do mês.",
    "Um cliente perguntou: qual a diferença entre o cimento CP II e CP III?",
]

if __name__ == "__main__":
    print(f"Jarvis iniciado para: {DEMO_TENANT.store_name}")
    print("=" * 60)
    for query in demo_queries:
        print(f"\nConsulta: {query}")
        print("-" * 40)
        jarvis.print_response(query, stream=True)
        print()
