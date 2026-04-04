"""WordPress Agno Toolkit for Brav Digital agents."""

import json
from typing import Any

from agno.tools import Toolkit

from .client import WordPressClient


class WordPressTools(Toolkit):
    """Agno toolkit that exposes WordPress REST API actions to AI agents.

    Usage::

        from brav_digital.integrations.wordpress.tools import WordPressTools

        agent = Agent(
            tools=[WordPressTools()],
            ...
        )
    """

    def __init__(
        self,
        base_url: str | None = None,
        username: str | None = None,
        app_password: str | None = None,
        api_key: str | None = None,
    ) -> None:
        super().__init__(name="wordpress")
        self._wp = WordPressClient(
            base_url=base_url,
            username=username,
            app_password=app_password,
            api_key=api_key,
        )
        self.register(self.get_site_info)
        self.register(self.list_posts)
        self.register(self.get_post)
        self.register(self.create_post)
        self.register(self.update_post)
        self.register(self.list_pages)
        self.register(self.list_media)
        self.register(self.upload_media)
        self.register(self.list_categories)
        self.register(self.list_tags)

    # ------------------------------------------------------------------
    # Site
    # ------------------------------------------------------------------

    def get_site_info(self) -> str:
        """Return the name, description, URL and WordPress version of the site."""
        try:
            info = self._wp.get_site_info()
            return json.dumps(
                {
                    "name": info.get("name"),
                    "description": info.get("description"),
                    "url": info.get("url"),
                    "wp_version": info.get("generator", {}).get("version"),
                    "timezone": info.get("timezone_string"),
                },
                ensure_ascii=False,
            )
        except Exception as e:
            return f"Erro ao buscar informacoes do site: {e}"

    # ------------------------------------------------------------------
    # Posts
    # ------------------------------------------------------------------

    def list_posts(
        self,
        status: str = "publish",
        per_page: int = 10,
        search: str = "",
    ) -> str:
        """List posts from the WordPress site.

        Args:
            status: Post status — publish, draft, pending, private (default: publish).
            per_page: Number of posts to return (max 100, default 10).
            search: Optional keyword to filter posts by title or content.
        """
        try:
            posts = self._wp.list_posts(status=status, per_page=per_page, search=search)
            result = [
                {
                    "id": p["id"],
                    "title": p["title"]["rendered"],
                    "status": p["status"],
                    "date": p["date"],
                    "link": p["link"],
                    "excerpt": p.get("excerpt", {}).get("rendered", "")[:200],
                }
                for p in posts
            ]
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return f"Erro ao listar posts: {e}"

    def get_post(self, post_id: int) -> str:
        """Get the full content of a WordPress post by ID.

        Args:
            post_id: The numeric WordPress post ID.
        """
        try:
            p = self._wp.get_post(post_id)
            return json.dumps(
                {
                    "id": p["id"],
                    "title": p["title"]["rendered"],
                    "content": p["content"]["rendered"],
                    "excerpt": p.get("excerpt", {}).get("rendered", ""),
                    "status": p["status"],
                    "date": p["date"],
                    "modified": p["modified"],
                    "link": p["link"],
                    "categories": p.get("categories", []),
                    "tags": p.get("tags", []),
                    "featured_media": p.get("featured_media"),
                },
                ensure_ascii=False,
            )
        except Exception as e:
            return f"Erro ao buscar post {post_id}: {e}"

    def create_post(
        self,
        title: str,
        content: str,
        status: str = "draft",
        excerpt: str = "",
    ) -> str:
        """Create a new post on the WordPress site.

        Args:
            title: Post title (plain text).
            content: Post body in HTML or plain text.
            status: 'draft' (default) or 'publish' to go live immediately.
            excerpt: Short summary shown in post listings.
        """
        try:
            p = self._wp.create_post(
                title=title,
                content=content,
                status=status,
                excerpt=excerpt,
            )
            return json.dumps(
                {
                    "id": p["id"],
                    "title": p["title"]["rendered"],
                    "status": p["status"],
                    "link": p["link"],
                    "edit_link": p.get("_links", {}).get("self", [{}])[0].get("href", ""),
                },
                ensure_ascii=False,
            )
        except Exception as e:
            return f"Erro ao criar post: {e}"

    def update_post(
        self,
        post_id: int,
        title: str = "",
        content: str = "",
        status: str = "",
        excerpt: str = "",
    ) -> str:
        """Update an existing WordPress post.

        Args:
            post_id: The numeric post ID to update.
            title: New title (leave empty to keep current).
            content: New body content (leave empty to keep current).
            status: New status — publish, draft, private (leave empty to keep current).
            excerpt: New excerpt (leave empty to keep current).
        """
        try:
            fields: dict[str, Any] = {}
            if title:
                fields["title"] = title
            if content:
                fields["content"] = content
            if status:
                fields["status"] = status
            if excerpt:
                fields["excerpt"] = excerpt
            if not fields:
                return "Nenhum campo fornecido para atualizar."
            p = self._wp.update_post(post_id, **fields)
            return json.dumps(
                {"id": p["id"], "status": p["status"], "link": p["link"]},
                ensure_ascii=False,
            )
        except Exception as e:
            return f"Erro ao atualizar post {post_id}: {e}"

    # ------------------------------------------------------------------
    # Pages
    # ------------------------------------------------------------------

    def list_pages(self, per_page: int = 20, status: str = "publish") -> str:
        """List pages on the WordPress site.

        Args:
            per_page: Number of pages to return (default 20).
            status: Page status — publish, draft (default: publish).
        """
        try:
            pages = self._wp.list_pages(per_page=per_page, status=status)
            result = [
                {
                    "id": pg["id"],
                    "title": pg["title"]["rendered"],
                    "status": pg["status"],
                    "link": pg["link"],
                    "parent": pg.get("parent", 0),
                    "menu_order": pg.get("menu_order", 0),
                }
                for pg in pages
            ]
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return f"Erro ao listar paginas: {e}"

    # ------------------------------------------------------------------
    # Media
    # ------------------------------------------------------------------

    def list_media(self, media_type: str = "image", per_page: int = 20) -> str:
        """List media files uploaded to WordPress.

        Args:
            media_type: Filter by type — image, video, audio, application (default: image).
            per_page: Number of items to return (default 20).
        """
        try:
            items = self._wp.list_media(media_type=media_type, per_page=per_page)
            result = [
                {
                    "id": m["id"],
                    "title": m["title"]["rendered"],
                    "url": m["source_url"],
                    "alt_text": m.get("alt_text", ""),
                    "mime_type": m.get("mime_type", ""),
                    "date": m["date"],
                }
                for m in items
            ]
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return f"Erro ao listar midia: {e}"

    def upload_media(
        self,
        file_path: str,
        title: str = "",
        alt_text: str = "",
        caption: str = "",
    ) -> str:
        """Upload a local file to the WordPress media library.

        Args:
            file_path: Absolute path to the local file to upload.
            title: Media title (optional).
            alt_text: Image alt text for accessibility and SEO (optional).
            caption: Caption shown below the image (optional).
        """
        try:
            m = self._wp.upload_media(
                file_path=file_path,
                title=title,
                alt_text=alt_text,
                caption=caption,
            )
            return json.dumps(
                {
                    "id": m["id"],
                    "url": m["source_url"],
                    "title": m["title"]["rendered"],
                    "alt_text": m.get("alt_text", ""),
                },
                ensure_ascii=False,
            )
        except Exception as e:
            return f"Erro ao fazer upload de midia: {e}"

    # ------------------------------------------------------------------
    # Taxonomies
    # ------------------------------------------------------------------

    def list_categories(self) -> str:
        """List all post categories available on the WordPress site."""
        try:
            cats = self._wp.list_categories()
            result = [
                {"id": c["id"], "name": c["name"], "slug": c["slug"], "count": c["count"]}
                for c in cats
            ]
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return f"Erro ao listar categorias: {e}"

    def list_tags(self) -> str:
        """List all post tags available on the WordPress site."""
        try:
            tags = self._wp.list_tags()
            result = [
                {"id": t["id"], "name": t["name"], "slug": t["slug"], "count": t["count"]}
                for t in tags
            ]
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return f"Erro ao listar tags: {e}"
