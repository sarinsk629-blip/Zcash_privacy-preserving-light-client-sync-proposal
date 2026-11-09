"""Runnable demo: sync one block over all three privacy tiers.

Usage:

    PYTHONPATH=poc/src python -m pirlight.demo
"""

from __future__ import annotations

from .chain import MockChain
from .client import PrivacyTier, SyncClient
from .metrics import bandwidth_report, privacy_matrix


def run_demo(seed: int = 42, target_height: int = 37) -> dict:
    """Sync ``target_height`` via every tier; verify results agree."""
    chain = MockChain(n_blocks=64, block_size=256, seed=seed)
    results = {}
    payloads: set[bytes] = set()
    for tier in PrivacyTier:
        client = SyncClient(chain, tier, seed=seed)
        res = client.sync_block(target_height)
        results[tier.value] = res
        payloads.add(res.block.payload)
    consistent = (
        len(payloads) == 1 and next(iter(payloads)) == chain.block(target_height).payload
    )
    return {
        "target_height": target_height,
        "chain_length": len(chain),
        "results": results,
        "bandwidth": bandwidth_report(len(chain), 256, k_servers=2),
        "privacy": privacy_matrix(),
        "consistent": consistent,
    }


def main() -> None:
    report = run_demo()
    print(
        f"Synced block #{report['target_height']} of a {report['chain_length']}-block"
        f" mock chain over all privacy tiers\n"
    )
    for name in ("direct", "tor", "tor_pir"):
        res = report["results"][name]
        print(
            f"[{name:>8}] observer sees: ip={res.view.client_ip}  "
            f"requested_height={res.view.requested_height}"
        )
    print("\nBandwidth for one private block retrieval (N=64, B=256 bytes):")
    b = report["bandwidth"]
    print(
        f"  download-everything : {b['download_everything_bytes']} bytes"
        f" (perfect privacy vs a single server)"
    )
    print(
        f"  XorPIR   (k=2)      : up {b['xor_pir']['upload_bits']} bits,"
        f" down {b['xor_pir']['download_bytes']} bytes"
    )
    print(
        f"  MatrixPIR (2 srv)   : up {b['matrix_pir']['upload_bits']} bits,"
        f" down {b['matrix_pir']['download_bytes']} bytes"
    )
    print(f"\nAll tiers returned the identical block payload: {report['consistent']}")


if __name__ == "__main__":
    main()
