# PoC: privacy-preserving light client sync (simulated)

Reference implementation backing the [ZCG grant proposal](../docs/PROPOSAL.md).
It demonstrates the three sync privacy tiers and the multi-server PIR schemes —
**entirely in-process, against a mock chain, with zero network calls**.

## What it implements

| Module | Contents |
|--------|----------|
| `chain.py` | Deterministic mock compact-block chain (uniform-size payloads) |
| `pir.py` | `XorPIR` (k servers, O(N) upload) and `MatrixPIR` (2 servers, O(√N) upload) with information-theoretic per-server privacy |
| `client.py` | `SyncClient` with three privacy tiers + simulated Tor circuits; models exactly what an observer learns |
| `metrics.py` | Bandwidth report and the privacy matrix (single source of truth) |
| `demo.py` | End-to-end demo across all tiers |
| `tests/` | Correctness + privacy-property tests |

## Quickstart

```bash
pip install -r requirements-dev.txt

# full test suite (correctness + privacy properties)
pytest

# demo: sync block #37 of a 64-block chain over all three tiers
PYTHONPATH=src python -m pirlight.demo

# lint
ruff check . ../scripts
```

Expected demo output:

```
[  direct] observer sees: ip=203.0.113.7  requested_height=37
[     tor] observer sees: ip=onion:XXXXXXXX  requested_height=37
[ tor_pir] observer sees: ip=onion:XXXXXXXX  requested_height=None
```

## Scope honesty

This is a **reference demonstration**, not audited production code: the network
and Tor are simulated, payloads are mock data, and mainnet parameterization is
the M1–M2 work of the proposal. See [SECURITY policy](../SECURITY.md) for the
exact claims we make — and the ones we deliberately do not.
