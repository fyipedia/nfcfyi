"""MCP server for nfcfyi — AI assistant tools for nfcfyi.com.

Run: uvx --from "nfcfyi[mcp]" python -m nfcfyi.mcp_server
"""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("NFCFYI")


@mcp.tool()
def list_chips(limit: int = 20, offset: int = 0) -> str:
    """List chips from nfcfyi.com.

    Args:
        limit: Maximum number of results. Default 20.
        offset: Number of results to skip. Default 0.
    """
    from nfcfyi.api import NFCFYI

    with NFCFYI() as api:
        data = api.list_chips(limit=limit, offset=offset)
        results = data.get("results", data) if isinstance(data, dict) else data
        if not results:
            return "No chips found."
        items = results[:limit] if isinstance(results, list) else []
        return "\n".join(f"- {item.get('name', item.get('slug', '?'))}" for item in items)


@mcp.tool()
def get_chip(slug: str) -> str:
    """Get detailed information about a specific chip.

    Args:
        slug: URL slug identifier for the chip.
    """
    from nfcfyi.api import NFCFYI

    with NFCFYI() as api:
        data = api.get_chip(slug)
        return str(data)


@mcp.tool()
def list_ndef_types(limit: int = 20, offset: int = 0) -> str:
    """List ndef_types from nfcfyi.com.

    Args:
        limit: Maximum number of results. Default 20.
        offset: Number of results to skip. Default 0.
    """
    from nfcfyi.api import NFCFYI

    with NFCFYI() as api:
        data = api.list_ndef_types(limit=limit, offset=offset)
        results = data.get("results", data) if isinstance(data, dict) else data
        if not results:
            return "No ndef_types found."
        items = results[:limit] if isinstance(results, list) else []
        return "\n".join(f"- {item.get('name', item.get('slug', '?'))}" for item in items)


@mcp.tool()
def search_nfc(query: str) -> str:
    """Search nfcfyi.com for NFC chips, NDEF types, and manufacturers.

    Args:
        query: Search query string.
    """
    from nfcfyi.api import NFCFYI

    with NFCFYI() as api:
        data = api.search(query)
        results = data.get("results", data) if isinstance(data, dict) else data
        if not results:
            return f"No results found for \"{query}\"."
        items = results[:10] if isinstance(results, list) else []
        return "\n".join(f"- {item.get('name', item.get('slug', '?'))}" for item in items)


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
