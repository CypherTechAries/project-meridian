# Security

## Reporting

Please report security concerns privately, through GitHub's **Report a vulnerability** flow on this
repository (Security → Advisories), rather than opening a public issue.

Include what you found, how to reproduce it, and what you think the impact is. Please allow a
reasonable period for a fix before any public disclosure. This is a solo research project, so
response times are best-effort rather than contractual.

## Scope

MERIDIAN is a **local research prototype**. It has no authentication, no user accounts, no
persistence and no deployment target. It is not intended to be exposed to a network, and running it
on a public interface is outside its design.

Useful reports include: a path allowing scenario loading outside the packaged allowlist; a way to
bypass a B5 control; dependency vulnerabilities reachable from the authoritative path; a way to make
the interface present fixture content as engine-computed output.

Out of scope: the absence of authentication, the in-memory-only run store, and anything requiring
the application to be deployed publicly — these are known design limits, documented in the README.

## Safety controls

MERIDIAN enforces a fictional-world boundary in code — eight controls covering scenario loading,
target validation, protected-trait exclusion, persuasion-optimisation refusal, disclosure and
provenance. They are specified and mapped to tests in
[`docs/safety/B5-TECHNICAL-CONTROLS.md`](docs/safety/B5-TECHNICAL-CONTROLS.md).

**A way to circumvent any of those controls is a security issue** and we would like to hear about it.
