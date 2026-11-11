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

> **Correction log (2026-11):** a community reviewer correctly flagged that
> Ywallet is discontinued (superseded by Zkool) and that Zashi 2.1 already
> ships Tor via Arti (sources 10–11 below). The proposal's problem statement
> was updated accordingly: the IP-address leak is largely solved by the
> wallets' Arti integrations; the open gap this project targets is
> query-pattern privacy and session linkability (sources 10–12).

4. **lightwalletd repository and wallet-app threat model**
   <https://github.com/zcash/lightwalletd>
   "lightwalletd is a backend service that provides a bandwidth-efficient interface
   to the Zcash blockchain for mobile and other wallets"; developers are pointed
   to the wallet-app threat model covering light-wallet privacy limitations.
   (The README's wallet examples include Ywallet, which has since been
   discontinued in favor of Zkool — see source 11.) → Supports: the problem
   statement.

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
   the SDK networking interface is the right integration point for the PIR
   fetch layer (M2).

9. **Zashi CrossPay launch (Sep 2025)** — <https://zodl.com/private-cross-chain-payments-with-zashi-crosspay>
   ECC's own post stresses minimizing metadata leakage as a product principle.
   → Supports: the ecosystem's stated values match this project's goals.

## The current state (verified after community review — November 2026)

10. **Zashi 2.1: Enhanced Privacy with Tor (Beta) (Aug 7, 2025)**
    <https://zodl.com/zashi-2-1-enhanced-privacy-with-tor-beta> and
    <https://forum.zcashcommunity.com/t/zashi-2-1-enhanced-privacy-with-tor-beta/51865>
    "Zashi's Tor integration is built on Arti, a Rust-based Tor implementation";
    the wallet's built-in Tor client is used for transaction submission and
    other traffic. → Supports: Tier 1 (IP hiding) already ships; this proposal
    builds the layer above it, not a duplicate.

11. **Zkool — successor to Ywallet (hanh)**
    <https://github.com/hhanh00/zkool2> ("Zkool - Wallet for Zcash (successor to
    ywallet)") and docs <https://hhanh00.github.io/zkool2>; community thread
    <https://forum.zcashcommunity.com/t/zkool-the-successor-to-ywallet/51139>.
    Zkool ships native Arti/Tor support per community discussion. → Supports:
    accurate current wallet landscape; prior Arti integration work to build on.

12. **What Tor alone does not solve**
    Even with Arti/Tor transports, the sync operator still observes which
    compact blocks a wallet requests, and the wallet presents a stable client
    onion identity that links its sessions over time. → Supports: the open gap
    (query-pattern privacy) that multi-server PIR addresses; matches ZCG's
    "network layer privacy solutions for light client SDKs" priority.

## Methods (the cryptography is standard)

13. Chor, Goldreich, Kushilevitz, Sudan — *Private Information Retrieval* (STOC'95)
    and Chor–Gilboa–Naor follow-ups: the k-server XOR scheme and the √N matrix
    layout implemented in `poc/` are the textbook constructions, used here for
    their per-server information-theoretic privacy. (Cited as literature; the PoC
    tests, not the papers, are the executable spec.)
