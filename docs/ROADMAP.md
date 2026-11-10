# Roadmap — 8 months, 4 milestones

## M1 (months 1–2): PoC hardening + open spec — $4,000

- Extend the PoC from single-block retrieval to streaming sync (multi-block,
  incremental chains).
- Parameterize for realistic compact-block sizes; publish a benchmark table.
- Write the open spec: threat model, PIR parameters, error handling, failure modes.
- **Acceptance:** CI green; spec posted to forum.zcashcommunity.com for review;
  benchmark table published in-repo.

## M2 (months 3–4): SDK integration prototype — $10,000

- Implement the privacy transport as a swappable networking layer following the
  direction of librustzcash #2665 (backend-agnostic network-privacy layer) and
  zcash-android-wallet-sdk #1741 (lightwalletd calls over Tor).
- Prototype targets: Tier 1 (onion) as default, Tier 2 (PIR) behind a flag.
- **Acceptance:** prototype syncs a testnet chain end-to-end over Tor; benchmark
  report comparing sync time and bandwidth vs baseline; upstream issue threads
  updated with findings.

## M3 (months 5–7): Distributed sync node pilot — $8,000

- Stand up 3–5 independently operated testnet lightwalletd + PIR nodes.
- Publish the node-operator runbook (deployment, onion setup, monitoring).
- Public status dashboard for the pilot network.
- **Acceptance:** ≥3 nodes live on testnet with onion endpoints; a third party can
  follow the runbook to add a node; dashboard is public.

## M4 (month 8): Audit, docs, handover — $5,000

- External review of the privacy layer (focused, fixed-scope).
- Final documentation set; upstream PRs submitted.
- Maintenance and handover plan for post-grant operation.
- **Acceptance:** review findings addressed or triaged; upstream PRs open; handover
  document merged.

## Post-grant sustainability

- Node operations continue under the multi-operator model the RFP envisions.
- The spec and runbook lower the barrier for new node operators — the network's
  decentralization grows with adoption, not with this grant.
