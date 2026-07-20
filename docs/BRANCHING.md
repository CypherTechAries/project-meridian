# Branching and repository hygiene

> **Proposed policy — awaiting founder approval.** Nothing has been deleted, renamed or
> force-pushed. This document records the model; applying the cleanup requires explicit approval.

## Canonical branches

| Role | Branch | Notes |
|---|---|---|
| Default / production | **`main`** | The only long-lived branch. Every release is cut from it. |
| Integration | *(none)* | A `develop` branch is **not** warranted at current scale — one maintainer, short-lived branches, hosted CI on every push. Add one only if parallel release trains appear. |
| Release preparation | `release/<version>` | Short-lived; merged back into `main` and then retired. |

`main` is stable and CI-verified. **New work always branches from `main`.**

## Naming convention

| Prefix | Use | Example |
|---|---|---|
| `feat/` | New capability | `feat/ui-briefing-view` |
| `fix/` | Bug fix | `fix/cohort-weighting-overflow` |
| `docs/` | Documentation only, no code | `docs/two-horizon-roadmap` |
| `research/` | Experiments not intended to merge as-is | `research/belief-update-rules` |
| `release/` | Release preparation | `release/v0.1-public-front-door` |
| `archive/` | Preserved history before deletion | `archive/feat-old-thing` |

Use short, hyphenated, descriptive names. No personal names, no ticket numbers alone, no `test2`.

## Rules

**Never push directly to `main`.** All changes arrive by pull request, even for the sole maintainer —
the PR is where CI runs and where the reasoning is recorded.

**Merge strategy: merge commits.** History is a record of how the project actually developed, which
matters more here than a linear log. Do not rebase or force-push shared branches.

**Every PR must:** keep the test suites green; state its determinism impact if any; not weaken an
honesty or safety test to make a change pass; include a screenshot for user-visible UI change.

**Hotfixes** branch from `main` as `fix/<name>`, carry a test reproducing the fault, and merge by PR
like anything else. There is no emergency path that bypasses CI.

## Retiring a branch

1. Confirm it has **zero unique commits** — `git rev-list --count main..<branch>` returns `0`.
2. Confirm no open PR references it.
3. If it has unique work that should be preserved but not merged, copy it to `archive/<name>` first.
4. Delete only with owner approval.

**Never delete a branch with unique commits without an explicit decision.** A merged branch is
recoverable from history; an unmerged one may not be.

## What new contributors should do

Branch from `main` · use the prefixes above · open a PR · include tests · update the relevant record
in `docs/delivery/` if behaviour changes · never push to `main` · never weaken a test to make CI pass.

Note that unsolicited code contributions are not currently accepted — see
[`../CONTRIBUTING.md`](../CONTRIBUTING.md).

## Recommended GitHub protection for `main`

To be applied by the owner after publication:

- Require a pull request before merging
- Require status checks to pass (`CI`)
- Block force pushes
- Block deletion
- Require conversation resolution
- **Do not** require an approving review from another person — it would block solo development.
  Add that requirement only when a second maintainer exists.

## Access levels

| Level | Who |
|---|---|
| Admin | Owner only |
| Maintain | Trusted long-term maintainers only |
| Write | Regular contributors, working through PRs |
| Triage / Read | Reviewers and external advisors |
