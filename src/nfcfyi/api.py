"""HTTP API client for nfcfyi.com REST endpoints.

Requires the ``api`` extra: ``pip install nfcfyi[api]``

Usage::

    from nfcfyi.api import NFCFYI

    with NFCFYI() as api:
        items = api.list_chip_families()
        detail = api.get_chip_family("example-slug")
        results = api.search("query")
"""

from __future__ import annotations

from typing import Any

import httpx


class NFCFYI:
    """API client for the nfcfyi.com REST API.

    Provides typed access to all nfcfyi.com endpoints including
    list, detail, and search operations.

    Args:
        base_url: API base URL. Defaults to ``https://nfcfyi.com``.
        timeout: Request timeout in seconds. Defaults to ``10.0``.
    """

    def __init__(
        self,
        base_url: str = "https://nfcfyi.com",
        timeout: float = 10.0,
    ) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(
            path,
            params={k: v for k, v in params.items() if v is not None},
        )
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    # -- Endpoints -----------------------------------------------------------

    def list_chip_families(self, **params: Any) -> dict[str, Any]:
        """List all chip families."""
        return self._get("/api/v1/chip-families/", **params)

    def get_chip_family(self, slug: str) -> dict[str, Any]:
        """Get chip family by slug."""
        return self._get(f"/api/v1/chip-families/" + slug + "/")

    def list_chips(self, **params: Any) -> dict[str, Any]:
        """List all chips."""
        return self._get("/api/v1/chips/", **params)

    def get_chip(self, slug: str) -> dict[str, Any]:
        """Get chip by slug."""
        return self._get(f"/api/v1/chips/" + slug + "/")

    def list_faqs(self, **params: Any) -> dict[str, Any]:
        """List all faqs."""
        return self._get("/api/v1/faqs/", **params)

    def get_faq(self, slug: str) -> dict[str, Any]:
        """Get faq by slug."""
        return self._get(f"/api/v1/faqs/" + slug + "/")

    def list_frequency_bands(self, **params: Any) -> dict[str, Any]:
        """List all frequency bands."""
        return self._get("/api/v1/frequency-bands/", **params)

    def get_frequency_band(self, slug: str) -> dict[str, Any]:
        """Get frequency band by slug."""
        return self._get(f"/api/v1/frequency-bands/" + slug + "/")

    def list_glossary(self, **params: Any) -> dict[str, Any]:
        """List all glossary."""
        return self._get("/api/v1/glossary/", **params)

    def get_term(self, slug: str) -> dict[str, Any]:
        """Get term by slug."""
        return self._get(f"/api/v1/glossary/" + slug + "/")

    def list_guides(self, **params: Any) -> dict[str, Any]:
        """List all guides."""
        return self._get("/api/v1/guides/", **params)

    def get_guide(self, slug: str) -> dict[str, Any]:
        """Get guide by slug."""
        return self._get(f"/api/v1/guides/" + slug + "/")

    def list_manufacturers(self, **params: Any) -> dict[str, Any]:
        """List all manufacturers."""
        return self._get("/api/v1/manufacturers/", **params)

    def get_manufacturer(self, slug: str) -> dict[str, Any]:
        """Get manufacturer by slug."""
        return self._get(f"/api/v1/manufacturers/" + slug + "/")

    def list_ndef_types(self, **params: Any) -> dict[str, Any]:
        """List all ndef types."""
        return self._get("/api/v1/ndef-types/", **params)

    def get_ndef_type(self, slug: str) -> dict[str, Any]:
        """Get ndef type by slug."""
        return self._get(f"/api/v1/ndef-types/" + slug + "/")

    def list_operating_modes(self, **params: Any) -> dict[str, Any]:
        """List all operating modes."""
        return self._get("/api/v1/operating-modes/", **params)

    def get_operating_mode(self, slug: str) -> dict[str, Any]:
        """Get operating mode by slug."""
        return self._get(f"/api/v1/operating-modes/" + slug + "/")

    def list_security_protocols(self, **params: Any) -> dict[str, Any]:
        """List all security protocols."""
        return self._get("/api/v1/security-protocols/", **params)

    def get_security_protocol(self, slug: str) -> dict[str, Any]:
        """Get security protocol by slug."""
        return self._get(f"/api/v1/security-protocols/" + slug + "/")

    def list_standards(self, **params: Any) -> dict[str, Any]:
        """List all standards."""
        return self._get("/api/v1/standards/", **params)

    def get_standard(self, slug: str) -> dict[str, Any]:
        """Get standard by slug."""
        return self._get(f"/api/v1/standards/" + slug + "/")

    def list_tag_types(self, **params: Any) -> dict[str, Any]:
        """List all tag types."""
        return self._get("/api/v1/tag-types/", **params)

    def get_tag_type(self, slug: str) -> dict[str, Any]:
        """Get tag type by slug."""
        return self._get(f"/api/v1/tag-types/" + slug + "/")

    def list_tools(self, **params: Any) -> dict[str, Any]:
        """List all tools."""
        return self._get("/api/v1/tools/", **params)

    def get_tool(self, slug: str) -> dict[str, Any]:
        """Get tool by slug."""
        return self._get(f"/api/v1/tools/" + slug + "/")

    def list_use_cases(self, **params: Any) -> dict[str, Any]:
        """List all use cases."""
        return self._get("/api/v1/use-cases/", **params)

    def get_use_case(self, slug: str) -> dict[str, Any]:
        """Get use case by slug."""
        return self._get(f"/api/v1/use-cases/" + slug + "/")

    def search(self, query: str, **params: Any) -> dict[str, Any]:
        """Search across all content."""
        return self._get(f"/api/v1/search/", q=query, **params)

    # -- Lifecycle -----------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> NFCFYI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
