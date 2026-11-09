"""Deterministic mock compact-block chain for the PoC (no network calls).

Blocks have fixed-size payloads so that PIR servers can enforce a uniform
database shape. The chain is fully deterministic given a seed.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import random


@dataclass(frozen=True)
class CompactBlock:
    """A stand-in for a lightwalletd compact block."""

    height: int
    block_hash: str
    txids: tuple[str, ...]
    payload: bytes

    @property
    def size(self) -> int:
        return len(self.payload)


class MockChain:
    """Builds a deterministic mock compact-block chain."""

    def __init__(
        self,
        n_blocks: int = 64,
        block_size: int = 256,
        tx_per_block: int = 3,
        seed: int = 42,
    ) -> None:
        if n_blocks <= 0:
            raise ValueError("n_blocks must be positive")
        if block_size <= 0:
            raise ValueError("block_size must be positive")
        rng = random.Random(seed)
        self._blocks: list[CompactBlock] = []
        for height in range(n_blocks):
            digest = hashlib.sha256(f"block-{seed}-{height}".encode()).hexdigest()
            txids = tuple(
                hashlib.sha256(f"tx-{seed}-{height}-{t}".encode()).hexdigest()[:16]
                for t in range(tx_per_block)
            )
            payload = bytes(rng.randrange(256) for _ in range(block_size))
            self._blocks.append(
                CompactBlock(height=height, block_hash=digest[:16], txids=txids, payload=payload)
            )

    def __len__(self) -> int:
        return len(self._blocks)

    def block(self, height: int) -> CompactBlock:
        if not 0 <= height < len(self._blocks):
            raise IndexError(f"height {height} out of range [0, {len(self._blocks)})")
        return self._blocks[height]

    def heights(self) -> list[int]:
        return [b.height for b in self._blocks]
