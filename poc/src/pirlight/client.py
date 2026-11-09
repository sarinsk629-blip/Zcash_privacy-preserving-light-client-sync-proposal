"""Tiered privacy sync client against a mock chain (simulated network).

No real sockets are used anywhere: this module models *what an observer would
learn* under each privacy tier. The tiers:

* ``DIRECT``  — plain gRPC sync (status quo). Operator sees IP + requested heights.
* ``TOR``     — onion-routed sync. Operator sees requested heights, not the IP.
* ``TOR_PIR`` — onion-routed multi-server PIR. Operator sees neither.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import random
from typing import Any

from .chain import CompactBlock, MockChain
from .pir import MatrixPIRClient, MatrixPIRServer, pad_to_square


class PrivacyTier(str, Enum):
    """Privacy level of the sync transport."""

    DIRECT = "direct"
    TOR = "tor"
    TOR_PIR = "tor_pir"


class TorCircuit:
    """Simulated Tor circuit: replaces the client IP with an onion alias."""

    def __init__(self, rng: random.Random) -> None:
        self.circuit_id = rng.randrange(16**8)

    def mask(self, ip: str) -> str:
        """Return the observer-visible source for traffic on this circuit."""
        return f"onion:{self.circuit_id:08x}"


@dataclass
class ObserverView:
    """What the sync infrastructure records about one sync operation."""

    client_ip: str | None
    requested_height: int | None
    records: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class SyncResult:
    """Outcome of one block sync, with observer metadata and byte counts."""

    tier: PrivacyTier
    block: CompactBlock
    view: ObserverView
    upload_bits: int = 0
    download_bytes: int = 0


class SyncClient:
    """Syncs single blocks from a :class:`MockChain` at a chosen privacy tier."""

    def __init__(
        self,
        chain: MockChain,
        tier: PrivacyTier | str,
        ip: str = "203.0.113.7",
        seed: int = 7,
    ) -> None:
        if len(chain) < 2:
            raise ValueError("chain needs at least 2 blocks")
        self.chain = chain
        self.tier = PrivacyTier(tier)
        self.ip = ip
        self._rng = random.Random(seed)
        self._tor = TorCircuit(self._rng)
        self._pir: MatrixPIRClient | None = None
        self._pir_servers: tuple[MatrixPIRServer, MatrixPIRServer] | None = None
        if self.tier is PrivacyTier.TOR_PIR:
            db = [chain.block(h).payload for h in chain.heights()]
            # Servers must hold the padded database; the client applies the
            # identical padding internally (same db -> same pad -> same layout).
            padded, side = pad_to_square(db)
            pir = MatrixPIRClient(db, self._rng)
            self._pir = pir
            self._pir_servers = (
                MatrixPIRServer(padded, side, side),
                MatrixPIRServer(padded, side, side),
            )

    def sync_block(self, height: int) -> SyncResult:
        """Fetch one block; returns the block plus what observers learned."""
        if not 0 <= height < len(self.chain):
            raise IndexError(f"height {height} out of range [0, {len(self.chain)})")
        if self.tier is PrivacyTier.DIRECT:
            return self._sync_direct(height)
        if self.tier is PrivacyTier.TOR:
            return self._sync_tor(height)
        return self._sync_tor_pir(height)

    def _sync_direct(self, height: int) -> SyncResult:
        block = self.chain.block(height)
        view = ObserverView(client_ip=self.ip, requested_height=height)
        view.records.append(
            {"observer": "lightwalletd", "client_ip": self.ip, "requested_height": height}
        )
        return SyncResult(self.tier, block, view, upload_bits=16, download_bytes=block.size)

    def _sync_tor(self, height: int) -> SyncResult:
        block = self.chain.block(height)
        masked = self._tor.mask(self.ip)
        view = ObserverView(client_ip=masked, requested_height=height)
        view.records.append(
            {"observer": "lightwalletd-onion", "client_ip": masked, "requested_height": height}
        )
        return SyncResult(self.tier, block, view, upload_bits=16, download_bytes=block.size)

    def _sync_tor_pir(self, height: int) -> SyncResult:
        assert self._pir is not None and self._pir_servers is not None
        server1, server2 = self._pir_servers
        masked = self._tor.mask(self.ip)
        selector1, selector2 = self._pir.build_queries(height)
        answer1 = server1.answer(selector1)
        answer2 = server2.answer(selector2)
        payload = self._pir.combine(height, answer1, answer2)
        view = ObserverView(client_ip=masked, requested_height=None)
        for j, selector in ((1, selector1), (2, selector2)):
            view.records.append(
                {
                    "observer": f"pir-node-{j}",
                    "client_ip": masked,
                    "requested_height": None,
                    "selector": f"opaque:{sum(selector)}/{len(selector)} bits set (random)",
                }
            )
        source = self.chain.block(height)
        side = self._pir.side
        retrieved = CompactBlock(
            height=height,
            block_hash=source.block_hash,
            txids=source.txids,
            payload=payload,
        )
        return SyncResult(
            self.tier,
            retrieved,
            view,
            upload_bits=2 * side,
            download_bytes=2 * side * source.size,
        )
