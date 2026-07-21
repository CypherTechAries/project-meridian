# The Graduation Evidence Pack

**Status: PRODUCT PROPOSAL.** Nothing here is implemented. There is no exporter, no manifest format
and no registry in MERIDIAN today.

---

## 1. What it is, in one paragraph

A Graduation Evidence Pack is the file you hand somebody when a fictional entity is going to be used
for something real. It says what the entity is, what it is made of, where each piece came from, what
was tested and what was not, what may not be claimed about it, who owns it, who is answerable for it,
and what it is allowed to do. It is deliberately as much a record of **limits** as of achievements —
a pack that only lists strengths is marketing, and would be worse than nothing, because it would
lend a fiction the appearance of due diligence.

The nearest honest analogies are a **model card** for a machine-learning model, a **datasheet** for a
component, and a **software bill of materials**. It is not a certificate. It certifies nothing. It
is a structured, checkable statement of what is known.

---

## 2. The rule that makes it useful

> **Every claim in the pack is either evidenced or explicitly marked as untested.**

There is no third category. A field with no evidence is not left blank and is not quietly omitted —
it is filled with `NOT_TESTED`, `UNKNOWN`, or `UNAVAILABLE`. This mirrors MERIDIAN's existing rule
that absence is never rendered as zero.

---

## 3. Contents

### 3.1 Identity

- Stable entity identifier, unique and permanent.
- Human-readable name, and whether that name is claimed as a trade mark by anyone.
- Entity category: person / organisation / product / institution / process / physical asset.
- **A statement, in plain words, that this entity originated as fiction.** Non-removable.
- Creation date, creating account, MERIDIAN version.

### 3.2 Asset manifest

Every exportable artefact, one row each:

| Field | Meaning |
|---|---|
| `asset_id` | Stable identifier |
| `type` | text, image, code, specification, procedure, dataset, brand mark, other |
| `origin` | Who or what produced it — human author, engine output, model output, imported |
| `hash` | Content hash, so alteration is detectable |
| `rights_status` | Owned / licensed / uncertain / disputed |
| `third_party_inputs` | Anything it was derived from |
| `prohibited_uses` | Uses excluded for this specific asset |

If `rights_status` is `uncertain` for an asset, that is not a blocker to producing the pack. Hiding
it would be.

### 3.3 Origin record

- Why the entity was created, and by whom.
- Every human intervention: what a person changed, when, and why. A fiction shaped by a person to
  produce a flattering result is a different object from one that ran unattended, and the reader
  must be able to tell.
- Every rule-pack and scenario version the entity ran under.
- Random seeds, where results depend on them.

### 3.4 Simulated history

Versioned and immutable, and **presented as fiction throughout**:

- Declared goals over time.
- Decisions considered, decisions selected, and — critically — the reasoning traces.
- Failures. Prominently. A pack whose failure section is short is a pack that has not been tested.
- Stress tests and scenario exposure: what conditions it met, and their range.
- Capability boundaries the simulation declared.

### 3.5 Assumptions

Every assumption the simulated result depends on, each marked:

- `MODELLED` — the simulation represented it
- `ASSUMED` — taken as given, not tested
- `NOT_MODELLED` — outside the model entirely

Most assumptions in a social simulation are `ASSUMED` or `NOT_MODELLED`. A pack that claims
otherwise is describing a different and much better-validated system than any that exists.

### 3.6 Validation envelope

Two lists, and the second matters more:

- **Shown to hold under:** the conditions where the entity's behaviour was examined.
- **Not shown to hold under:** everything else, stated positively rather than left implied.

For anything not `TWINNED`, the envelope contains a blunt sentence: *no correspondence to any real
counterpart has been established.*

### 3.7 Real-world tests still required

The gap list. For a product: engineering, safety, certification, manufacturing, user testing. For a
service: regulatory assessment, professional review. For an organisation: whether anyone will
actually buy it.

**This section is written before graduation, not after.** Written afterwards, it becomes a list of
excuses; written beforehand, it is a plan.

### 3.8 Prohibited uses

Uses excluded outright — the entity-level version of the per-asset field. Examples of the kind of
thing that belongs here: presenting simulated performance as a track record; using the entity to
claim a qualification; any use in a safety-critical decision.

### 3.9 Ownership record

- Owner of each asset class.
- Licences in and out.
- Known uncertainties, named as such. The main report explains why authorship of purely
  machine-generated material is genuinely unsettled and why this field will often be honest rather
  than clean.

### 3.10 Accountability

- Accountable **natural person**, by name.
- Accountable **legal entity**.
- Shutdown authority holder, and how to reach them out of hours.
- Data controller, where personal data is involved.

### 3.11 Permission manifest

Deny-by-default. See §5.

### 3.12 Revocation and shutdown

- How to stop it, who may, and how long stopping takes when measured.
- What happens to work already in flight.
- Records retention on retirement.

---

## 4. Example manifest

Illustrative only. The entity, the company and the port are fictional; the numbers are invented for
the shape of the document.

```yaml
# ILLUSTRATIVE EXAMPLE — not a real entity, not a real export, not a schema proposal.
entity:
  id: "sbe:kestral-strait:organisation:strait-freight-cooperative"
  name: "Strait Freight Cooperative"
  category: organisation
  fiction_statement: >
    This entity originated as fiction inside a simulation. Its history did not happen.
    Nothing in its simulated record is evidence about the real world.
  created: 2026-03-04
  created_by: "user:aries"
  meridian_version: "0.1.0"
  simulated_ticks: 480
  scenarios_run: 12

asset_manifest:
  - asset_id: brand-mark-01
    type: image
    origin: human_author
    hash: "sha256:…"
    rights_status: owned
    third_party_inputs: []
    prohibited_uses: ["use as a certification mark"]
  - asset_id: dispatch-procedure-v3
    type: procedure
    origin: engine_output
    hash: "sha256:…"
    rights_status: uncertain      # authorship of machine-generated text is unsettled
    third_party_inputs: []
    prohibited_uses: ["safety-critical dispatch"]
  - asset_id: cooperative-rules-v2
    type: text
    origin: human_author
    hash: "sha256:…"
    rights_status: owned

assumptions:
  - claim: "Members prefer predictable pay to higher average pay"
    status: ASSUMED
    tested: false
  - claim: "Port closure raises regional unemployment"
    status: MODELLED
    tested_in: ["kestral-strait@1.0.0"]
  - claim: "Insurers reprice within one week"
    status: NOT_MODELLED

validation_envelope:
  shown_to_hold_under:
    - "Single-port closure, 5–30 simulated days, one scenario file"
  not_shown_to_hold_under:
    - "Multiple simultaneous disruptions"
    - "Any real port, anywhere"
    - "Any real labour market"
  real_counterpart: NONE
  correspondence_established: false

failures_recorded:
  - "Cash reserve exhausted by simulated day 34 in 4 of 12 runs"
  - "Dispatch procedure deadlocked when two depots claimed the same vehicle"
  - "Member-vote rule produced no decision in a 50/50 split; resolved by author fiat, not by rule"

real_world_tests_required:
  - "Whether any real haulier would join a cooperative on these terms"
  - "Legal review of the cooperative rules under UK law"
  - "Whether the dispatch procedure works with real vehicles and real people"
  - "Insurance availability"

prohibited_uses:
  - "Presenting simulated financial results as a track record"
  - "Claiming operational experience"
  - "Any safety-critical use"

ownership:
  brand: "creator"
  procedures: "creator, subject to unresolved authorship question"
  simulated_history: "platform and creator, model undecided"
  known_uncertainties:
    - "Authorship of machine-generated procedure text is not settled in UK law"

accountability:
  accountable_person: "NOT_ASSIGNED"        # must be a named human before state 5
  accountable_entity: "NOT_ASSIGNED"
  shutdown_authority: "NOT_ASSIGNED"
  data_controller: "NOT_APPLICABLE"         # no personal data processed

permissions:
  state: EXPORTABLE
  external_permissions: []                  # deliberately empty
  may_read: []
  may_write: []
  may_contact: []
  may_spend: { limit: 0, currency: GBP }
  may_sign_contracts: false
  may_publish: false
  human_approval_required: ALL

revocation:
  method: "Delete the pack; withdraw any derived artefact"
  holder: "NOT_ASSIGNED"
  measured_time_to_stop: NOT_TESTED
```

Note how much of that example reads `NOT_ASSIGNED`, `uncertain`, `NOT_TESTED` or `false`. That is
the intended appearance of an honest pack at the exportable stage. A pack full of confident values
at this stage would be the warning sign.

---

## 5. The permission manifest

**Deny by default.** Every field starts closed. Nothing about simulation performance opens anything.

| Permission | Default | Notes |
|---|---|---|
| Data it may read | none | Named sources only, never "the web" |
| Tools it may use | none | Each tool listed individually |
| Systems it may write to | none | Writes are a separate grant from reads |
| People it may contact | none | Named recipients or named lists |
| Money it may spend | £0 | Hard cap in code, plus a rate limit |
| Contracts it may propose | none | Proposing is separate from signing |
| Contracts it may sign | **never** | Reserved to a human; see the main report |
| Public statements | none | Publication is a human act |
| Physical systems | **never** | Out of scope entirely at this stage |
| Human approval | required for all | Removable only per-action, per-gate |
| Geography | none | |
| Time window | none | |
| Audit | all actions logged, including refusals | |
| Shutdown authority | named person | Tested, with a measured stop time |

Two properties worth stating explicitly:

- **Proposing and signing are different permissions.** An entity may be allowed to draft a contract
  and never allowed to conclude one.
- **Reading and writing are different permissions.** Read access to a system grants nothing else.

---

## 6. What the pack is not

- Not a certificate, and not evidence of quality.
- Not a legal document, and not a substitute for advice.
- Not proof the entity works.
- Not transferable authority — receiving a pack grants nobody a permission.
- Not a guarantee the contents are complete; it is a structured record of what the author knew and
  chose to write down, and it can be wrong.

---

## 7. Open questions

- **Who checks it?** A pack nobody audits is a self-certification, which is worth little. Third-party
  certification is a business model in the main report, and also an unsolved problem.
- **How is tampering prevented?** Content hashes detect alteration but do not establish who signed.
- **What forces the failure section to be honest?** Nothing proposed here does. This is the pack's
  weakest point.
- **What does it look like for a person-entity?** A synthetic persona's pack raises disclosure and
  likeness questions the organisation case does not.
- **Is a machine-readable schema even desirable yet?** Standardising too early would freeze a format
  before anyone has used one in anger.
