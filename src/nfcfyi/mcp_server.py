"""MCP server for nfcfyi — NFC chip and NDEF tools for AI assistants.

Requires the ``mcp`` extra: ``pip install nfcfyi[mcp]``

Run as a standalone server::

    python -m nfcfyi.mcp_server

Or configure in ``claude_desktop_config.json``::

    {
        "mcpServers": {
            "nfcfyi": {
                "command": "python",
                "args": ["-m", "nfcfyi.mcp_server"]
            }
        }
    }
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("nfcfyi")


@mcp.tool()
def nfc_search(query: str) -> str:
    """Search for NFC chips, standards, NDEF types, and terminology on NFCFYI.

    Search across NFC chips (NTAG, MIFARE, ST25), standards (ISO 14443, ISO 15693),
    NDEF record types, operating modes, use cases, and glossary terms.

    Args:
        query: Search term (e.g. "ntag", "iso 14443", "ndef", "card emulation").
    """
    from nfcfyi.api import NFCFYI

    with NFCFYI() as api:
        results = api.search(query)

    items = results.get("results", [])
    if not items:
        return f"No results found for '{query}'."

    lines = [
        f"## NFC Search: {query}",
        "",
        f"Found {len(items)} result(s):",
        "",
        "| Type | Name | Slug |",
        "|------|------|------|",
    ]

    for item in items:
        t, n, s = item.get("type", ""), item.get("name", ""), item.get("slug", "")
        lines.append(f"| {t} | {n} | {s} |")

    return "\n".join(lines)


@mcp.tool()
def nfc_lookup(slug: str) -> str:
    """Look up a specific NFC chip by slug.

    Returns full specifications including memory size, NFC Forum type,
    operating frequency, supported standards, and use cases.

    Args:
        slug: Chip slug (e.g. "ntag213", "ntag215", "mifare-ultralight-c", "st25ta02k").
    """
    from nfcfyi.api import NFCFYI

    with NFCFYI() as api:
        data = api.chip(slug)

    lines = [
        f"## {data.get('name', slug)}",
        "",
        data.get("description", ""),
        "",
        f"- **Manufacturer**: {data.get('manufacturer', 'N/A')}",
        f"- **NFC Forum Type**: {data.get('nfc_forum_type', 'N/A')}",
        f"- **Memory Size**: {data.get('memory_size', 'N/A')}",
        f"- **User Memory**: {data.get('user_memory', 'N/A')}",
        f"- **Operating Frequency**: {data.get('operating_frequency', 'N/A')}",
        f"- **Data Transfer Rate**: {data.get('data_transfer_rate', 'N/A')}",
        f"- **UID Length**: {data.get('uid_length', 'N/A')}",
    ]

    standards = data.get("standards", [])
    if standards:
        lines.append("")
        lines.append("### Standards")
        for st in standards:
            lines.append(f"- {st.get('name', '')} ({st.get('organization', '')})")

    return "\n".join(lines)


@mcp.tool()
def nfc_compare(slug_a: str, slug_b: str) -> str:
    """Compare two NFC chips side by side.

    Args:
        slug_a: First chip slug (e.g. "ntag213").
        slug_b: Second chip slug (e.g. "ntag215").
    """
    from nfcfyi.api import NFCFYI

    with NFCFYI() as api:
        data = api.compare(slug_a, slug_b)

    a = data.get("a", {})
    b = data.get("b", {})

    lines = [
        f"## {a.get('name', slug_a)} vs {b.get('name', slug_b)}",
        "",
        "| Property | " + a.get("name", slug_a) + " | " + b.get("name", slug_b) + " |",
        "|----------|"
        + "-" * len(a.get("name", slug_a))
        + "--|"
        + "-" * len(b.get("name", slug_b))
        + "--|",
    ]

    fields = [
        ("Manufacturer", "manufacturer"),
        ("NFC Forum Type", "nfc_forum_type"),
        ("Memory Size", "memory_size"),
        ("User Memory", "user_memory"),
        ("Frequency", "operating_frequency"),
        ("UID Length", "uid_length"),
    ]
    for label, key in fields:
        lines.append(f"| {label} | {a.get(key, '-')} | {b.get(key, '-')} |")

    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
