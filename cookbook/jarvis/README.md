# Jarvis — Construction Intelligence OS

Jarvis is an AI operating system for Brazilian construction material store owners ("donos de lojas de materiais de construção"). It is a multi-tenant SaaS where each store has its own intelligent agent, powered by Claude Sonnet via the [agno](https://github.com/agno-agi/agno) framework.

---

## What Jarvis Does

Jarvis integrates all operational data from a construction store and provides AI-powered assistance across five domains:

| Agent | Responsibility |
|-------|---------------|
| Inventory Agent | Stock monitoring, critical alerts, reorder suggestions |
| Marketing Agent | WhatsApp campaigns, customer segmentation, promotions |
| WhatsApp Agent | Customer service, product Q&A, availability checks |
| Projects Agent | Architectural PDF analysis, materials extraction, cost quotes |
| Reports Agent | Daily/weekly/monthly executive reports, trend analysis |

The main **Jarvis Team** orchestrates all agents, routing each request to the right specialist and synthesizing responses into a single, actionable reply.

---

## Architecture

```
cookbook/jarvis/
├── config.py              # TenantConfig — one config per store (tenant)
├── jarvis.py              # Main Team orchestrator
├── demo.py                # Demo script with sample queries
├── agents/
│   ├── inventory_agent.py # Stock monitoring and reorder
│   ├── marketing_agent.py # WhatsApp campaigns
│   ├── whatsapp_agent.py  # Customer service
│   ├── projects_agent.py  # Project analysis + cost quotes
│   └── reports_agent.py   # Executive reports
└── README.md
```

Each store (tenant) is isolated by `tenant_id` in `TenantConfig`, with its own database URL, WhatsApp credentials, and store name.

---

## Setup

### 1. Install dependencies

```bash
./scripts/demo_setup.sh
```

### 2. Start the database

```bash
./cookbook/scripts/run_pgvector.sh
```

### 3. Configure environment variables

Copy `.env.example` and fill in your credentials:

```bash
cp .env.example .env
```

Required variables:

```env
# Database
DATABASE_URL=postgresql+psycopg://ai:ai@localhost:5532/ai

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# WhatsApp (optional — required only for marketing/whatsapp agents)
WHATSAPP_ACCESS_TOKEN=...
WHATSAPP_PHONE_NUMBER_ID=...

# Tenant
TENANT_demo_STORE_NAME=Materiais Construção Demo
```

### 4. Run the demo

```bash
.venvs/demo/bin/python cookbook/jarvis/demo.py
```

---

## Usage

```python
from cookbook.jarvis.config import get_tenant_config
from cookbook.jarvis.jarvis import get_jarvis_team

tenant = get_tenant_config("minha-loja")
jarvis = get_jarvis_team(tenant)

jarvis.print_response(
    "Quais produtos estão com estoque crítico esta semana?",
    stream=True,
)
```

---

## Sample Interactions

```
Consulta: Quais produtos estão com estoque crítico esta semana?
-> Agente de Estoque analisa o banco e lista produtos abaixo do mínimo

Consulta: Crie uma campanha de WhatsApp para clientes que compraram cimento nos últimos 30 dias.
-> Agente de Marketing segmenta clientes e compõe mensagem promocional

Consulta: Gere um relatório executivo de vendas do mês.
-> Agente de Relatórios consulta dados e gera resumo gerencial

Consulta: Um cliente quer orçamento para uma casa de 80m².
-> Agente de Projetos calcula materiais e gera ProjectQuote estruturado
```

---

## Multi-Tenancy

Each tenant (store) has its own isolated configuration:

```python
from cookbook.jarvis.config import get_tenant_config

loja_a = get_tenant_config("loja-sao-paulo")
loja_b = get_tenant_config("loja-belo-horizonte")
```

Environment variables follow the pattern `TENANT_{tenant_id}_{KEY}`.
