"""Multi-server Private Information Retrieval (PIR) — reference implementations.

Both schemes provide *information-theoretic* privacy against each individual
(non-colluding) server: the query any single server receives is uniformly
random and independent of the block the client retrieves.

* ``XorPIR``    — k-server scheme (Chor et al. style).
                  Upload O(k*N) bits, download O(|B|) bytes per retrieval.
* ``MatrixPIR`` — 2-server scheme over a sqrt(N) x sqrt(N) block matrix.
                  Upload O(sqrt(N)) bits, download O(sqrt(N) * |B|) bytes.
"""

from __future__ import annotations

import math
import random
from collections.abc import Sequence


def xor_bytes(a: bytes, b: bytes) -> bytes:
    """Element-wise XOR of two equal-length byte strings."""
    if len(a) != len(b):
        raise ValueError(f"length mismatch: {len(a)} != {len(b)}")
    return bytes(x ^ y for x, y in zip(a, b))


def _validate_db(db: Sequence[bytes]) -> list[bytes]:
    """Normalize a block list and enforce the uniform-size invariant."""
    blocks = [bytes(b) for b in db]
    if len(blocks) < 2:
        raise ValueError("database needs at least 2 blocks")
    sizes = {len(b) for b in blocks}
    if len(sizes) != 1:
        raise ValueError(f"blocks must be uniform size, got sizes {sorted(sizes)}")
    return blocks


def next_square(n: int) -> int:
    """Side length of the smallest perfect square >= n."""
    if n < 1:
        raise ValueError("n must be >= 1")
    side = math.isqrt(n)
    if side * side < n:
        side += 1
    return side


def pad_to_square(db: Sequence[bytes]) -> tuple[list[bytes], int]:
    """Pad a block list with zero blocks up to the next perfect square.

    Returns (padded_blocks, side). Padding is transparent: clients never
    request padded indices.
    """
    blocks = _validate_db(db)
    side = next_square(len(blocks))
    pad = side * side - len(blocks)
    return blocks + [bytes(len(blocks[0]))] * pad, side


class XorPIRServer:
    """One PIR server over the database; answers 0/1 selector vectors."""

    def __init__(self, db: Sequence[bytes]) -> None:
        self._db = _validate_db(db)

    @property
    def size(self) -> int:
        return len(self._db)

    @property
    def block_size(self) -> int:
        return len(self._db[0])

    def answer(self, selector: Sequence[int]) -> bytes:
        """XOR of all blocks whose selector bit is 1."""
        selector = list(selector)
        if len(selector) != self.size:
            raise ValueError(f"selector length {len(selector)} != db size {self.size}")
        out = bytes(self.block_size)
        for bit, block in zip(selector, self._db):
            if bit:
                out = xor_bytes(out, block)
        return out


class XorPIRClient:
    """Retrieves blocks from >= 2 :class:`XorPIRServer` instances privately."""

    def __init__(self, servers: Sequence[XorPIRServer], rng: random.Random) -> None:
        servers = list(servers)
        if len(servers) < 2:
            raise ValueError("multi-server PIR requires at least 2 servers")
        size = servers[0].size
        if any(s.size != size for s in servers):
            raise ValueError("all servers must hold the same database shape")
        self._servers = servers
        self._rng = rng
        self._n = size

    @property
    def n(self) -> int:
        return self._n

    def build_queries(self, index: int) -> list[list[int]]:
        """k selector vectors whose XOR is the unit vector at ``index``."""
        if not 0 <= index < self._n:
            raise IndexError(f"index {index} out of range [0, {self._n})")
        unit = [1 if t == index else 0 for t in range(self._n)]
        acc = [0] * self._n
        queries: list[list[int]] = []
        for _ in range(len(self._servers) - 1):
            v = [self._rng.randrange(2) for _ in range(self._n)]
            queries.append(v)
            acc = [a ^ b for a, b in zip(acc, v)]
        queries.append([a ^ u for a, u in zip(acc, unit)])
        return queries

    def retrieve(self, index: int) -> bytes:
        """Retrieve db[index] without any single server learning the index."""
        queries = self.build_queries(index)
        answers = [server.answer(q) for server, q in zip(self._servers, queries)]
        out = answers[0]
        for a in answers[1:]:
            out = xor_bytes(out, a)
        return out


class MatrixPIRServer:
    """Holds the database as a rows x cols matrix of uniform-size blocks.

    ``answer(selector)`` returns, for every column, the element-wise XOR of
    the blocks in the selected rows — a list of ``cols`` blocks.
    """

    def __init__(self, db: Sequence[bytes], rows: int, cols: int) -> None:
        blocks = [bytes(b) for b in db]
        if rows * cols != len(blocks):
            raise ValueError(f"rows*cols ({rows}*{cols}) must equal db size ({len(blocks)})")
        sizes = {len(b) for b in blocks}
        if len(sizes) != 1:
            raise ValueError(f"blocks must be uniform size, got sizes {sorted(sizes)}")
        self._rows, self._cols = rows, cols
        self._block_size = len(blocks[0])
        self._matrix = [[blocks[r * cols + c] for c in range(cols)] for r in range(rows)]

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def cols(self) -> int:
        return self._cols

    @property
    def block_size(self) -> int:
        return self._block_size

    def answer(self, selector: Sequence[int]) -> list[bytes]:
        """Element-wise XOR of the selected rows (one block per column)."""
        selector = list(selector)
        if len(selector) != self._rows:
            raise ValueError(f"selector length {len(selector)} != rows {self._rows}")
        out = [bytes(self._block_size) for _ in range(self._cols)]
        for bit, row in zip(selector, self._matrix):
            if bit:
                out = [xor_bytes(acc, block) for acc, block in zip(out, row)]
        return out


class MatrixPIRClient:
    """Two-server retrieval with O(sqrt(N)) upload and O(sqrt(N)*|B|) download.

    The database is laid out as a side x side matrix (padded with zero blocks
    to a square when needed). Client wants block (r, c); it sends a uniform
    selector ``s`` to server 2 and ``s XOR e_r`` to server 1. Each server's
    selector is uniform regardless of the target row — one-time-pad argument.
    """

    def __init__(self, db: Sequence[bytes], rng: random.Random) -> None:
        _, side = pad_to_square(db)
        self._side = side
        self._n_original = len(db)
        self._rng = rng

    @property
    def n(self) -> int:
        return self._n_original

    @property
    def side(self) -> int:
        return self._side

    def build_queries(self, index: int) -> tuple[list[int], list[int]]:
        """Return (selector_for_server1, selector_for_server2)."""
        if not 0 <= index < self._n_original:
            raise IndexError(f"index {index} out of range [0, {self._n_original})")
        r = index // self._side
        secret = [self._rng.randrange(2) for _ in range(self._side)]
        selector1 = [s ^ (1 if i == r else 0) for i, s in enumerate(secret)]
        return selector1, secret

    def combine(self, index: int, answer1: list[bytes], answer2: list[bytes]) -> bytes:
        """Combine both servers' answers into the requested block."""
        c = index % self._side
        return xor_bytes(answer1[c], answer2[c])

    def retrieve(self, index: int, server1: MatrixPIRServer, server2: MatrixPIRServer) -> bytes:
        """Convenience end-to-end retrieval against two servers."""
        selector1, selector2 = self.build_queries(index)
        answer1 = server1.answer(selector1)
        answer2 = server2.answer(selector2)
        return self.combine(index, answer1, answer2)
