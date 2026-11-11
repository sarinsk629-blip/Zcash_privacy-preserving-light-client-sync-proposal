# FORUM_POST.md — ready to paste on forum.zcashcommunity.com

Post this in the **Grants** category after submitting the GitHub issue, and
replace `ISSUE_URL` with the real issue link. Community input is REQUIRED
before ZCG can discuss and vote.

---

**Title:** ZCG Application — PrivateSync: Privacy-Preserving Light Client Sync Infrastructure (feedback wanted)

Hi all,

I've submitted a ZCG grant application and I'm posting it here for community
input, as required: ISSUE_URL

**The problem:** Zashi and other light wallets sync through lightwalletd
servers. Since Zashi 2.1 (Aug 2025) wallets tunnel sync through Tor via Arti,
so the IP leak is largely handled — but the sync operator still sees which
compact blocks the wallet downloads, and a wallet's stable client onion
identity links all of its sync sessions. That metadata trail can deanonymize
otherwise shielded activity. lightwalletd's own wallet-app threat model
documents these limitations, and ZCG's open RFP for lightwalletd
infrastructure asks for a multi-operator solution.

**The proposal:** build the layer Tor does not provide — query-pattern
privacy — on top of the ecosystem's shipped Arti/Tor transports (no Tor
re-implementation), aligned with upstream work (librustzcash #2665, SDK
#1741):

- Tier 1 — Tor onion sync: **already shipped** (Zashi 2.1 via Arti; native
  in Zkool, Ywallet's successor) — acknowledged and built upon, not redone
- Tier 2 — Tor + multi-server PIR (this proposal): no single sync node
  learns which block you requested (information-theoretic, per-server
  privacy)
- Deployment: 3–5 independently operated testnet nodes + a runbook so more
  operators can join — the multi-team model the RFP calls for

**Ask:** $27,000 over 8 months, paid per milestone, no upfront.

**Evidence base (everything is public):**
- Application repo (proposal, whitepaper, budget, verified research):
  https://github.com/sarinsk629-blip/Zcash_privacy-preserving-light-client-sync-proposal
- Working PoC already in the repo: multi-server PIR + tiered sync demo, 34
  passing tests, CI green on Python 3.10–3.12
- The open RFP it responds to:
  https://forum.zcashcommunity.com/t/rfp-zcash-lightwalletd-infrastructure-development-and-maintenance/47080

I'd genuinely value critique before ZCG reviews it — especially on:
1. the PIR bandwidth assumptions vs real compact-block sizes,
2. the node-operator recruitment plan,
3. whether Tier 1 (Tor-only) should just be the default end-state.

Thanks for reading. 🛡️

---

## Submission checklist (do these in order)

1. ⚠️ Edit the two fields marked in ZCG_grant_application.md:
   "How did you learn about ZCG" (your real path) and the Project Lead
   background (your real, honest background).
2. Submit the GitHub issue with all 9 terms checkboxes ticked.
3. Copy the issue URL and post FORUM_POST.md text (with the URL filled in)
   in forum.zcashcommunity.com → Grants category.
4. Respond to ZCG/community questions on the issue promptly.
5. If not already done: make 1–2 small merged PRs to a Zcash repo before ZCG
   reviews — track record is the top rejection reason in 2026 minutes.
