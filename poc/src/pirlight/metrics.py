"""Bandwidth and privacy-leakage metrics for the three sync tiers."""

from __future__ import annotations

import math


def bandwidth_report(n_blocks: int, block_size: int, k_servers: int = 2) -> dict:
    """Byte/bit costs for retrieving ONE block, per scheme.

    ``download_everything_bytes`` is the only non-PIR way to hide the query
    outright from a single server: fetch the whole chain.
    """
    if n_blocks < 1:
        raise ValueError("n_blocks must be >= 1")
    if block_size < 1:
        raise ValueError("block_size must be >= 1")
    if k_servers < 2:
        raise ValueError("xor_pir needs k_servers >= 2")
    side = math.isqrt(n_blocks)
    if side * side < n_blocks:
        side += 1
    return {
        "n_blocks": n_blocks,
        "block_size": block_size,
        "direct_fetch_bytes": block_size,
        "download_everything_bytes": n_blocks * block_size,
        "xor_pir": {
            "k_servers": k_servers,
            "upload_bits": k_servers * n_blocks,
            "download_bytes": block_size,
        },
        "matrix_pir": {
            "servers": 2,
            "upload_bits": 2 * side,
            "download_bytes": 2 * side * block_size,
        },
    }


def privacy_matrix() -> list[dict]:
    """What each tier hides, as data (single source of truth for docs/demo)."""
    return [
        {
            "tier": "direct (tier 0)",
            "hides_ip": False,
            "hides_query": False,
            "trusted_servers": "1 (operator sees everything)",
        },
        {
            "tier": "tor (tier 1)",
            "hides_ip": True,
            "hides_query": False,
            "trusted_servers": "1 (operator sees queries)",
        },
        {
            "tier": "tor+pir (tier 2)",
            "hides_ip": True,
            "hides_query": True,
            "trusted_servers": "k-1 of k (no single server learns the query)",
        },
    ]
