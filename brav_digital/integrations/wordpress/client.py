"""WordPress REST API client for Brav Digital."""

import os
from typing import Any

import httpx


class WordPressClient:
    """Low-level client for the WordPress REST API.

    Authentication:
        Uses HTTP Basic Auth with a WordPress Application Password.
        Generate one at: WordPress Admin > Users > Profile > Application Passwords.

        Alternatively, set WORDPRESS_API_KEY for Bearer token auth
        (e.g. Hostinger API key or JWT plugin token).
    """

    def __init__(
        self,
        base_url: str | None = None,
        username: str | None = None,
        app_password: str | None = None,
        api_key: str | None = None,
    ) -> None:
        self.base_url = (base_url or os.getenv("WORDPRESS_URL", "http://bravdigital.com")).rstrip("/")
        self.api_base = f"{self.base_url}/wp-json/wp/v2"

        # Build auth headers
        self._username = username or os.getenv("WORDPRESS_USERNAME", "")
        self._app_password = app_password or os.getenv("WORDPRESS_APP_PASSWORD", "")
        self._api_key = api_key or os.getenv("WORDPRESS_API_KEY", "")

        headers: dict[str, str] = {"Content-Type": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        auth = None
        if self._username and self._app_password:
            auth = (self._username, self._app_password)

        self._client = httpx.Client(
            headers=headers,
            auth=auth,
            timeout=30.0,
            follow_redirects=True,
        )

    # ------------------------------------------------------------------
    # Site
    # ------------------------------------------------------------------

    def get_site_info(self) -> dict[str, Any]:
        """Return basic site information."""
        resp = self._client.get(f"{self.base_url}/wp-json/")
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # Posts
    # ------------------------------------------------------------------

    def list_posts(
        self,
        status: str = "publish",
        per_page: int = 10,
        page: int = 1,
        search: str = "",
        order_by: str = "date",
    ) -> list[dict[str, Any]]:
        params: dict[str, Any] = {
            "status": status,
            "per_page": per_page,
            "page": page,
            "orderby": order_by,
        }
        if search:
            params["search"] = search
        resp = self._client.get(f"{self.api_base}/posts", params=params)
        resp.raise_for_status()
        return resp.json()

    def get_post(self, post_id: int) -> dict[str, Any]:
        resp = self._client.get(f"{self.api_base}/posts/{post_id}")
        resp.raise_for_status()
        return resp.json()

    def create_post(
        self,
        title: str,
        content: str,
        status: str = "draft",
        excerpt: str = "",
        categories: list[int] | None = None,
        tags: list[int] | None = None,
        featured_media: int | None = None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "title": title,
            "content": content,
            "status": status,
        }
        if excerpt:
            payload["excerpt"] = excerpt
        if categories:
            payload["categories"] = categories
        if tags:
            payload["tags"] = tags
        if featured_media:
            payload["featured_media"] = featured_media
        resp = self._client.post(f"{self.api_base}/posts", json=payload)
        resp.raise_for_status()
        return resp.json()

    def update_post(self, post_id: int, **fields: Any) -> dict[str, Any]:
        resp = self._client.post(f"{self.api_base}/posts/{post_id}", json=fields)
        resp.raise_for_status()
        return resp.json()

    def delete_post(self, post_id: int, force: bool = False) -> dict[str, Any]:
        resp = self._client.delete(
            f"{self.api_base}/posts/{post_id}",
            params={"force": force},
        )
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # Pages
    # ------------------------------------------------------------------

    def list_pages(self, per_page: int = 20, status: str = "publish") -> list[dict[str, Any]]:
        resp = self._client.get(
            f"{self.api_base}/pages",
            params={"per_page": per_page, "status": status},
        )
        resp.raise_for_status()
        return resp.json()

    def get_page(self, page_id: int) -> dict[str, Any]:
        resp = self._client.get(f"{self.api_base}/pages/{page_id}")
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # Media
    # ------------------------------------------------------------------

    def list_media(
        self,
        media_type: str = "image",
        per_page: int = 20,
    ) -> list[dict[str, Any]]:
        resp = self._client.get(
            f"{self.api_base}/media",
            params={"media_type": media_type, "per_page": per_page},
        )
        resp.raise_for_status()
        return resp.json()

    def upload_media(
        self,
        file_path: str,
        title: str = "",
        alt_text: str = "",
        caption: str = "",
    ) -> dict[str, Any]:
        import mimetypes

        mime_type, _ = mimetypes.guess_type(file_path)
        mime_type = mime_type or "application/octet-stream"
        filename = os.path.basename(file_path)

        headers = {
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Type": mime_type,
        }
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"

        with open(file_path, "rb") as f:
            resp = self._client.post(
                f"{self.api_base}/media",
                content=f.read(),
                headers=headers,
            )
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()

        # Update metadata if provided
        if title or alt_text or caption:
            meta: dict[str, Any] = {}
            if title:
                meta["title"] = title
            if alt_text:
                meta["alt_text"] = alt_text
            if caption:
                meta["caption"] = caption
            result = self.update_media(result["id"], **meta)

        return result

    def update_media(self, media_id: int, **fields: Any) -> dict[str, Any]:
        resp = self._client.post(f"{self.api_base}/media/{media_id}", json=fields)
        resp.raise_for_status()
        return resp.json()

    # ------------------------------------------------------------------
    # Categories & Tags
    # ------------------------------------------------------------------

    def list_categories(self, per_page: int = 50) -> list[dict[str, Any]]:
        resp = self._client.get(f"{self.api_base}/categories", params={"per_page": per_page})
        resp.raise_for_status()
        return resp.json()

    def list_tags(self, per_page: int = 50) -> list[dict[str, Any]]:
        resp = self._client.get(f"{self.api_base}/tags", params={"per_page": per_page})
        resp.raise_for_status()
        return resp.json()

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "WordPressClient":
        return self

    def __exit__(self, *_: Any) -> None:
        self.close()
