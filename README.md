# Zcash Privacy-Preserving Light Client Sync — Grant Proposal

[![CI](https://github.com/sarinsk629-blip/Zcash_privacy-preserving-light-client-sync-proposal/actions/workflows/ci.yml/badge.svg)](https://github.com/sarinsk629-blip/Zcash_privacy-preserving-light-client-sync-proposal/actions/workflows/ci.yml)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

A complete **Zcash Community Grants (ZCG) application** for privacy-preserving
light client sync infrastructure, plus a **working proof-of-concept**.

## The problem

Zcash light wallets (Zashi, Ywallet) sync through [lightwalletd](https://github.com/zcash/lightwalletd)
servers. Today that sync:

1. **leaks the user's IP address** to the server operator, and
2. **lets the server see which blocks the wallet downloads** — a metadata trail
   that can deanonymize otherwise fully shielded transactions.

## The proposal

A Tor-integrated, multi-server PIR sync network for Zcash light clients,
delivered as open source with three privacy tiers:

| Tier | Transport | IP hidden? | Block queries hidden? |
|------|-----------|:----------:|:---------------------:|
| 0 | direct gRPC (status quo) | ✗ | ✗ |
| 1 | Tor onion lightwalletd | ✓ | ✗ |
| 2 | Tor + multi-server PIR | ✓ | ✓ |

**Ask:** $27,000 over 8 months, paid per milestone — squarely inside the range
ZCG has actually approved, responding to an open RFP rather than an invented need.

## Repository map

| Path | What it is |
|------|------------|
| [`docs/PROPOSAL.md`](docs/PROPOSAL.md) | **The ZCG grant application** (summary, problem, milestones, budget, risks) |
| [`docs/TECHNICAL_WHITEPAPER.md`](docs/TECHNICAL_WHITEPAPER.md) | Threat model, architecture, PIR design |
| [`docs/BUDGET.md`](docs/BUDGET.md) | Milestone-based budget and justification |
| [`docs/RESEARCH.md`](docs/RESEARCH.md) | Verified sources: RFP, ZCG priorities, upstream issues |
| [`docs/PROPOSAL_CHECKLIST.md`](docs/PROPOSAL_CHECKLIST.md) | Every ZCG approval criterion mapped to our evidence |
| [`docs/ROADMAP.md`](docs/ROADMAP.md) | M1–M4 delivery plan |
| [`poc/`](poc/README.md) | Working Python PoC: multi-server PIR + tiered sync demo + tests |
| [`TEAM.md`](TEAM.md) | Applicant profile (to be completed by the applicant before submission) |

## Quickstart (PoC)

```bash
pip install -r poc/requirements-dev.txt

# run the test suite
pytest

# run the demo: sync block #37 over all three privacy tiers
PYTHONPATH=poc/src python -m pirlight.demo

# lint
ruff check poc scripts
```

The demo builds a deterministic mock compact-block chain and shows exactly what a
network observer sees at each tier — including that at Tier 2 no server learns
which block was requested.

## Scope honesty

The `poc/` code is a **reference demonstration** (simulated network, mock chain),
not audited production code. Hardening it is Milestone M1 of the proposal. All
budget figures, milestones and claims are documented and traceable to the
sources in [`docs/RESEARCH.md`](docs/RESEARCH.md).

## License

MIT — see [LICENSE](LICENSE).
