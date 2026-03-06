"""HTTP API client for nfcfyi.com REST endpoints.

Requires the ``api`` extra: ``pip install nfcfyi[api]``

Usage::

    from nfcfyi.api import NFCFYI

    with NFCFYI() as api:
        results = api.search("ntag")
        chip = api.chip("ntag215")
        comparison = api.compare("ntag213", "ntag215")
"""

from __future__ import annotations

from typing import Any

import httpx


class NFCFYI:
    """API client for the nfcfyi.com REST API.

    Provides access to 11 endpoints covering NFC chips, chip families,
    standards, operating modes, NDEF record types, use cases, glossary terms,
    search, comparison, and random discovery.

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

    # -- HTTP helpers ----------------------------------------------------------

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(path, params={k: v for k, v in params.items() if v is not None})
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    # -- Endpoints -------------------------------------------------------------

    def chip(self, slug: str) -> dict[str, Any]:
        """Get NFC chip detail with specs, memory layout, and supported standards.

        Args:
            slug: Chip URL slug (e.g. ``"ntag213"``, ``"ntag215"``, ``"st25ta02k"``).
        """
        return self._get(f"/api/chip/{slug}/")

    def chip_family(self, slug: str) -> dict[str, Any]:
        """Get chip family with product line overview and member chips.

        Args:
            slug: Family URL slug (e.g. ``"ntag-21x"``, ``"mifare-ultralight"``).
        """
        return self._get(f"/api/chip-family/{slug}/")

    def standard(self, slug: str) -> dict[str, Any]:
        """Get NFC standard detail with linked chips and protocols.

        Args:
            slug: Standard URL slug (e.g. ``"iso-14443"``, ``"iso-15693"``).
        """
        return self._get(f"/api/standard/{slug}/")

    def operating_mode(self, slug: str) -> dict[str, Any]:
        """Get NFC operating mode detail with protocol flow and use cases.

        Args:
            slug: Operating mode URL slug (e.g. ``"read-write"``, ``"card-emulation"``).
        """
        return self._get(f"/api/operating-mode/{slug}/")

    def ndef_type(self, slug: str) -> dict[str, Any]:
        """Get NDEF record type detail with encoding format and examples.

        Args:
            slug: NDEF type URL slug (e.g. ``"text"``, ``"uri"``, ``"smart-poster"``).
        """
        return self._get(f"/api/ndef-type/{slug}/")

    def use_case(self, slug: str) -> dict[str, Any]:
        """Get NFC use case detail with recommended chips and implementation notes.

        Args:
            slug: Use case URL slug (e.g. ``"access-control"``, ``"payments"``).
        """
        return self._get(f"/api/use-case/{slug}/")

    def glossary_term(self, slug: str) -> dict[str, Any]:
        """Get glossary term definition for tooltips and reference.

        Args:
            slug: Term URL slug (e.g. ``"ndef"``, ``"anti-collision"``, ``"atqa"``).
        """
        return self._get(f"/api/term/{slug}/")

    def search(self, query: str) -> dict[str, Any]:
        """Search across chips, standards, NDEF types, use cases, and glossary terms.

        Args:
            query: Search term (minimum 2 characters).
        """
        return self._get("/api/search/", q=query)

    def compare(self, slug_a: str, slug_b: str) -> dict[str, Any]:
        """Compare two NFC chips side by side.

        Args:
            slug_a: First chip slug (e.g. ``"ntag213"``).
            slug_b: Second chip slug (e.g. ``"ntag215"``).
        """
        return self._get("/api/compare/", a=slug_a, b=slug_b)

    def random(self) -> dict[str, Any]:
        """Get a random NFC chip with full detail."""
        return self._get("/api/random/")

    def openapi(self) -> dict[str, Any]:
        """Get the OpenAPI 3.1.0 specification."""
        return self._get("/api/openapi.json")

    # -- Context manager -------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP connection."""
        self._client.close()

    def __enter__(self) -> NFCFYI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
