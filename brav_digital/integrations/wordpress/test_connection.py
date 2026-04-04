"""Test da conexao com o WordPress da Brav Digital.

Uso:
    cp .env.example .env
    # edite .env com suas credenciais
    .venvs/demo/bin/python brav_digital/integrations/wordpress/test_connection.py
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

from brav_digital.integrations.wordpress import WordPressClient  # noqa: E402


def main() -> None:
    url = os.getenv("WORDPRESS_URL", "http://bravdigital.com")
    print(f"Conectando em: {url}")

    try:
        with WordPressClient() as wp:
            # 1. Site info
            print("\n--- Site ---")
            info = wp.get_site_info()
            print(f"Nome : {info.get('name')}")
            print(f"Desc : {info.get('description')}")
            print(f"URL  : {info.get('url')}")

            # 2. Posts
            print("\n--- Posts publicados (5 mais recentes) ---")
            posts = wp.list_posts(per_page=5)
            if posts:
                for p in posts:
                    print(f"  [{p['id']}] {p['title']['rendered']} ({p['date'][:10]})")
            else:
                print("  Nenhum post encontrado.")

            # 3. Paginas
            print("\n--- Paginas ---")
            pages = wp.list_pages(per_page=5)
            if pages:
                for pg in pages:
                    print(f"  [{pg['id']}] {pg['title']['rendered']}")
            else:
                print("  Nenhuma pagina encontrada.")

            # 4. Midia
            print("\n--- Midias (5 mais recentes) ---")
            media = wp.list_media(per_page=5)
            if media:
                for m in media:
                    print(f"  [{m['id']}] {m['title']['rendered']} — {m['source_url']}")
            else:
                print("  Nenhuma midia encontrada.")

            print("\nConexao OK.")

    except Exception as e:
        print(f"\nERRO: {e}", file=sys.stderr)
        print("\nVerifique as variaveis de ambiente em .env:", file=sys.stderr)
        print("  WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_APP_PASSWORD", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
