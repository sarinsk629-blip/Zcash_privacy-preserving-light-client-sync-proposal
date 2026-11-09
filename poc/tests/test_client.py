"""Tests for the tiered sync client, the mock chain, and the demo."""

from __future__ import annotations

import pytest

from pirlight.chain import MockChain
from pirlight.client import PrivacyTier, SyncClient
from pirlight.demo import run_demo
from pirlight.metrics import bandwidth_report, privacy_matrix


class TestMockChain:
    def test_deterministic(self) -> None:
        a = MockChain(16, seed=7)
        b = MockChain(16, seed=7)
        assert [a.block(h).payload for h in a.heights()] == [
            b.block(h).payload for h in b.heights()
        ]

    def test_different_seed_differs(self) -> None:
        assert MockChain(16, seed=7).block(0).payload != MockChain(16, seed=8).block(0).payload

    def test_out_of_range(self) -> None:
        with pytest.raises(IndexError):
            MockChain(4).block(4)

    def test_uniform_payload_size(self) -> None:
        chain = MockChain(16, block_size=64)
        assert {len(chain.block(h).payload) for h in chain.heights()} == {64}


class TestPrivacyTiers:
    def test_direct_leaks_everything(self) -> None:
        chain = MockChain(16)
        res = SyncClient(chain, PrivacyTier.DIRECT, ip="198.51.100.9").sync_block(5)
        assert res.view.client_ip == "198.51.100.9"
        assert res.view.requested_height == 5
        assert res.block == chain.block(5)

    def test_tor_hides_ip_not_query(self) -> None:
        chain = MockChain(16)
        res = SyncClient(chain, PrivacyTier.TOR, ip="198.51.100.9").sync_block(5)
        assert res.view.client_ip is not None
        assert res.view.client_ip.startswith("onion:")
        assert res.view.client_ip != "198.51.100.9"
        assert res.view.requested_height == 5
        assert res.block == chain.block(5)

    def test_tor_pir_hides_both(self) -> None:
        chain = MockChain(16)
        res = SyncClient(chain, PrivacyTier.TOR_PIR, ip="198.51.100.9").sync_block(5)
        assert res.view.client_ip is not None
        assert res.view.client_ip.startswith("onion:")
        assert res.view.requested_height is None
        assert res.view.records
        for record in res.view.records:
            assert record["requested_height"] is None
        assert res.block == chain.block(5)

    def test_all_tiers_same_payload(self) -> None:
        chain = MockChain(32)
        payloads = {
            SyncClient(chain, tier).sync_block(9).block.payload for tier in PrivacyTier
        }
        assert len(payloads) == 1

    def test_accepts_tier_as_string(self) -> None:
        chain = MockChain(16)
        res = SyncClient(chain, "tor").sync_block(3)
        assert res.tier is PrivacyTier.TOR

    def test_out_of_range_height(self) -> None:
        with pytest.raises(IndexError):
            SyncClient(MockChain(8), PrivacyTier.DIRECT).sync_block(8)

    def test_rejects_tiny_chain(self) -> None:
        with pytest.raises(ValueError):
            SyncClient(MockChain(1), PrivacyTier.DIRECT)


class TestDemoAndMetrics:
    def test_demo_runs_and_is_consistent(self) -> None:
        report = run_demo()
        assert report["consistent"] is True
        assert set(report["results"]) == {"direct", "tor", "tor_pir"}

    def test_bandwidth_report_values(self) -> None:
        r = bandwidth_report(64, 256, k_servers=2)
        assert r["download_everything_bytes"] == 64 * 256
        assert r["xor_pir"]["upload_bits"] == 2 * 64
        assert r["xor_pir"]["download_bytes"] == 256
        assert r["matrix_pir"]["upload_bits"] == 2 * 8
        assert r["matrix_pir"]["download_bytes"] == 2 * 8 * 256
        assert r["matrix_pir"]["download_bytes"] < r["download_everything_bytes"]

    def test_bandwidth_report_validation(self) -> None:
        with pytest.raises(ValueError):
            bandwidth_report(0, 256)
        with pytest.raises(ValueError):
            bandwidth_report(64, 0)
        with pytest.raises(ValueError):
            bandwidth_report(64, 256, k_servers=1)

    def test_privacy_matrix(self) -> None:
        tiers = {row["tier"]: row for row in privacy_matrix()}
        assert tiers["direct (tier 0)"]["hides_ip"] is False
        assert tiers["direct (tier 0)"]["hides_query"] is False
        assert tiers["tor (tier 1)"]["hides_ip"] is True
        assert tiers["tor (tier 1)"]["hides_query"] is False
        assert tiers["tor+pir (tier 2)"]["hides_ip"] is True
        assert tiers["tor+pir (tier 2)"]["hides_query"] is True
