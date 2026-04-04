# WordPress Integration — Brav Digital

Integração com o WordPress de `http://bravdigital.com` via REST API.

---

## Funcionalidades

| Acao | Metodo |
|------|--------|
| Info do site | `get_site_info()` |
| Listar posts | `list_posts(status, per_page, search)` |
| Ler post | `get_post(post_id)` |
| Criar post | `create_post(title, content, status)` |
| Atualizar post | `update_post(post_id, ...)` |
| Listar paginas | `list_pages()` |
| Listar midia | `list_media(media_type)` |
| Upload de midia | `upload_media(file_path, alt_text)` |
| Listar categorias | `list_categories()` |
| Listar tags | `list_tags()` |

---

## Setup

### 1. Credenciais

```bash
cp brav_digital/integrations/wordpress/.env.example .env
```

Edite `.env` com:

```env
WORDPRESS_URL=http://bravdigital.com
WORDPRESS_USERNAME=seu_usuario
WORDPRESS_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
```

**Gerar Application Password:**
1. Acesse WordPress Admin > Usuários > Perfil
2. Role até "Senhas de Aplicativo"
3. Digite um nome (ex: "Jarvis API") e clique em "Adicionar nova senha de aplicativo"
4. Copie a senha gerada (formato: `xxxx xxxx xxxx xxxx xxxx xxxx`)

### 2. Testar conexão

```bash
.venvs/demo/bin/python brav_digital/integrations/wordpress/test_connection.py
```

### 3. Rodar o agente conversacional

```bash
.venvs/demo/bin/python brav_digital/integrations/wordpress/wordpress_agent.py
```

---

## Uso como Toolkit no Jarvis

```python
from brav_digital.integrations.wordpress.tools import WordPressTools
from agno.agent import Agent

agent = Agent(
    tools=[WordPressTools()],
    ...
)
```

---

## Autenticacao

| Metodo | Variavel | Quando usar |
|--------|----------|-------------|
| Application Password | `WORDPRESS_USERNAME` + `WORDPRESS_APP_PASSWORD` | Padrao — integrado ao WordPress |
| Bearer Token / API Key | `WORDPRESS_API_KEY` | JWT plugin ou API do hosting |

---

## Estrutura

```
wordpress/
├── __init__.py           # Exports principais
├── client.py             # Cliente HTTP baixo nível
├── tools.py              # Agno Toolkit (usa client.py)
├── wordpress_agent.py    # Agente conversacional de exemplo
├── test_connection.py    # Script de teste de conectividade
├── .env.example          # Template de variaveis de ambiente
└── README.md             # Este arquivo
```
