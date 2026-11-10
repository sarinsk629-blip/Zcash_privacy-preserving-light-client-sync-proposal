# FORUM_POST.md — ready to paste on forum.zcashcommunity.com

Post this in the **Grants** category after submitting the GitHub issue, and
replace `ISSUE_URL` with the real issue link. Community input is REQUIRED
before ZCG can discuss and vote.

---

**Title:** ZCG Application — PrivateSync: Privacy-Preserving Light Client Sync Infrastructure (feedback wanted)

Hi all,

I've submitted a ZCG grant application and I'm posting it here for community
input, as required: ISSUE_URL

**The problem:** Zashi/Ywallet sync through lightwalletd servers, and that
sync leaks the user's IP address and which compact blocks the wallet
downloads — a metadata trail that can deanonymize otherwise shielded
activity. lightwalletd's own wallet-app threat model documents these
limitations, and ZCG's open RFP for lightwalletd infrastructure asks for a
multi-operator solution.

**The proposal:** a three-tier privacy stack for light client sync, aligned
with upstream work already in flight (librustzcash #2665, SDK #1741):

- Tier 1 — Tor onion sync for lightwalletd (ships first)
- Tier 2 — Tor + multi-server PIR, where no single sync node learns which
  block you requested (information-theoretic, per-server privacy)
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
