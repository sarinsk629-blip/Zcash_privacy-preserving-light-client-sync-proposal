# Contributing

Thanks for helping make Zcash light client sync private.

## Ground rules

- MIT-licensed; all contributions are under the same license.
- Every change must keep CI green: `pytest`, `ruff check`, and the docs checker
  (see `.github/workflows/ci.yml`).
- No secrets, tokens, or keys in commits — ever. If one slips, rotate it
  immediately and notify the maintainer.

## Local development

```bash
pip install -r poc/requirements-dev.txt
pytest
ruff check poc scripts
python scripts/check_docs.py
```

## Good first contributions

- Extend the PoC: variable block sizes, k > 2 XorPIR benchmarks, a streaming sync
  mode (see docs/ROADMAP.md M1).
- Docs: clarify the whitepaper, improve the threat model.
- Tests: tighten the statistical privacy tests.

## Process

1. Open an issue describing the change.
2. Fork / branch, commit with clear messages.
3. Open a PR; a maintainer reviews; squash-merge.

## Code of conduct

Be excellent to each other. This repo follows the spirit of the Zcash community
code of conduct.
