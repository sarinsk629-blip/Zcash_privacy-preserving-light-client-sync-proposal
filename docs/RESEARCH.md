# Research base — verified sources

Every claim in the proposal traces to one of the sources below. All links were
retrieved and read while preparing this proposal (accessed: 2026-11-09/10).

## The need (ZCG's own words)

1. **ZCG open RFP — "Zcash Lightwalletd Infrastructure Development and Maintenance"**
   <https://forum.zcashcommunity.com/t/rfp-zcash-lightwalletd-infrastructure-development-and-maintenance/47080>
   ZCG invites submissions for "development, deployment, and ongoing maintenance of
   Zcash lightwalletd infrastructure", explicitly a *global public infrastructure
   maintained by many teams*. → Supports: our project responds to an open RFP.

2. **ZCG priorities page** — <https://zcashcommunitygrants.org>
   Lists, verbatim: "SDK — network layer privacy solutions for light client SDKs and
   libraries"; "Core — R&D decentralized light client syncing"; "Ongoing services —
   light client servers / infrastructure". → Supports: three priority hits in one
   proposal.

3. **ZCG grant range** — <https://zcashcommunitygrants.org> (grants range $5,000–$200,000)
   and recent meeting minutes (<https://forum.zcashcommunity.com/t/zcash-community-grants-meeting-minutes-10-23-2026/58488>)
   show approvals clustering small and milestone-based. → Supports: the $27k,
   4-milestone ask.

## The pain (documented, not invented)

4. **lightwalletd repository and wallet-app threat model**
   <https://github.com/zcash/lightwalletd>
   "lightwalletd is a backend service that provides a bandwidth-efficient interface
   to the Zcash blockchain for mobile and other wallets, such as Zashi and Ywallet";
   developers are pointed to the wallet-app threat model covering light-wallet
   privacy limitations. → Supports: the problem statement.

5. **ZachXBT on Zashi CrossPay / NEAR Intents traceability (Oct 2025)**
   <https://cryptorank.io/news/feed/90629-zachxbt-flags-privacy-flaw-in-zashi-wallets-near-intents-integration>
   and <https://x.com/zachxbt/status/1980612190609576229>
   Independent investigator flagged a traceability flaw in a Zashi integration;
   ECC responded with a remediation plan. → Supports: metadata privacy remains a
   live, high-visibility concern for the ecosystem.

6. **"TOR for Lightwalletd" community proposal (Dec 2023)**
   <https://forum.zcashcommunity.com/t/tor-for-lightwalletd/46358>
   Community discussion of Tor for lightwalletd gRPC; noted as a candidate path by
   core-adjacent maintainers. → Supports: Tier 1 is a long-acknowledged need.

## The upstream direction (we ride it, not fight it)

7. **librustzcash issue #2665 — "Add a backend-agnostic network-privacy layer" (Jul 2026)**
   <https://github.com/zcash/librustzcash/issues/2665>
   Generalize the Tor transport into a backend-agnostic network-privacy layer for
   lightwalletd clients. → Supports: our Tier 1/2 design plugs into planned
   upstream architecture.

8. **zcash-android-wallet-sdk issue #1741 — "Use new Lightwalletd calls over Tor" (Apr 2025)**
   <https://github.com/zcash/zcash-android-wallet-sdk/issues/1741>
   SDK-side plan to adopt Tor APIs behind a networking interface. → Supports:
   Tier 1 is the minimal shippable step and SDK integration is the right M2 focus.

9. **Zashi CrossPay launch (Sep 2025)** — <https://zodl.com/private-cross-chain-payments-with-zashi-crosspay>
   ECC's own post stresses minimizing metadata leakage as a product principle.
   → Supports: the ecosystem's stated values match this project's goals.

## Methods (the cryptography is standard)

10. Chor, Goldreich, Kushilevitz, Sudan — *Private Information Retrieval* (STOC'95)
    and Chor–Gilboa–Naor follow-ups: the k-server XOR scheme and the √N matrix
    layout implemented in `poc/` are the textbook constructions, used here for
    their per-server information-theoretic privacy. (Cited as literature; the PoC
    tests, not the papers, are the executable spec.)
