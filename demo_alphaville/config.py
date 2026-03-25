"""
Configuracao central da demo Argamassa Alphaville.
Carrega o token de autenticacao do ambiente.
"""

import os

# Tenta carregar o token de auth via variavel de ambiente ou arquivo de sessao
AUTH_TOKEN = os.environ.get("ANTHROPIC_AUTH_TOKEN") or os.environ.get("ANTHROPIC_API_KEY")

if not AUTH_TOKEN:
    for token_file in [
        os.path.expanduser("~/.claude/remote/.session_ingress_token"),
        "/home/claude/.claude/remote/.session_ingress_token",
    ]:
        try:
            with open(token_file) as f:
                AUTH_TOKEN = f.read().strip()
            if AUTH_TOKEN:
                break
        except FileNotFoundError:
            continue

if not AUTH_TOKEN:
    raise EnvironmentError(
        "Nenhum token de autenticacao encontrado.\n"
        "Defina ANTHROPIC_AUTH_TOKEN ou ANTHROPIC_API_KEY."
    )

# Modelo padrao — haiku para velocidade ao vivo
MODEL_FAST = "claude-haiku-4-5-20251001"

# Modelo principal — sonnet para qualidade
MODEL_MAIN = "claude-sonnet-4-6"
