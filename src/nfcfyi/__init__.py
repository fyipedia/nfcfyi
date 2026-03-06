"""nfcfyi — NFC chip encyclopedia API client for developers.

Look up NFC chips, NDEF record types, operating modes, standards, and use cases from NFCFYI.

Usage::

    from nfcfyi.api import NFCFYI

    with NFCFYI() as api:
        results = api.search("ntag")
        print(results)
"""

__version__ = "0.1.0"
