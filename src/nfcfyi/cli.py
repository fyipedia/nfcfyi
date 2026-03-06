"""Command-line interface for nfcfyi.

Requires the ``cli`` extra: ``pip install nfcfyi[cli]``

Usage::

    nfcfyi search "ntag"
    nfcfyi chip ntag215
    nfcfyi compare ntag213 ntag215
    nfcfyi random
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="nfcfyi",
    help="NFC chip encyclopedia — look up chips, standards, NDEF types, and specs from NFCFYI.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def search(
    query: str = typer.Argument(help="Search term (e.g. 'ntag', 'iso 14443', 'ndef')"),
) -> None:
    """Search across chips, standards, NDEF types, use cases, and glossary."""
    from nfcfyi.api import NFCFYI

    with NFCFYI() as api:
        results = api.search(query)

    table = Table(title=f"Search: {query}")
    table.add_column("Type", style="cyan", no_wrap=True)
    table.add_column("Name")
    table.add_column("Slug")

    items = results.get("results", [])
    if not items:
        console.print(f"[yellow]No results found for '{query}'[/yellow]")
        return

    for item in items:
        table.add_row(item.get("type", ""), item.get("name", ""), item.get("slug", ""))

    console.print(table)


@app.command()
def chip(
    slug: str = typer.Argument(help="Chip slug (e.g. 'ntag213', 'ntag215', 'st25ta02k')"),
) -> None:
    """Look up an NFC chip with full specifications."""
    from nfcfyi.api import NFCFYI

    with NFCFYI() as api:
        data = api.chip(slug)

    console.print(f"\n[bold]{data.get('name', slug)}[/bold]")
    if data.get("description"):
        console.print(f"  {data['description'][:200]}")
    console.print()

    table = Table(title="Specifications")
    table.add_column("Property", style="cyan")
    table.add_column("Value")

    specs = [
        ("Manufacturer", data.get("manufacturer")),
        ("NFC Forum Type", data.get("nfc_forum_type")),
        ("Memory Size", data.get("memory_size")),
        ("User Memory", data.get("user_memory")),
        ("Operating Frequency", data.get("operating_frequency")),
        ("Data Transfer Rate", data.get("data_transfer_rate")),
        ("UID Length", data.get("uid_length")),
        ("ISO Standard", data.get("iso_standard")),
    ]
    for label, value in specs:
        if value is not None:
            table.add_row(label, str(value))

    console.print(table)


@app.command()
def compare(
    slug_a: str = typer.Argument(help="First chip slug"),
    slug_b: str = typer.Argument(help="Second chip slug"),
) -> None:
    """Compare two NFC chips side by side."""
    from nfcfyi.api import NFCFYI

    with NFCFYI() as api:
        data = api.compare(slug_a, slug_b)

    a = data.get("a", {})
    b = data.get("b", {})

    table = Table(title=f"{a.get('name', slug_a)} vs {b.get('name', slug_b)}")
    table.add_column("Property", style="cyan")
    table.add_column(a.get("name", slug_a), style="green")
    table.add_column(b.get("name", slug_b), style="yellow")

    fields = [
        ("Manufacturer", "manufacturer"),
        ("NFC Forum Type", "nfc_forum_type"),
        ("Memory Size", "memory_size"),
        ("User Memory", "user_memory"),
        ("Frequency", "operating_frequency"),
        ("UID Length", "uid_length"),
    ]
    for label, key in fields:
        table.add_row(label, str(a.get(key, "-")), str(b.get(key, "-")))

    console.print(table)


@app.command()
def random() -> None:
    """Discover a random NFC chip."""
    from nfcfyi.api import NFCFYI

    with NFCFYI() as api:
        data = api.random()

    console.print(f"\n[bold]{data.get('name', 'Unknown')}[/bold]")
    if data.get("description"):
        console.print(f"  {data['description'][:200]}")
    console.print(f"  Manufacturer: {data.get('manufacturer', 'N/A')}")
    console.print(f"  NFC Forum Type: {data.get('nfc_forum_type', 'N/A')}")
    console.print(f"  Memory: {data.get('memory_size', 'N/A')}")
    console.print()


if __name__ == "__main__":
    app()
