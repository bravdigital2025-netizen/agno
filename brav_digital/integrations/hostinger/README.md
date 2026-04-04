# Hostinger Integration — Brav Digital

Integração com a API da Hostinger para gerenciar domínios, VPS, DNS e assinaturas,
combinada com o WordPress em `bravdigital.com`.

---

## Funcionalidades

### Hostinger API

| Acao | Metodo |
|------|--------|
| Listar VPS | `list_vps()` |
| Status + metricas do VPS | `get_vps(id)` / `get_vps_metrics(id)` |
| Listar dominios | `list_domains()` |
| Listar subdomains | `list_subdomains()` |
| Listar registros DNS | `list_dns_records(domain)` |
| Criar registro DNS | `create_dns_record(domain, type, name, content)` |
| Listar assinaturas | `list_subscriptions()` |

### WordPress

Ver `brav_digital/integrations/wordpress/README.md`.

---

## Setup

### 1. Token da Hostinger

1. Acesse [hPanel](https://hpanel.hostinger.com)
2. Clique no ícone do perfil (canto superior direito)
3. Vá em **Informações da conta > API**
4. Clique em **Gerar token**
5. Copie o token gerado

### 2. Application Password do WordPress

1. Acesse WordPress Admin > **Usuários > Perfil**
2. Role até **Senhas de Aplicativo**
3. Crie uma chamada "Jarvis API" e copie a senha

### 3. Configurar .env

```bash
cp brav_digital/integrations/hostinger/.env.example .env
```

```env
HOSTINGER_API_TOKEN=seu_token_hostinger
WORDPRESS_URL=http://bravdigital.com
WORDPRESS_USERNAME=seu_usuario_wp
WORDPRESS_APP_PASSWORD=xxxx xxxx xxxx xxxx xxxx xxxx
```

### 4. Testar conexão

```bash
.venvs/demo/bin/python brav_digital/integrations/hostinger/test_connection.py
```

### 5. Rodar o agente

```bash
.venvs/demo/bin/python brav_digital/integrations/hostinger/hosting_agent.py
```

---

## Exemplos de uso no agente

```
Voce: quais são meus dominios?
Voce: mostre os 5 posts mais recentes do site
Voce: qual o status do meu VPS?
Voce: liste os registros DNS do bravdigital.com
Voce: crie um post rascunho com o título "Novidades de Abril"
```

---

## Estrutura

```
hostinger/
├── __init__.py           # Exports
├── client.py             # Cliente HTTP Hostinger API
├── tools.py              # Agno Toolkit (Hostinger)
├── hosting_agent.py      # Agente combinado Hostinger + WordPress
├── test_connection.py    # Testa ambas as conexões
├── .env.example          # Template de variáveis
└── README.md             # Este arquivo
```
