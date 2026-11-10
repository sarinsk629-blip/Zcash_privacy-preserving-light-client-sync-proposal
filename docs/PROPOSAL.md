# ZCG Grant Proposal: Privacy-Preserving Light Client Sync Infrastructure for Zcash

**Applicant:** sarinsk629-blip ([github.com/sarinsk629-blip](https://github.com/sarinsk629-blip))
**Requested amount:** $27,000 USD, paid per milestone
**Duration:** 8 months (4 milestones)
**Proposal repository:** [github.com/sarinsk629-blip/Zcash_privacy-preserving-light-client-sync-proposal](https://github.com/sarinsk629-blip/Zcash_privacy-preserving-light-client-sync-proposal)

## 1. Summary

Zcash light wallets (Zashi, Ywallet) sync through lightwalletd servers. Today that
sync leaks the user's IP address to the server operator, and the server can observe
which blocks the wallet downloads — a metadata trail that deanonymizes otherwise
shielded transactions. ZCG's open RFP ["Zcash Lightwalletd Infrastructure
Development and Maintenance"](https://forum.zcashcommunity.com/t/rfp-zcash-lightwalletd-infrastructure-development-and-maintenance/47080)
asks for a global, multi-operator lightwalletd infrastructure; ZCG's priority list
separately calls for "network layer privacy solutions for light client SDKs" and
"R&D decentralized light client syncing". This proposal delivers exactly that layer:
a Tor-integrated, multi-server PIR sync network for light clients, built as open
source and aligned with upstream work (librustzcash #2665,
zcash-android-wallet-sdk #1741).

## 2. Problem

1. **IP disclosure.** Light wallets connect to lightwalletd over gRPC; the operator
   learns the wallet's IP address on every sync.
2. **Query-pattern disclosure.** The server sees which compact blocks a wallet
   pulls, which can be correlated with transaction timing and the wallet's view of
   the chain.
3. **Centralization pressure.** Wallet defaults point at a handful of servers; a
   single operator sees metadata for a large fraction of users.
4. lightwalletd's own documentation directs developers to the wallet-app threat
   model describing these limitations.

## 3. Proposed solution: three privacy tiers, one sync stack

| Tier | Transport | IP hidden? | Block queries hidden? | Cost |
|------|-----------|:----------:|:---------------------:|------|
| 0    | direct gRPC (status quo) | ✗ | ✗ | none |
| 1    | Tor onion lightwalletd | ✓ | ✗ (operator sees queries) | ~zero |
| 2    | Tor + multi-server PIR | ✓ | ✓ (no server learns which block) | low bandwidth overhead |

Tier 1 is deployable immediately and matches work already planned upstream
(librustzcash #2665 "backend-agnostic network-privacy layer"). Tier 2 applies
Chor–Gilboa–Naor style XOR-based multi-server PIR over compact-block data so that
each server answers a randomized query and no individual server learns which block
the client wants; client uploads scale as O(√N) with the √N×√N layout.

The PoC in this repository (`poc/`) implements all three tiers with tests: a mock
compact-block chain, PIR servers and client, simulated Tor circuit wrappers, and
bandwidth/leakage metrics. It is a reference demonstration, not audited production
code — the milestones below harden and productionize it.

## 4. Milestones and budget

| # | Milestone | Duration | Budget | Deliverables & acceptance criteria |
|---|-----------|----------|--------|-------------------------------------|
| M1 | PoC hardening + open spec | 2 mo | $4,000 | CI-green PoC extended to streaming sync; written spec (threat model, PIR parameters, error handling); published on the forum for comment |
| M2 | SDK integration prototype | 2 mo | $10,000 | Privacy transport prototype against zcash-client-backend patterns (mirrors librustzcash #2665); benchmark report: sync time + bandwidth vs baseline |
| M3 | Distributed sync node pilot | 3 mo | $8,000 | 3–5 independently operated testnet lightwalletd nodes with onion endpoints; node-operator runbook; public monitoring dashboard |
| M4 | Audit, docs, handover | 1 mo | $5,000 | External code review of the privacy layer; final documentation; upstream PRs submitted; maintenance/handover plan |
| | **Total** | **8 mo** | **$27,000** | |

Payments requested per completed milestone. All code MIT-licensed, public from
day one. See [BUDGET.md](BUDGET.md) for the line-item breakdown.

## 5. Why this wins ZCG's stated criteria

- **Responds to an open RFP** (lightwalletd infrastructure) rather than inventing a
  need.
- **Hits three listed priorities**: SDK network-privacy, decentralized light client
  syncing, light client servers/infrastructure.
- **Builds on existing infra** (lightwalletd, librustzcash Tor work) — does not
  reinvent wallets or payments.
- **Modest, milestone-based budget** in the range ZCG has actually approved
  ($1.5k–40k cluster in recent meetings).
- **Public, verifiable progress**: CI-green repo, spec review on the forum,
  milestone reports.

## 6. Team

- **sarinsk629-blip** — project lead. Background and prior work: *(fill in before
  submission: link 1–2 prior projects or merged PRs; ZCG weights track record
  heavily)*

Team details are provided in the grant application issue itself
(Project Lead section) and in docs/ZCG_APPLICATION_FORM.md.

## 7. Risks and mitigations

- **PIR bandwidth overhead at mainnet scale** → benchmark in M1–M2; fall back to
  Tier 1 (Tor-only) as the shipped default if overhead exceeds budget.
- **Node operator recruitment** → the RFP explicitly asks for multi-operator
  infrastructure; coordinate with the ZCG committee and existing node runners.
- **Upstream drift** → track librustzcash #2665; deliver upstream-compatible APIs.

## 8. Community engagement

Spec posted to forum.zcashcommunity.com for review at M1; milestone updates in the
grants category; ZecHub onboarding write-up at M3.
