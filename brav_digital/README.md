# Brav Digital — Projetos de IA

Este diretório concentra todos os projetos de IA desenvolvidos pela **Brav Digital**, usando o framework [Agno](https://github.com/agno-agi/agno).

---

## Estrutura

```
brav_digital/
├── README.md          # Este arquivo
├── PROJECTS.md        # Registro e status de todos os projetos
├── jarvis/            # Jarvis — OS de Inteligência para Materiais de Construção
└── ...                # Projetos futuros
```

---

## Projetos

| Projeto | Status | Descrição |
|---------|--------|-----------|
| [Jarvis](./jarvis/) | Em desenvolvimento | OS de IA para lojas de materiais de construção |

---

## Setup do ambiente

```bash
# Criar ambiente virtual de desenvolvimento
./scripts/demo_setup.sh

# Banco de dados (PostgreSQL + pgvector)
./cookbook/scripts/run_pgvector.sh

# Rodar um projeto
.venvs/demo/bin/python brav_digital/<projeto>/<arquivo>.py
```

---

## Padrões e convenções

- Todo projeto tem sua própria pasta dentro de `brav_digital/`
- Cada projeto deve ter `README.md` e `.env.example` próprios
- Não misturar código Brav Digital com os cookbooks genéricos do Agno (`cookbook/`)
- Seguir os padrões do `.cursorrules` do repositório

---

## Contato

Brav Digital — [bravdigital.com.br](https://bravdigital.com.br)
