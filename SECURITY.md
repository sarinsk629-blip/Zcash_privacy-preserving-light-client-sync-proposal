# Security Policy

## Scope

This repository contains a **grant proposal** and a **proof-of-concept
demonstration** (`poc/`). The PoC:

- runs entirely against simulated networks and a mock chain;
- makes **no network calls**;
- is **not audited** and must not be used to protect real funds or real traffic.

## Reporting a vulnerability or correctness issue

- Open a GitHub issue for non-sensitive problems (incorrect crypto reasoning,
  test gaps, documentation errors).
- For sensitive reports, contact the maintainer via GitHub
  ([sarinsk629-blip](https://github.com/sarinsk629-blip)) and allow up to 7 days
  for a response before public disclosure.

## Expectations

The privacy properties we claim are precisely the ones tested in
`poc/tests/` — per-server information-theoretic privacy of PIR queries and the
tiered metadata model. We do not claim:

- protection against a global passive adversary on Tor;
- protection against client-side compromise;
- production readiness of the PoC.
