"""Tests for the PIR schemes: correctness + the privacy property."""

from __future__ import annotations

import random

import pytest

from pirlight.pir import (
    MatrixPIRClient,
    MatrixPIRServer,
    XorPIRClient,
    XorPIRServer,
    next_square,
    pad_to_square,
    xor_bytes,
)


def make_db(rng: random.Random, n: int = 32, size: int = 16) -> list[bytes]:
    return [bytes(rng.randrange(256) for _ in range(size)) for _ in range(n)]


class TestHelpers:
    def test_xor_bytes(self) -> None:
        assert xor_bytes(b"\x00\xff", b"\xff\x0f") == b"\xff\xf0"

    def test_xor_bytes_length_mismatch(self) -> None:
        with pytest.raises(ValueError):
            xor_bytes(b"\x00", b"\x00\x00")

    def test_next_square(self) -> None:
        assert next_square(1) == 1
        assert next_square(2) == 2
        assert next_square(16) == 4
        assert next_square(17) == 5
        assert next_square(50) == 8

    def test_pad_to_square(self) -> None:
        rng = random.Random(99)
        db = make_db(rng, n=50, size=8)
        padded, side = pad_to_square(db)
        assert side == 8
        assert len(padded) == 64
        assert padded[:50] == db
        assert padded[50:] == [bytes(8)] * 14

    def test_pad_to_square_rejects_ragged(self) -> None:
        with pytest.raises(ValueError):
            pad_to_square([b"a", b"bb"])


class TestXorPIR:
    @pytest.mark.parametrize("k", [2, 3, 4])
    def test_retrieves_correct_block(self, k: int) -> None:
        rng = random.Random(1)
        db = make_db(rng, n=32)
        servers = [XorPIRServer(db) for _ in range(k)]
        client = XorPIRClient(servers, random.Random(2))
        for i in (0, 5, 17, 31):
            assert client.retrieve(i) == db[i]

    def test_rejects_single_server(self) -> None:
        rng = random.Random(1)
        db = make_db(rng, n=8)
        with pytest.raises(ValueError):
            XorPIRClient([XorPIRServer(db)], random.Random(2))

    def test_rejects_bad_index(self) -> None:
        rng = random.Random(1)
        db = make_db(rng, n=8)
        client = XorPIRClient([XorPIRServer(db), XorPIRServer(db)], random.Random(2))
        with pytest.raises(IndexError):
            client.retrieve(8)

    def test_queries_xor_to_unit_vector(self) -> None:
        rng = random.Random(5)
        db = make_db(rng, n=16)
        client = XorPIRClient(
            [XorPIRServer(db), XorPIRServer(db), XorPIRServer(db)], random.Random(6)
        )
        for i in range(16):
            queries = client.build_queries(i)
            acc = [0] * 16
            for q in queries:
                acc = [a ^ b for a, b in zip(acc, q)]
            assert acc == [1 if t == i else 0 for t in range(16)]

    def test_per_server_query_uniformity(self) -> None:
        """Privacy core: each server's selector is uniform regardless of index.

        Statistical check over ~2k samples; the bound is deliberately generous
        so the test is stable, while still catching any index-dependent bias.
        """
        rng = random.Random(3)
        db = make_db(rng, n=64)
        servers = [XorPIRServer(db), XorPIRServer(db)]
        client = XorPIRClient(servers, random.Random(4))
        ones = 0
        total = 0
        for i in range(64):
            for _ in range(30):
                queries = client.build_queries(i)
                ones += sum(queries[0])
                total += len(queries[0])
        assert abs(ones / total - 0.5) < 0.05

    def test_rejects_ragged_db(self) -> None:
        with pytest.raises(ValueError):
            XorPIRServer([b"a", b"bb"])


class TestMatrixPIR:
    def test_square_db_retrieval(self) -> None:
        rng = random.Random(11)
        db = make_db(rng, n=64)
        padded, side = pad_to_square(db)
        server1 = MatrixPIRServer(padded, side, side)
        server2 = MatrixPIRServer(padded, side, side)
        client = MatrixPIRClient(db, random.Random(12))
        for i in (0, 7, 9, 63):
            assert client.retrieve(i, server1, server2) == db[i]

    def test_padded_db_retrieval(self) -> None:
        rng = random.Random(13)
        db = make_db(rng, n=50)
        padded, side = pad_to_square(db)
        server1 = MatrixPIRServer(padded, side, side)
        server2 = MatrixPIRServer(padded, side, side)
        client = MatrixPIRClient(db, random.Random(14))
        for i in range(len(db)):
            assert client.retrieve(i, server1, server2) == db[i]

    def test_rejects_bad_index(self) -> None:
        rng = random.Random(15)
        db = make_db(rng, n=50)
        client = MatrixPIRClient(db, random.Random(16))
        with pytest.raises(IndexError):
            client.build_queries(50)

    def test_selector_uniformity(self) -> None:
        """Each server's row selector is uniform regardless of the target row."""
        rng = random.Random(17)
        db = make_db(rng, n=64)
        client = MatrixPIRClient(db, random.Random(18))
        ones = 0
        total = 0
        for i in range(64):
            for _ in range(25):
                selector1, selector2 = client.build_queries(i)
                ones += sum(selector2)
                total += len(selector2)
        assert abs(ones / total - 0.5) < 0.05

    def test_bandwidth_advantage_over_download_all(self) -> None:
        rng = random.Random(19)
        db = make_db(rng, n=64, size=256)
        padded, side = pad_to_square(db)
        server = MatrixPIRServer(padded, side, side)
        client = MatrixPIRClient(db, random.Random(20))
        selector1, selector2 = client.build_queries(0)
        answer1 = server.answer(selector1)
        answer2 = server.answer(selector2)
        download = sum(len(b) for b in answer1) + sum(len(b) for b in answer2)
        assert download == 2 * side * 256
        assert download < 64 * 256

    def test_server_validation(self) -> None:
        rng = random.Random(21)
        db = make_db(rng, n=8)
        with pytest.raises(ValueError):
            MatrixPIRServer(db, 2, 3)
        with pytest.raises(ValueError):
            MatrixPIRServer(db, 4, 4)
