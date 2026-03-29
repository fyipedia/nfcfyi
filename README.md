# nfcfyi

[![PyPI version](https://agentgif.com/badge/pypi/nfcfyi/version.svg)](https://pypi.org/project/nfcfyi/)
[![Python](https://img.shields.io/pypi/pyversions/nfcfyi)](https://pypi.org/project/nfcfyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

NFC chip encyclopedia API client for Python. Look up NFC chips from NTAG, MIFARE, ST25, FeliCa, and ICODE families, NFC Forum Tag Types 1-5, NDEF record types, operating modes, ISO 14443/15693 standards, and contactless use cases from [NFCFYI](https://nfcfyi.com) -- the comprehensive NFC reference with 288 records covering every major chip family in commercial and industrial use.

Extracted from [NFCFYI](https://nfcfyi.com), an NFC technology platform with 288 records spanning chip specifications, manufacturer product lines, security protocols, frequency bands, and deployment guides used by embedded systems engineers, IoT architects, and mobile payment developers worldwide.

> **Explore NFC at [nfcfyi.com](https://nfcfyi.com)** -- [Chip Explorer](https://nfcfyi.com/chip/) | [Standards Reference](https://nfcfyi.com/standard/) | [NDEF Types](https://nfcfyi.com/ndef-type/) | [Use Cases](https://nfcfyi.com/use-case/)

<p align="center">
  <img src="https://raw.githubusercontent.com/fyipedia/nfcfyi/main/demo.gif" alt="nfcfyi demo -- NFC chip lookup, NDEF type reference, and chip comparison in Python" width="800">
</p>

## Table of Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [What You'll Find on NFCFYI](#what-youll-find-on-nfcfyi)
  - [NFC Forum Tag Types (1-5)](#nfc-forum-tag-types-1-5)
  - [NDEF Record Types](#ndef-record-types)
  - [Operating Modes](#operating-modes)
  - [Chip Families](#chip-families)
  - [NFC vs RFID vs BLE](#nfc-vs-rfid-vs-ble)
  - [Security and Authentication](#security-and-authentication)
  - [Key NFC Standards](#key-nfc-standards)
- [API Endpoints](#api-endpoints)
- [Command-Line Interface](#command-line-interface)
- [MCP Server (Claude, Cursor, Windsurf)](#mcp-server-claude-cursor-windsurf)
- [REST API Client](#rest-api-client)
- [Learn More About NFC](#learn-more-about-nfc)
- [Also Available](#also-available)
- [Tag FYI Family](#tag-fyi-family)
- [FYIPedia Developer Tools](#fyipedia-developer-tools)
- [License](#license)

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

    # Look up a specific NFC chip
    ntag215 = api.chip("ntag215")
    print(ntag215["name"], ntag215["memory_size"])  # NTAG215 504 bytes

    # Compare two NFC chips side-by-side
    diff = api.compare("ntag213", "ntag215")
    print(diff)

    # Discover a random chip
    surprise = api.random()
    print(surprise["name"])
```

## What You'll Find on NFCFYI

NFCFYI is a comprehensive NFC chip encyclopedia covering chips, standards, NDEF record types, operating modes, and real-world use cases. Near Field Communication (NFC) is a short-range wireless technology operating at 13.56 MHz that enables contactless data exchange between devices within approximately 4 cm -- the foundation of mobile payments (Apple Pay, Google Pay), transit cards (Suica, Oyster), access control, smart posters, product authentication, and IoT device pairing worldwide.

### NFC Forum Tag Types (1-5)

The NFC Forum defines five standardized tag types with different memory, speed, and compatibility trade-offs. Each type maps to an underlying ISO standard and radio modulation scheme:

| Tag Type | Based On | Memory | Speed | Read/Write | Example Chips |
|----------|----------|--------|-------|------------|---------------|
| Type 1 | ISO 14443A (Topaz) | 96 B - 2 KB | 106 kbps | R/W or read-only | Broadcom Topaz 512 |
| Type 2 | ISO 14443A | 48 B - 2 KB | 106 kbps | R/W or read-only | NTAG213, NTAG215, NTAG216 |
| Type 3 | FeliCa (JIS X 6319-4) | Up to 1 MB | 212/424 kbps | R/W or read-only | Sony FeliCa Lite-S, RC-S967 |
| Type 4 | ISO 14443A/B | Up to 32 KB | 106-424 kbps | R/W or read-only | MIFARE DESFire EV3, ST25TA |
| Type 5 | ISO 15693 (VICC) | Up to 64 KB | 26.48 kbps | R/W or read-only | ICODE SLIX2, ST25TV |

**Type 2 dominance**: NTAG 21x chips (Type 2) dominate consumer NFC applications due to low cost ($0.05-0.15 per tag), reliable 106 kbps communication, and broad smartphone compatibility. NTAG213 (144 bytes) suits URLs and small records, NTAG215 (504 bytes) is used for Nintendo Amiibo figures, and NTAG216 (888 bytes) handles vCards and multi-record NDEF messages.

**Type 4 for security**: MIFARE DESFire EV3 (Type 4) provides AES-128 encryption, mutual authentication, and up to 8 independent applications on a single card -- the standard for corporate access control, transit systems, and government identity programs requiring tamper-resistant credential storage.

Learn more: [Chip Explorer](https://nfcfyi.com/chip/) | [Glossary](https://nfcfyi.com/glossary/)

### NDEF Record Types

NFC Data Exchange Format (NDEF) is the standard message format for NFC tags. Each NDEF message contains one or more records, identified by a Type Name Format (TNF) field and a record type:

| Record Type | TNF | Type String | Description |
|-------------|-----|-------------|-------------|
| Text | 0x01 (Well Known) | T | Plain text with language code (e.g. "en", "ja") |
| URI | 0x01 (Well Known) | U | URLs with prefix abbreviation (0x01=http://www., 0x02=https://www.) |
| Smart Poster | 0x01 (Well Known) | Sp | URI + title + action + icon for interactive posters |
| Handover Select | 0x01 (Well Known) | Hs | Bluetooth/Wi-Fi handover negotiation |
| MIME | 0x02 (Media-type) | varies | vCard (text/vcard), Wi-Fi config, Bluetooth OOB |
| External | 0x04 (External) | varies | Custom application-specific records |
| Android App Record | 0x04 (External) | android.com:pkg | Launches specific Android app on tap |

**URI prefix abbreviation**: The NDEF URI record type compresses common URL prefixes into a single byte -- `0x01` for `http://www.`, `0x02` for `https://www.`, `0x03` for `http://`, `0x04` for `https://`, and 30+ other prefixes including `tel:`, `mailto:`, and `ftp://`. This saves 7-15 bytes per record, critical for memory-constrained Type 2 tags.

Learn more: [NDEF Types](https://nfcfyi.com/ndef-type/) | [Use Cases](https://nfcfyi.com/use-case/)

### Operating Modes

NFC devices operate in three primary modes, each serving different interaction patterns:

| Mode | Device Role | Initiator | Use Cases |
|------|-------------|-----------|-----------|
| Read/Write | Active reader + passive tag | Reader | Smart posters, product authentication, inventory |
| Card Emulation | Device emulates passive card | External reader | Apple Pay, Google Pay, transit cards, access control |
| Peer-to-Peer | Two active devices | Either | Android Beam (deprecated), device pairing, data sharing |

**Host Card Emulation (HCE)**: Android 4.4+ introduced HCE, allowing apps to emulate NFC cards without a hardware Secure Element. HCE routes APDU commands from the NFC controller directly to an Android service, enabling cloud-based payment tokens and custom card emulation applications. Apple restricts card emulation to Apple Pay via the Secure Enclave.

### Chip Families

Major NFC chip product lines from leading manufacturers:

| Family | Manufacturer | Tag Type | Memory Range | Key Feature |
|--------|-------------|----------|-------------|-------------|
| NTAG 21x | NXP | Type 2 | 144-888 bytes | Most popular, Amiibo (NTAG215), low-cost |
| NTAG I2C | NXP | Type 2 | 1-2 KB | I2C interface for MCU bridging |
| MIFARE Ultralight | NXP | Type 2 | 64-192 bytes | Transit ticketing, single-ride tokens |
| MIFARE DESFire | NXP | Type 4 | 2-8 KB | AES-128 crypto, multi-application |
| MIFARE Classic | NXP | Proprietary | 1-4 KB | Legacy access control, Crypto-1 (broken) |
| ST25TA | STMicroelectronics | Type 4 | 256 B - 64 KB | Augmented NDEF, tamper detection |
| ST25TV | STMicroelectronics | Type 5 | 256 B - 64 KB | VICC, long-range, anti-counterfeiting |
| FeliCa | Sony | Type 3 | Up to 1 MB | Suica, PASMO, high-speed 424 kbps transit |
| ICODE | NXP | Type 5 | 128 B - 8 KB | Library books, logistics, longer range |

**MIFARE Classic vulnerability**: MIFARE Classic's proprietary Crypto-1 cipher was reverse-engineered in 2008. The key recovery attack (MFOC/MFCUK) can extract all sector keys in seconds. New deployments should use MIFARE DESFire EV3 or NTAG 424 DNA with AES-128 authentication.

Learn more: [Chip Explorer](https://nfcfyi.com/chip/) | [Standards Reference](https://nfcfyi.com/standard/)

### NFC vs RFID vs BLE

| Feature | NFC (13.56 MHz) | HF RFID (13.56 MHz) | UHF RFID (860-960 MHz) | BLE |
|---------|-----------------|---------------------|----------------------|-----|
| Range | ~4 cm | ~1 m | 1-12 m | 10-100 m |
| Frequency | 13.56 MHz | 13.56 MHz | 860-960 MHz | 2.4 GHz |
| Power Source | Reader field | Reader field | Reader field | Battery |
| Data Rate | 106-424 kbps | 26-424 kbps | 40-640 kbps | 1-2 Mbps |
| Standards | ISO 14443, 18092 | ISO 14443, 15693 | ISO 18000-63, EPC Gen2 | Bluetooth 4.0-5.4 |
| Bidirectional | Yes (peer-to-peer) | Limited | No (backscatter only) | Yes |
| Phone Support | Native (iOS/Android) | Requires external reader | Requires external reader | Native |

### Security and Authentication

Modern NFC chips implement multiple security layers for product authentication, access control, and payment applications:

| Feature | NTAG 213/215/216 | NTAG 424 DNA | MIFARE DESFire EV3 |
|---------|------------------|--------------|---------------------|
| Password Protection | 32-bit password | AES-128 | AES-128/192/256 |
| Dynamic URL (SUN) | No | Yes (per-tap counter) | No |
| Mutual Authentication | No | Yes (LRP protocol) | Yes (EV2/EV3 auth) |
| Message Authentication | No | CMAC (AES) | CMAC (AES) |
| Originality Signature | ECDSA | ECDSA | ECDSA |
| Applications | 1 | 1 | Up to 8 independent apps |

**NTAG 424 DNA** (DNA = Digital NFC Authentication) generates a unique encrypted URL on every tap, enabling cloud-based product authentication without specialized readers. Each tap increments a counter and produces a fresh AES-CMAC signature, making cloning practically impossible.

### Key NFC Standards

| Standard | Organization | Scope |
|----------|-------------|-------|
| ISO/IEC 14443 A/B | ISO | Proximity cards -- modulation, anti-collision, transmission |
| ISO/IEC 15693 | ISO | Vicinity cards -- longer read range, lower data rate |
| ISO/IEC 18092 (NFCIP-1) | ISO | NFC interface and protocol -- active/passive communication |
| ISO/IEC 21481 (NFCIP-2) | ISO | NFC operating mode selection |
| JIS X 6319-4 | JISC | FeliCa contactless IC card standard |
| GlobalPlatform | GP | Secure element management for card emulation |
| EMV Contactless (Books A-D) | EMVCo | Contactless payment terminal specifications |

Learn more: [Standards Reference](https://nfcfyi.com/standard/) | [Glossary](https://nfcfyi.com/glossary/)

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

### Example

```bash
# Search for NTAG chips
curl -s "https://nfcfyi.com/api/search/?q=ntag" | python -m json.tool
```

Full API documentation at [nfcfyi.com/api/](https://nfcfyi.com/api/).
OpenAPI 3.1.0 spec: [nfcfyi.com/api/openapi.json](https://nfcfyi.com/api/openapi.json).

## Command-Line Interface

```bash
nfcfyi search "ntag"                  # Search all content
nfcfyi chip ntag215                   # Chip detail
nfcfyi compare ntag213 ntag215        # Side-by-side comparison
nfcfyi random                         # Discover a random chip
```

## MCP Server (Claude, Cursor, Windsurf)

```json
{
    "mcpServers": {
        "nfcfyi": {
            "command": "uvx",
            "args": ["--from", "nfcfyi[mcp]", "python", "-m", "nfcfyi.mcp_server"]
        }
    }
}
```

Tools: `nfc_search`, `nfc_lookup`, `nfc_compare`

## REST API Client

```python
from nfcfyi.api import NFCFYI

with NFCFYI() as api:
    api.search("ntag")                     # Full-text search
    api.chip("ntag215")                    # Chip detail
    api.chip_family("ntag-21x")            # Chip family
    api.standard("iso-14443")              # Standard detail
    api.operating_mode("read-write")       # Operating mode
    api.ndef_type("uri")                   # NDEF record type
    api.use_case("access-control")         # Use case
    api.glossary_term("ndef")              # Glossary term
    api.compare("ntag213", "ntag215")      # Compare two chips
    api.random()                           # Random discovery
    api.openapi()                          # OpenAPI 3.1.0 spec
```

## Learn More About NFC

- **Browse**: [Chip Explorer](https://nfcfyi.com/chip/) · [NDEF Types](https://nfcfyi.com/ndef-type/) · [Use Cases](https://nfcfyi.com/use-case/)
- **Reference**: [Standards](https://nfcfyi.com/standard/) · [Operating Modes](https://nfcfyi.com/operating-mode/) · [Glossary](https://nfcfyi.com/glossary/)
- **API**: [REST API Docs](https://nfcfyi.com/api/) · [OpenAPI Spec](https://nfcfyi.com/api/openapi.json)

## Also Available

| Platform | Install | Link |
|----------|---------|------|
| **npm** | `npm install nfcfyi` | [npm](https://www.npmjs.com/package/nfcfyi) |
| **Go** | `go get github.com/fyipedia/nfcfyi-go` | [pkg.go.dev](https://pkg.go.dev/github.com/fyipedia/nfcfyi-go) |
| **Rust** | `cargo add nfcfyi` | [crates.io](https://crates.io/crates/nfcfyi) |
| **Ruby** | `gem install nfcfyi` | [rubygems.org](https://rubygems.org/gems/nfcfyi) |
| **MCP** | `uvx --from "nfcfyi[mcp]" python -m nfcfyi.mcp_server` | [Config](#mcp-server-claude-cursor-windsurf) |

## Tag FYI Family

Part of the [FYIPedia](https://fyipedia.com) open-source developer tools ecosystem -- automatic identification and data capture technologies.

| Site | Domain | Focus |
|------|--------|-------|
| BarcodeFYI | [barcodefyi.com](https://barcodefyi.com) | 518 records -- barcode symbologies, standards, GS1 prefixes |
| QRCodeFYI | [qrcodefyi.com](https://qrcodefyi.com) | 425 records -- QR code types, versions, encoding modes |
| **NFCFYI** | [nfcfyi.com](https://nfcfyi.com) | **288 records -- NFC chips, NDEF records, standards** |
| BLEFYI | [blefyi.com](https://blefyi.com) | 261 records -- BLE chips, GATT profiles, beacons |
| RFIDFYI | [rfidfyi.com](https://rfidfyi.com) | 318 records -- RFID tags, frequency bands, EPC schemes |
| SmartCardFYI | [smartcardfyi.com](https://smartcardfyi.com) | 280 records -- smart cards, EMV, Java Card, platforms |

## FYIPedia Developer Tools

| Package | PyPI | npm | Description |
|---------|------|-----|-------------|
| barcodefyi | [PyPI](https://pypi.org/project/barcodefyi/) | [npm](https://www.npmjs.com/package/barcodefyi) | Barcode symbologies, standards -- [barcodefyi.com](https://barcodefyi.com) |
| qrcodefyi | [PyPI](https://pypi.org/project/qrcodefyi/) | [npm](https://www.npmjs.com/package/qrcodefyi) | QR code types, versions, encoding -- [qrcodefyi.com](https://qrcodefyi.com) |
| **nfcfyi** | [PyPI](https://pypi.org/project/nfcfyi/) | [npm](https://www.npmjs.com/package/nfcfyi) | **NFC chips, NDEF, standards -- [nfcfyi.com](https://nfcfyi.com)** |
| blefyi | [PyPI](https://pypi.org/project/blefyi/) | [npm](https://www.npmjs.com/package/blefyi) | BLE profiles, beacons, chips -- [blefyi.com](https://blefyi.com) |
| rfidfyi | [PyPI](https://pypi.org/project/rfidfyi/) | [npm](https://www.npmjs.com/package/rfidfyi) | RFID tags, readers, frequencies -- [rfidfyi.com](https://rfidfyi.com) |
| smartcardfyi | [PyPI](https://pypi.org/project/smartcardfyi/) | [npm](https://www.npmjs.com/package/smartcardfyi) | Smart cards, EMV, platforms -- [smartcardfyi.com](https://smartcardfyi.com) |

## Embed Widget

Embed [NFCFYI](https://nfcfyi.com) widgets on any website with [nfcfyi-embed](https://widget.nfcfyi.com):

```html
<script src="https://cdn.jsdelivr.net/npm/nfcfyi-embed@1/dist/embed.min.js"></script>
<div data-nfcfyi="entity" data-slug="example"></div>
```

Zero dependencies · Shadow DOM · 4 themes (light/dark/sepia/auto) · [Widget docs](https://widget.nfcfyi.com)

## License

MIT
