"""Testa conexao com a API da Hostinger e com o WordPress da Brav Digital.

Uso:
    cp .env.example .env   # edite com suas credenciais
    .venvs/demo/bin/python brav_digital/integrations/hostinger/test_connection.py
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

from brav_digital.integrations.hostinger import HostingerClient  # noqa: E402
from brav_digital.integrations.wordpress import WordPressClient  # noqa: E402


def test_hostinger() -> None:
    print("=== Hostinger API ===")
    try:
        with HostingerClient() as h:
            # Dominios
            print("\n--- Dominios ---")
            try:
                domains = h.list_domains()
                items = domains if isinstance(domains, list) else domains.get("data", [])
                for d in items:
                    print(f"  {d.get('domain')} — {d.get('status')}")
                if not items:
                    print("  Nenhum dominio encontrado.")
            except Exception as e:
                print(f"  Aviso: {e}")

            # VPS
            print("\n--- VPS ---")
            try:
                vms = h.list_vps()
                items = vms if isinstance(vms, list) else vms.get("data", [])
                for v in items:
                    print(f"  [{v.get('id')}] {v.get('hostname')} — {v.get('state')}")
                if not items:
                    print("  Nenhum VPS encontrado.")
            except Exception as e:
                print(f"  Aviso: {e}")

            # Assinaturas
            print("\n--- Assinaturas ---")
            try:
                subs = h.list_subscriptions()
                items = subs if isinstance(subs, list) else subs.get("data", [])
                for s in items:
                    print(f"  {s.get('name')} — {s.get('status')}")
                if not items:
                    print("  Nenhuma assinatura encontrada.")
            except Exception as e:
                print(f"  Aviso: {e}")

        print("\nHostinger API: OK")
    except Exception as e:
        print(f"\nERRO Hostinger: {e}", file=sys.stderr)
        print("Verifique HOSTINGER_API_TOKEN no .env", file=sys.stderr)


def test_wordpress() -> None:
    print("\n=== WordPress (bravdigital.com) ===")
    url = os.getenv("WORDPRESS_URL", "http://bravdigital.com")
    print(f"URL: {url}")
    try:
        with WordPressClient() as wp:
            info = wp.get_site_info()
            print(f"Nome : {info.get('name')}")
            print(f"URL  : {info.get('url')}")

            posts = wp.list_posts(per_page=3)
            print(f"\nUltimos posts ({len(posts)}):")
            for p in posts:
                print(f"  [{p['id']}] {p['title']['rendered'][:60]}")

        print("\nWordPress API: OK")
    except Exception as e:
        print(f"\nERRO WordPress: {e}", file=sys.stderr)
        print(
            "Verifique WORDPRESS_USERNAME e WORDPRESS_APP_PASSWORD no .env",
            file=sys.stderr,
        )


if __name__ == "__main__":
    test_hostinger()
    test_wordpress()
