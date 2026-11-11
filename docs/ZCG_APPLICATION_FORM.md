# ZCG Grant Application — ready to paste into the GitHub issue form

> Form: https://github.com/ZcashCommunityGrants/zcashcommunitygrants/issues/new
> Fields marked ⚠️ REQUIRE YOUR INPUT — do not submit without editing them.
> Budget arithmetic (verified): 1,000 + 6,100 + 19,900 = 27,000

---

## Title

Grant Application - PrivateSync: Privacy-Preserving Light Client Sync Infrastructure for Zcash

## Terms and Conditions (checkboxes — YOU must tick these)

Tick all 9 boxes after reading. Note:
- KYC is only required above $50,000 — this application asks $27,000.
- The CONTRIBUTING.md box: already satisfied — our repo ships one.
- The forum-posting box: step 3 of the submission checklist below.

## Application Owners

@sarinsk629-blip

## Organization Details

**Organization Name:** Independent developer — individual applicant (GitHub: sarinsk629-blip)

**How did you learn about Zcash Community Grants:** ⚠️ EDIT TO YOUR REAL PATH.
Suggested: "Through the Zcash Community Forum, while researching the open RFP
'Zcash Lightwalletd Infrastructure Development and Maintenance', and ZCG's
priorities page at zcashcommunitygrants.org."

## Project Overview

**Requested Grant Amount (USD):** $27,000

**Category:** ⚠️ Pick ONE from the Category Definitions page. Recommended:
"Core Development" (this project is light client infrastructure / SDK privacy).

## Team Information

**Project Lead:**
- Name: ⚠️ your real name or handle
- Role: Project Lead / sole developer
- Background: ⚠️ 2–3 honest sentences. If you have no prior Zcash work, say so
  plainly and point to this proposal repo (docs, PoC, CI) as demonstrated work,
  plus any merged PRs you make before applying (recommended: 1–2 small PRs to
  Zashi/lightwalletd/ZecHub first — ZCG weighs track record heavily).
- Responsibilities: delivery of all milestones, community liaison, forum updates,
  upstream coordination.

**Additional Team Members:** None or N/A
(If you have collaborators, replace "None or N/A" with their real name/role/
background/responsibilities. Do not invent people.)

## Project Details

**Project Summary:**

PrivateSync brings query-pattern privacy to Zcash light wallet sync: wallets
already tunnel sync through Tor via Arti (Zashi 2.1; native in Zkool), which
hides the IP — this project adds multi-server PIR so the sync operator can no
longer see or link which blocks a wallet downloads, plus the multi-operator
lightwalletd network ZCG's open RFP asks for. A working, CI-tested open-source
PoC already exists in the public proposal repository.

**Project Description:**

Zcash light wallets (Zashi, Zkool) sync through lightwalletd servers. Since
Zashi 2.1 (August 2025), wallets tunnel sync through Tor via the Arti client —
building on ZCG-funded Arti work — which hides the user's IP address from the
operator. What Tor does not hide: **which compact blocks the wallet downloads**
(correlatable with transaction timing), and the **stable client onion
identity** that lets an operator link all of a wallet's sync sessions over
time. This remains a metadata trail that can deanonymize otherwise fully
shielded activity.

This project delivers the layer Tor does not provide, built on existing Zcash
infrastructure and composed with the wallets' shipped Arti transports (we
deliberately do NOT re-implement what already ships):

- **Tier 1 — Tor onion sync (already shipped, acknowledged):** Zashi 2.1
  tunnels sync through Arti (beta, August 2025); Zkool — the successor to
  Ywallet — ships native Arti support. This matches the direction of
  librustzcash issue #2665 ("backend-agnostic network-privacy layer") and
  zcash-android-wallet-sdk issue #1741 ("Use new Lightwalletd calls over Tor").
- **Tier 2 — Tor + multi-server PIR (this proposal):** the block-index
  question is answered by k ≥ 2 independent PIR nodes using Chor-style XOR
  selection (√N matrix layout). Each node receives a uniformly random
  selector, so no single node learns which block was requested —
  information-theoretic, per-server privacy with no cryptographic hardness
  assumptions. PIR removes the last visible signal: the block index itself.

Goals: (1) a hardened, benchmarked reference implementation with a written
spec; (2) a prototype privacy transport that plugs into the SDK networking
layer; (3) a pilot of 3–5 independently operated testnet nodes with a runbook
so others can join; (4) an external review, final docs, and upstream PRs.

The full proposal, technical whitepaper, budget, research base (all sources
verified), and a working PoC with 34 passing tests are public in the linked
repository.

**Proposed Problem:**

Already solved elsewhere (and not re-done by this proposal): the IP-address
leak — Zashi 2.1 ships Tor via Arti (beta), Zkool ships native Arti support.

What is still open:

1. Query-pattern disclosure: even over Tor, the server sees which compact
   blocks a wallet pulls, correlatable with transaction timing.
2. Session linkability: a wallet's stable client onion identity lets the
   operator cluster all of its sync sessions over time, with or without IP
   visibility.
3. Centralization: wallet defaults point at a few servers; one operator sees
   metadata for a large share of users — the open lightwalletd RFP targets
   exactly this.
4. These limitations are documented in lightwalletd's own wallet-app threat
   model, and metadata privacy remains a live community concern (e.g., the
   ZachXBT report on Zashi CrossPay traceability, Oct 2025).

**Proposed Solution:**

A sync stack composed with the wallets' existing Arti/Tor transports, adding
the missing layer:

- Tier 1 (shipped by the ecosystem, not by this grant): onion-addressed
  lightwalletd access via Arti — Zashi 2.1 (beta) and Zkool already provide
  it. We build on it and benchmark against it.
- Tier 2 (this proposal): multi-server PIR — the client splits its request
  into uniformly random selector vectors; each PIR node answers with an XOR
  of selected matrix rows; the client reconstructs the block locally.
  Bandwidth overhead is O(√N) upload / O(√N·B) download per retrieval —
  benchmarked openly, and PIR ships as opt-in while Tor-only (already the
  wallet default) remains the fallback if overhead is too high.
- Deployment follows the multi-operator model the ZCG lightwalletd RFP asks
  for: independent nodes, runbook, monitoring.

**Solution Format:**

Open-source software (MIT) and documentation:
1. Hardened PoC + open spec (threat model, PIR parameters, benchmarks).
2. Prototype privacy transport (SDK-integration oriented).
3. Testnet pilot: 3–5 lightwalletd+PIR nodes with onion endpoints, node
   operator runbook, public monitoring dashboard.
4. External security review of the privacy layer, final docs, upstream PRs,
   maintenance/handover plan.

**Dependencies:**

- Technical: lightwalletd (Go), a backing node (zebrad) for testnet, Tor
  (onion services), the zcash-client-backend / SDK networking interfaces.
- Collaborations: feedback from ECC/ZF SDK maintainers (librustzcash #2665,
  SDK #1741); node operators willing to host pilot endpoints (recruited
  publicly; the RFP itself calls for multi-team infrastructure).
- Resources: modest testnet node hosting (budgeted), CI (GitHub Actions, free
  for public repos). No proprietary dependencies.

**Technical Approach:**

- PoC (exists): Python reference implementation of the three tiers, mock
  compact-block chain, XorPIR (k servers) and MatrixPIR (2 servers, √N×√N
  layout) with per-server information-theoretic privacy, simulated Tor
  circuits, bandwidth/leakage metrics, 34 tests (correctness + selector
  uniformity), ruff-clean, CI-green on Python 3.10–3.12.
- M1: extend PoC to streaming sync (multi-block, incremental chains),
  parameterize for realistic compact-block sizes, publish benchmarks + open
  spec.
- M2: implement the PIR fetch layer as a swappable networking component
  mirroring the upstream interface direction (librustzcash #2665) — layered on
  the wallets' existing Arti/Tor transports, no Tor re-implementation; PIR
  opt-in behind a flag; benchmark vs Tor-only baseline on testnet.
- M3: package node deployment (Docker/compose, onion service config),
  runbook, monitoring dashboard; recruit operators publicly.
- M4: external review (fixed scope, privacy layer focus), fixes, upstream
  PRs, handover.

**Upstream Merge Opportunities:**

- Repos forked/modified: `zcash/lightwalletd` (PIR fetch extension spec +
  deployment docs for multi-operator nodes); prototype aligned with
  `zcash/librustzcash` (`zcash_client_backend` networking direction, issue
  #2665) and `zcash/zcash-android-wallet-sdk` (issue #1741). Tor transport
  itself is NOT re-implemented — the wallets' shipped Arti integrations
  (Zashi 2.1, Zkool) are the transport layer we compose with.
- Changes: an optional PIR fetch extension specified so node software can
  adopt it incrementally; reference client implementation; onion deployment
  docs for node operators.
- Upstream benefit: wallet SDKs gain query-pattern-protected sync without
  protocol changes; node operators gain a standard multi-operator recipe.
- Coordination: engage maintainers on the existing issues (#2665, #1741)
  before/while building; no consensus changes, so merge risk is low.
- Timeline: PIR fetch PRs opened during M2, finalized in M4 after review.

**Open Source License:** MIT (already applied in the repository).

## Budget

**Hardware/Software Costs (USD):** $1,000
**Hardware/Software Justification:** Testnet node rental for M2 prototype
benchmarking (1 month, mid-size VPS) — the PoC itself runs anywhere.

**Service Costs (USD):** $6,100
**Service Costs Justification:** CI/tooling/misc for the spec review draft
($600, M1); hosting for 3–5 testnet lightwalletd+PIR nodes for the 3-month
pilot ($2,000, M3); fixed-scope external security review of the privacy layer
($3,500, M4).

**Compensation Costs (USD):** $19,900
**Compensation Costs Justification:** Part-time development at modest, flat
rates across 8 months: M1 PoC hardening + spec ($3,400); M2 SDK-integration
prototype + benchmarks ($9,000); M3 pilot network + runbook + dashboard
($6,000); M4 final docs, upstream PR prep, handover ($1,500). No equity,
tokens, or price exposure; USD-denominated, paid per milestone.

**Total Budget (USD):** $27,000

**Previous Funding:** None — this is our first Zcash Community Grants application.

**Previous Funding Details:** N/A

**Other Funding Sources:** None — no other grants, VC funding, or token sales
are planned or received for this project.

## Risk Assessment

**Implementation Risks:**

1. PIR bandwidth overhead at mainnet scale may exceed usefulness → benchmark
   in M1–M2 with published numbers; ship Tier 1 (Tor) as the default and PIR
   as opt-in until overhead is acceptable.
2. PIR nodes colluding would defeat per-server privacy → the design requires
   k−1-of-k honesty and we document this trust assumption explicitly; the
   multi-operator RFP model is the mitigation at deployment level.
3. Node operator recruitment may be slow → the RFP explicitly asks for
   multi-team infrastructure; coordinate via ZCG committee and existing node
   runners; runbook lowers the barrier.
4. Upstream interfaces may shift (librustzcash #2665 is active) → track the
   issues, keep the transport thin and swappable, deliver upstream-compatible
   APIs.

**Potential Side Effects:**

1. Sync latency/traffic increases with Tor and PIR → measure and publish; keep
   direct sync available as a user choice.
2. Onion service reliability varies → pilot with monitoring dashboard;
   document failover.
3. Overpromising privacy → we claim exactly what the PoC tests (per-server
   PIR privacy + IP hiding); the spec states what is NOT protected (global
   passive adversary, client compromise).

**Success Metrics:**

1. CI-green repository with ≥34 tests and lint/docs checks at every milestone.
2. Published benchmark table (sync time, bandwidth vs baseline) at M2.
3. ≥3 independently operated testnet nodes with onion endpoints + a third
   party completing the runbook at M3.
4. External review completed; all findings addressed or triaged at M4.
5. ≥1 upstream PR submitted and under review; forum thread with milestone
   updates and community feedback.

## Project Schedule

**Startup Funding (USD):** $0
**Startup Funding Justification:** No upfront payment requested. Milestone 1
is self-contained (PoC exists; hardening starts immediately) and is paid on
completion and acceptance.

## Milestone Details (delete prefilled Milestones 5–12 in the form)

- Milestone: 1
  Amount (USD): 4000
  Expected Completion Date: 2027-02-28
  User Stories:
    - "As a light wallet SDK developer, I want a tested reference
      implementation of private sync tiers, so that I can evaluate
      integration without building from scratch."
    - "As a community reviewer, I want a written spec with threat model and
      benchmarks, so that I can verify the security and feasibility claims."
  Deliverables:
    - Extended PoC: streaming sync (multi-block, incremental), parameterized
      for realistic compact-block sizes, CI green
    - Published benchmark table (bandwidth/sync time vs baseline)
    - Open spec document (threat model, PIR parameters, error handling)
      posted to the Community Forum for review
  Acceptance Criteria: CI is green on the public repo; an SDK developer can
  run the PoC and reproduce the benchmark table; the spec thread is open on
  forum.zcashcommunity.com and has received ZCG/community comment.

- Milestone: 2
  Amount (USD): 10000
  Expected Completion Date: 2027-04-30
  User Stories:
    - "As a wallet developer, I want a PIR fetch layer prototype aligned with
      librustzcash #2665, so that I can add query-pattern privacy on top of
      the wallet's existing Arti/Tor transport without re-implementing it."
    - "As a light wallet user, I want the sync operator to be unable to see
      or link which blocks I download, so that my activity cannot be
      profiled from sync metadata."
  Deliverables:
    - PIR fetch prototype (opt-in behind a flag) layered on the wallets'
      existing Arti/Tor transport direction (upstream networking interface)
    - Benchmark report: sync time + bandwidth vs Tor-only baseline, on
      testnet
    - Findings posted to the upstream issue threads (#2665, #1741)
  Acceptance Criteria: the prototype syncs a testnet chain end-to-end over
  Tor+PIR; the benchmark report is published in the repo; at least one
  upstream maintainer has commented on the posted findings.

- Milestone: 3
  Amount (USD): 8000
  Expected Completion Date: 2027-07-31
  User Stories:
    - "As a node operator, I want a runbook to deploy a lightwalletd+PIR node
      with an onion endpoint, so that I can contribute sync infrastructure."
    - "As a light wallet user, I want multiple independent sync endpoints, so
      that no single operator sees everyone's metadata."
  Deliverables:
    - 3–5 independently operated testnet lightwalletd+PIR nodes with onion
      endpoints, live for the remainder of the grant
    - Node operator runbook (deployment, onion config, monitoring)
    - Public status/monitoring dashboard
  Acceptance Criteria: a third party can stand up a node by following the
    runbook; the dashboard is publicly accessible; nodes are reachable over
    onion services on testnet.

- Milestone: 4
  Amount (USD): 5000
  Expected Completion Date: 2027-08-31
  User Stories:
    - "As a security reviewer, I want an externally reviewed privacy layer,
      so that flaws are found before production adoption."
    - "As an ecosystem maintainer, I want docs, upstream PRs and a handover
      plan, so that the work continues beyond the grant."
  Deliverables:
    - External security review of the privacy layer (fixed scope) and a
      findings report with fixes or triage
    - Final documentation set
    - Upstream PRs submitted (lightwalletd configs/docs; transport reference)
    - Maintenance and handover plan
  Acceptance Criteria: review findings are addressed or explicitly triaged;
    upstream PRs are open and under review; the handover document is merged.

## Supporting Documents

- File/Link 1: Proposal repository — https://github.com/sarinsk629-blip/Zcash_privacy-preserving-light-client-sync-proposal
  (contains docs/PROPOSAL.md, docs/TECHNICAL_WHITEPAPER.md, docs/BUDGET.md,
  docs/RESEARCH.md with verified sources, docs/PROPOSAL_CHECKLIST.md mapping
  ZCG criteria to evidence, and the PoC with CI badge)
- File/Link 2: Open RFP this application responds to —
  https://forum.zcashcommunity.com/t/rfp-zcash-lightwalletd-infrastructure-development-and-maintenance/47080
- File/Link 3: Upstream alignment — https://github.com/zcash/librustzcash/issues/2665
  and https://github.com/zcash/zcash-android-wallet-sdk/issues/1741

---

## AFTER SUBMITTING (required by the terms)

1. Copy the new issue URL.
2. Post it on forum.zcashcommunity.com (Grants category) — see
   FORUM_POST.md for ready-to-paste text.
3. Watch for ZCG questions and answer on the issue within 48h when possible.
