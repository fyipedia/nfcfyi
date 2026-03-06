"""Tests for nfcfyi API client."""

from __future__ import annotations

from nfcfyi.api import NFCFYI


def test_client_init() -> None:
    client = NFCFYI()
    assert client._client.base_url == "https://nfcfyi.com"
    client.close()


def test_client_custom_base_url() -> None:
    client = NFCFYI(base_url="https://test.example.com")
    assert client._client.base_url == "https://test.example.com"
    client.close()


def test_client_context_manager() -> None:
    with NFCFYI() as api:
        assert api._client.base_url == "https://nfcfyi.com"


def test_version() -> None:
    from nfcfyi import __version__

    assert __version__ == "0.1.0"
