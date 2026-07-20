# Contributing

Thank you for looking at MERIDIAN.

## Code contributions are not currently accepted

**Source available — all rights reserved.** No licence is granted, and contribution terms are not yet
in place. Until they are, unsolicited pull requests cannot be merged, so please do not spend time on
one without asking first.

This is not a judgement on the contribution. It is that accepting code without agreed terms creates
an ownership question the project cannot currently answer cleanly.

## Issues and feedback are very welcome

Genuinely useful, and the fastest way to help:

- **Claims that do not hold.** If a statement in the README or `docs/` overstates what the code does,
  that is a defect and one worth reporting. The project treats accurate description as a feature.
- **Reproducible faults** — with the seed, scenario, mode and tick count.
- **Interface confusion.** If a screen failed to explain itself, say where you got stuck.
- **Questions about the model**, its limits, or the safety controls.

Use the issue templates. There is no support commitment; this is a research and engineering project.

## If contributions open later

The expectations will be:

- branch from `main` using the prefixes in [`docs/BRANCHING.md`](docs/BRANCHING.md);
- keep both test suites green — backend `pytest`, frontend `npm test`;
- **never weaken an honesty or safety test to make a change pass.** If a test blocks you, that is a
  finding to report, not an obstacle to remove;
- state the determinism impact of any engine change;
- include a screenshot for user-visible interface changes;
- update the relevant record in `docs/delivery/` when behaviour changes.

## Security

Do not open a public issue for a security concern. See [`SECURITY.md`](SECURITY.md).
