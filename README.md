# nfcfyi

[![PyPI](https://img.shields.io/pypi/v/nfcfyi)](https://pypi.org/project/nfcfyi/)
[![Python](https://img.shields.io/pypi/pyversions/nfcfyi)](https://pypi.org/project/nfcfyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

NFC chip encyclopedia API client for Python. Look up NFC chips, NDEF record types, operating modes, standards, and contactless use cases from [NFCFYI](https://nfcfyi.com) -- the comprehensive NFC reference covering NFC Forum Tag Types 1-5, ISO 14443 A/B, FeliCa, MIFARE, NTAG, and every major chip family in commercial and industrial use.

> **Explore NFC at [nfcfyi.com](https://nfcfyi.com)** -- [Chip Explorer](https://nfcfyi.com/chip/) | [Standards Reference](https://nfcfyi.com/standard/) | [NDEF Types](https://nfcfyi.com/ndef-type/) | [Use Cases](https://nfcfyi.com/use-case/)

## Install

```bash
pip install nfcfyi[api]     # API client (httpx)
pip install nfcfyi[cli]     # + CLI (typer, rich)
pip install nfcfyi[mcp]     # + MCP server
pip install nfcfyi[all]     # Everything
```

## Quick Start

```python
from nfcfyi.api import NFCFYI

with NFCFYI() as api:
    # Search chips, standards, NDEF types, glossary
    results = api.search("ntag")
    print(results)

    # Look up a specific chip
    ntag215 = api.chip("ntag215")
    print(ntag215["name"], ntag215["memory_size"])

    # Compare two chips
    diff = api.compare("ntag213", "ntag215")
    print(diff)

    # Discover a random chip
    surprise = api.random()
    print(surprise["name"])
```

## What You'll Find on NFCFYI

NFCFYI is a comprehensive NFC chip encyclopedia covering chips, standards, NDEF record types, operating modes, and real-world use cases. Near Field Communication (NFC) is a short-range wireless technology operating at 13.56 MHz that enables contactless data exchange between devices within approximately 4 cm -- the foundation of mobile payments, access control, transit cards, smart posters, and IoT device pairing worldwide.

### NFC Forum Tag Types

The NFC Forum defines five tag types with different memory, speed, and compatibility trade-offs:

| Tag Type | Based On | Memory | Speed | Example Chips |
|----------|----------|--------|-------|---------------|
| Type 1 | ISO 14443A (Topaz) | 96 B - 2 KB | 106 kbps | Broadcom Topaz 512 |
| Type 2 | ISO 14443A | 48 B - 2 KB | 106 kbps | NTAG213, NTAG215, NTAG216 |
| Type 3 | FeliCa (JIS X 6319-4) | Up to 1 MB | 212/424 kbps | Sony FeliCa Lite-S |
| Type 4 | ISO 14443A/B | Up to 32 KB | 106-424 kbps | MIFARE DESFire EV3, ST25TA |
| Type 5 | ISO 15693 (VICC) | Up to 64 KB | 26.48 kbps | ICODE SLIX2, ST25TV |

### NDEF Record Types

NFC Data Exchange Format (NDEF) is the standard message format for NFC tags. Each NDEF message contains one or more records:

| Record Type | TNF | Description |
|-------------|-----|-------------|
| Text | NFC Forum Well Known (0x01) | Plain text with language code (e.g. "en", "ja") |
| URI | NFC Forum Well Known (0x01) | URLs with prefix abbreviation (http://, https://, tel:) |
| Smart Poster | NFC Forum Well Known (0x01) | URI + title + action + icon for interactive posters |
| MIME | Media-type (0x02) | Arbitrary MIME data (vCard, Wi-Fi config, Bluetooth OOB) |
| External | NFC Forum External (0x04) | Custom application-specific records |
| Android Application Record | NFC Forum External (0x04) | Launches specific Android app on tap |

### Operating Modes

NFC devices operate in three primary modes, each serving different interaction patterns:

| Mode | Description | Use Cases |
|------|-------------|-----------|
| Read/Write | Device reads from or writes to a passive NFC tag | Smart posters, product authentication, inventory |
| Card Emulation | Device emulates a contactless smart card | Mobile payments (Apple Pay, Google Pay), transit cards |
| Peer-to-Peer | Two active NFC devices exchange data bidirectionally | Android Beam (deprecated), device pairing, data sharing |

### Key NFC Standards

| Standard | Organization | Scope |
|----------|-------------|-------|
| ISO/IEC 14443 | ISO | Proximity cards -- Type A (MIFARE) and Type B modulation schemes |
| ISO/IEC 15693 | ISO | Vicinity cards -- longer read range (up to 1 m), lower data rate |
| ISO/IEC 18092 (NFCIP-1) | ISO | NFC interface and protocol -- defines active/passive communication |
| JIS X 6319-4 | JISC | FeliCa contactless IC card standard (widely used in Japan) |
| GlobalPlatform | GP | Secure element management for card emulation and mobile payments |
| EMV Contactless | EMVCo | Payment terminal specifications for contactless transactions |

### Chip Families

Major NFC chip product lines from leading manufacturers:

| Family | Manufacturer | Type | Key Feature |
|--------|-------------|------|-------------|
| NTAG 21x | NXP | Type 2 | Most popular, Amiibo (NTAG215), low-cost |
| MIFARE Ultralight | NXP | Type 2 | Transit ticketing, single-ride tokens |
| MIFARE DESFire | NXP | Type 4 | AES-128 crypto, multi-application, high security |
| MIFARE Classic | NXP | Proprietary | Legacy access control, Crypto-1 (broken) |
| ST25TA | STMicroelectronics | Type 4 | Augmented NDEF, tamper detection |
| ST25TV | STMicroelectronics | Type 5 | VICC, long-range, anti-counterfeiting |
| FeliCa | Sony | Type 3 | Suica, PASMO, high-speed transit in Japan |
| ICODE | NXP | Type 5 | Library books, logistics, longer range |

Learn more: [Chip Explorer](https://nfcfyi.com/chip/) | [Standards Reference](https://nfcfyi.com/standard/) | [NDEF Types](https://nfcfyi.com/ndef-type/)

## API Endpoints

Free, no authentication required. JSON responses with CORS enabled.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/chip/{slug}/` | NFC chip detail with specs |
| GET | `/api/chip-family/{slug}/` | Chip family with product line |
| GET | `/api/standard/{slug}/` | Standard detail with linked chips |
| GET | `/api/operating-mode/{slug}/` | Operating mode detail |
| GET | `/api/ndef-type/{slug}/` | NDEF record type detail |
| GET | `/api/use-case/{slug}/` | Use case with recommended chips |
| GET | `/api/term/{slug}/` | Glossary term definition |
| GET | `/api/search/?q={query}` | Search across all content types |
| GET | `/api/compare/?a={slug}&b={slug}` | Compare two chips |
| GET | `/api/random/` | Random chip discovery |
| GET | `/api/openapi.json` | OpenAPI 3.1.0 specification |

```bash
# Example: search for NTAG chips
curl -s "https://nfcfyi.com/api/search/?q=ntag" | python -m json.tool
```

## Command-Line Interface

```bash
nfcfyi search "ntag"
nfcfyi chip ntag215
nfcfyi compare ntag213 ntag215
nfcfyi random
```

## MCP Server (Claude, Cursor, Windsurf)

```json
{
    "mcpServers": {
        "nfcfyi": {
            "command": "python",
            "args": ["-m", "nfcfyi.mcp_server"]
        }
    }
}
```

Tools: `nfc_search`, `nfc_lookup`, `nfc_compare`

## API Client

```python
from nfcfyi.api import NFCFYI

with NFCFYI() as api:
    # All 11 endpoints
    api.search("ntag")
    api.chip("ntag215")
    api.chip_family("ntag-21x")
    api.standard("iso-14443")
    api.operating_mode("read-write")
    api.ndef_type("uri")
    api.use_case("access-control")
    api.glossary_term("ndef")
    api.compare("ntag213", "ntag215")
    api.random()
    api.openapi()
```

## Also Available

| Language | Package | Install |
|----------|---------|---------|
| Python | [nfcfyi](https://pypi.org/project/nfcfyi/) | `pip install nfcfyi` |
| TypeScript | [nfcfyi](https://www.npmjs.com/package/nfcfyi) | `npm install nfcfyi` |
| Go | [nfcfyi-go](https://pkg.go.dev/github.com/fyipedia/nfcfyi-go) | `go get github.com/fyipedia/nfcfyi-go` |
| Rust | [nfcfyi](https://crates.io/crates/nfcfyi) | `cargo add nfcfyi` |
| Ruby | [nfcfyi](https://rubygems.org/gems/nfcfyi) | `gem install nfcfyi` |

## Code FYI Family

| Site | Domain | Focus |
|------|--------|-------|
| BarcodeFYI | [barcodefyi.com](https://barcodefyi.com) | Barcode symbologies & standards |
| QRCodeFYI | [qrcodefyi.com](https://qrcodefyi.com) | QR code types & encoding |
| NFCFYI | [nfcfyi.com](https://nfcfyi.com) | NFC chips & NDEF records |
| BLEFYI | [blefyi.com](https://blefyi.com) | Bluetooth Low Energy profiles |
| RFIDFYI | [rfidfyi.com](https://rfidfyi.com) | RFID tags & frequency bands |
| SmartCardFYI | [smartcardfyi.com](https://smartcardfyi.com) | Smart card types & platforms |

## License

MIT
