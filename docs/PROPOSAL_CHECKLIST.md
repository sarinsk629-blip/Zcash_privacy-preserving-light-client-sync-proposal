# ZCG approval checklist — evidence map

ZCG committees evaluate proposals on a recognizable set of criteria, based on the
grant process page and on decision patterns in 2026 meeting minutes. This maps
each criterion to concrete evidence in this repository.

| # | ZCG criterion | Our evidence |
|---|---------------|--------------|
| 1 | Addresses a stated Zcash need | Responds to the open lightwalletd-infrastructure RFP ([RESEARCH.md §1](RESEARCH.md)); hits 3 listed priorities verbatim |
| 2 | Not reinventing the wheel | Builds on lightwalletd, librustzcash Tor work (#2665), SDK Tor plans (#1741) ([RESEARCH.md §3](RESEARCH.md)) |
| 3 | Reasonable, milestone-based budget | $27,000 / 4 milestones / no upfront ([BUDGET.md](BUDGET.md)) |
| 4 | Concrete deliverables & acceptance criteria | PROPOSAL.md §4 table: every milestone has checkable outputs |
| 5 | Public, verifiable progress | CI-green repo from day one; PoC with tests in `poc/`; commit history |
| 6 | Team has credibility | Honest, first-time applicant profile in the application issue (Project Lead section, docs/ZCG_APPLICATION_FORM.md); 1–2 merged upstream PRs recommended before ZCG review |
| 7 | Community engagement plan | Forum spec review at M1; milestone updates; ZecHub write-up (PROPOSAL.md §8) |
| 8 | Risks acknowledged with mitigations | PROPOSAL.md §7 (bandwidth fallback, operator recruitment, upstream drift) |
| 9 | Licensing / open source | MIT, public from day one ([LICENSE](../LICENSE)) |
| 10 | Sustainability / handover | M4 includes maintenance & handover plan; node-operator runbook in M3 |

## Red flags we deliberately avoid (observed rejections, Oct 2026 cycle)

- ❌ Duplicate payment/checkout solutions → we build sync infrastructure, not payments
- ❌ Large asks from teams with zero public Zcash footprint → modest ask + evidence-first repo
- ❌ Vague specs → written spec is a named M1 deliverable
- ❌ "Marketing research" → none requested
- ❌ Overclaiming (audited-code claims, fake privacy guarantees) → limitations stated plainly in the whitepaper §5
