I read all eight documents in full. Below is the briefing.

---

# MERIDIAN world-model → interface obligations briefing

**Scope read:** `docs/world-model/ENTITY-ONTOLOGY.md` (1180 ln), `PERSON-MODEL.md` (1361), `ORGANISATION-MODEL.md` (1794), `RELATIONSHIP-GRAPH.md` (1416), `BELIEF-AND-KNOWLEDGE-MODEL.md` (1324), `POPULATION-FIDELITY.md` (998), `docs/safety/IDENTITY-AND-BIAS-GUIDELINES.md` (1029), `docs/design/ENTITY-PROFILE-EXPERIENCE.md` (978).

**Framing that applies to everything below.** All eight carry an identical banner: *"⚠ SPECIFICATION — NOT IMPLEMENTED."* All are **DRAFT, pending owner review** and **BACKLOG**. Nothing described is built. Where a document marks something proposal / unresolved / owner-decision, I have preserved that marking; anything in this briefing without such a marking is a stated requirement of the document, not of the codebase.

---

## 1. Interface obligations

### 1.1 The governing frame

> "The profile interface must therefore be built as an intelligence product, not an omniscient encyclopaedia."
> — ENTITY-ONTOLOGY §8.1 (:585-586)

> "An encyclopaedia tells you what is true. An intelligence product tells you **what you have been able to establish, how confident you are, where it came from, and what is still unknown or contested**."
> — ENTITY-PROFILE-EXPERIENCE §1 (:77-79)

The dossier renders **primarily the fourth view** (player intelligence), "drawing on the second and third where the player's role has access to them, and **never** the first except where the player's role has legitimately established a fact" (ENTITY-PROFILE-EXPERIENCE §1, :97-99).

### 1.2 Purity constraints — the dossier must not change the world

> **"D-1. A dossier is a projection, never a mutation.** Rendering a profile must be a pure function of authoritative reality, observation history and the observer. It must never write to authoritative state. Opening, reading, closing and re-opening a dossier any number of times must leave the simulation byte-identical."
> — ENTITY-PROFILE-EXPERIENCE §3 (:190-193)

> **"D-2. A dossier must consume zero randomness.** … If it did, *looking at an entity would change the simulation* … A player who opens ten dossiers must not thereby move the national economy."
> — ibid. (:195-200)

> **"D-3. Projection and narration are two separate steps, and only the second may call a model.** The projector computes the structured view — values, confidence labels, evidence links, contradictions — with no language model involved."
> — ibid. (:202-207)

The ontology states the same as four constraints on `project()`:

> "MUST NOT read another view. MUST NOT write to authoritative state. MUST NOT consume RNG draws (a projection must not perturb the run; see §7.3). MUST NOT call the LLM. Rendering the result into prose is a separate, later step."
> — ENTITY-ONTOLOGY §9.2 (:866-869)

The ontology adds the reason: "**projection must consume no randomness**, or reading a profile would change the simulation — a variant of the same attention-perturbs-the-world defect" (:874-876).

### 1.3 Visibility must be enforced server-side

> "The dossier must enforce this at the point of projection, not by hiding rendered content in the browser. **A value the player's role may not see must never be sent to the client at all.**"
> — ENTITY-PROFILE-EXPERIENCE §4.1 (:227-228)

> "There must be **no omniscient read path exposed to the interface**. An interface query returning authoritative edges rather than the observer's view would turn the intelligence product back into the encyclopaedia the source record explicitly rejects."
> — RELATIONSHIP-GRAPH §10, rule RG-Q1 (:1060-1064)

### 1.4 Two axes, never one enum

> "Whether an observer *may* see an attribute (visibility) and how well the observation is *evidenced* (confidence) are different questions. `Restricted` is a visibility outcome; `Disputed` is an evidence outcome. Overloading one enum with both would produce a model that cannot express 'observable but poorly evidenced' or 'well-evidenced but withheld'."
> — ENTITY-ONTOLOGY §8.4 (:684-688)

Restated as RG-5 (RELATIONSHIP-GRAPH :435-438), as ENTITY-PROFILE-EXPERIENCE §4.2 (:230-244), as BELIEF §4.7's three-axis table (observability / credence / evidential confidence, :891-895), and as ORGANISATION §10.5 (:1144-1148).

**RELATIONSHIP-GRAPH goes further than the others:**

> **"Specified invariant RG-4.** Confidence labels must attach **per dimension**, not per edge. A player may have confirmed that two ministers are related by marriage while only having an assessed view of whether one resents the other."
> — RELATIONSHIP-GRAPH §4.3 (:405-408)

### 1.5 The eight confidence labels

**Confirmed · Reported · Assessed · Disputed · Unknown · Possibly deceptive · Outdated · Restricted** (ENTITY-ONTOLOGY §8.4 :677-678; ENTITY-PROFILE-EXPERIENCE §5.1 :331; ORGANISATION §10.3 :1086; RELATIONSHIP-GRAPH §4.3 :386).

> **"V-4.** Confidence labels must be **computed** by the view projector from recorded evidence — observation records, source reliability, corroboration count, staleness, and known deception — and must never be authored, either by a scenario author or by the LLM."
> — ENTITY-ONTOLOGY §8.4 (:680-683)

> **"C-1.** Every value the dossier shows on the player-intelligence view carries exactly one label. **A value with no label must never be rendered.**"
> — ENTITY-PROFILE-EXPERIENCE §5.1 (:333-334)

Per-label interface treatment is specified in ENTITY-PROFILE-EXPERIENCE §5.2 (:343-352) and the assignment rules in BELIEF §4.7 (:897-906). Load-bearing display rules:

- **Unknown:** "Row present but value absent — the *absence* is information and must be shown, not hidden" (EPE :349). BELIEF: "**Must be displayed, not hidden** — an absent field and an unknown one are different statements" (:903).
- **Disputed:** "Value shown alongside the contradicting value(s); **the player is never handed a false resolution**" (EPE :348).
- **Outdated:** "**The player is told the basis is stale; never what changed.**" (BELIEF :905). BELIEF adds: "The label must leak the *existence* of a change and nothing about its content, and the rule must be tested for that" (:913-915).
- **Restricted:** "Row present, **value withheld**, labelled Restricted — the player learns the attribute *exists* but not its value, unless even existence is withheld" (EPE :352).
- **Possibly deceptive:** "Value shown with an explicit deception warning; never silently trusted" (EPE :350). "The label warns; it does not correct, **because correcting it would leak authoritative reality the role has not earned**" (EPE :364-366).

> "**Unknown and Restricted must both be rendered as present rows.** An intelligence product's most important content is often what it does *not* know or *may not* see. Hiding those rows entirely would turn the dossier back into an encyclopaedia that simply looks complete."
> — ENTITY-PROFILE-EXPERIENCE §5.2 (:356-360)

> "A role that has observed nothing must receive `Unknown` everywhere. That is the specified behaviour rather than a degenerate case."
> — BELIEF §4.7 (:910-912)

**`Restricted` is an unresolved design decision, not a settled rule:**

> "**`Restricted` leaks by existing.** Showing 'Restricted' tells the player there is something there. For some roles that is correct; for others the attribute should render as `Unknown` and be indistinguishable from absence. **This is a genuine design decision with a security character and is left open in Part 9.**"
> — BELIEF §4.7 (:916-919)

### 1.6 Provenance separation of engine fact from AI prose

> **"P-1.** Every element the dossier renders is exactly one of two kinds: an **engine-computed assertion** or an **AI-generated narration**. The two must be visually distinguishable at a glance, per element, with no reliance on a page-level caption or a documentation footnote (CHARTER.md:141).
> **P-2.** No AI-generated narration may ever be rendered in the visual style of an engine-computed assertion, and no engine-computed assertion may borrow the styling of narration to look more readable. **The distinction is load-bearing and must not be softened for aesthetics.**
> **P-3.** A confidence label belongs **only** to an engine-computed assertion. Narration never carries a confidence label, because it is not evidence; it carries a provenance tag instead."
> — ENTITY-PROFILE-EXPERIENCE §6.1 (:384-396)

The §6.2 table (:422-429) specifies the concrete differentiators:

| | Engine-computed assertion | AI-generated narration |
|---|---|---|
| Container | Plain data row / field | "A visibly distinct container — tinted panel, ruled edge, or equivalent — that reads as 'not a fact panel' without needing to be read" |
| Persistent tag | Confidence label chip | "A persistent 'AI-generated' provenance badge **on the block itself, so a screenshot of the block alone still carries its provenance**" |
| Grounding affordance | Evidence affordance opening the observation records | "A 'grounded in' affordance listing the record IDs the narration was rendered from" |
| Versioning shown | Tick and derivation | "`model_id + prompt_version + temperature` of the generation" |
| May change numbers? | The value *is* state (read-only here) | "**Never.** If narration and the facts it cites disagree, the facts win and the narration is flagged as stale and regenerated" |

> **"P-5. Grounding citations must be emitted by the projector, never returned by the model.** … If the model returned the citation set, the model would be attesting to its own grounding and the check would be **circular** … the narration return type carries **prose only**. If a future design needs the model to indicate which of the supplied records it drew on, that returned set must be validated as a **subset of the supplied set**, and any unrecognised ID must **reject the narration** rather than be displayed."
> — ENTITY-PROFILE-EXPERIENCE §6.4 (:455-468)

Charter-level, restated in five documents: "every generated advisory text must carry a visible provenance tag at the interface level, distinguishing it from engine-computed fact" (ENTITY-ONTOLOGY §8.5 :714-716; PERSON-MODEL 6.3 :1099; IDENTITY §7.3 :676-678; ORGANISATION §16.2 :1512-1513).

### 1.7 The pre-display bias gate (P-4)

> **"P-4. Every narration block must pass the pre-display bias filter, and the dossier must not juxtapose identity with judgement.** P-1 to P-3 govern *provenance* and the never-author boundary. Neither catches **stereotyped inference from facts that are true**: a biography narrated from a truthful ethnic, religious or class identity field can imply competence, morality or reliability without inventing a single fact …
> - Every generated narration block the dossier renders must pass the prohibited-construction detector of IDENTITY-AND-BIAS-GUIDELINES §6.4 **before display**, not only in offline tests. **A block that fails the filter must not be rendered.**
> - No dossier prompt may instruct or invite the model to infer character, competence or morality from identity.
> - **Display rule.** The dossier must not place a sensitive-identity attribute adjacent to a competence, reliability or morality assessment in a way that implies causation between them — the juxtaposition itself carries the inference, whether or not either element is individually honest.
>
> The filter is a **heuristic** and the safety document says so: it will miss stereotypes it has no pattern for. **It is a required gate, not a proof of safety.**"
> — ENTITY-PROFILE-EXPERIENCE §6.1 (:398-418); obligation placed on this surface by IDENTITY §7.3 (:674-675)

### 1.8 Things the interface must never show

| Obligation | Source |
|---|---|
| "A 'true priorities' panel must never be rendered from `actual_priorities` directly, at any tier, for any role, without an evidence chain that supports each line." | ORGANISATION §10.5 (:1138-1139) |
| "Divergence is NEVER exposed as a number on the player-facing profile." | ORGANISATION §10.4 (:1120) |
| `factually_wrong()` "must **not** be automatically available to a player. What a player sees is the disclosure view in 4.7, and **no player role may be granted a direct read of `truth_value` without an explicit owner decision recorded against the role model.** Otherwise the intelligence product collapses back into the omniscient encyclopaedia." | BELIEF §4.6 (:875-879) |
| "Deriving it guarantees the interface can never show a trusted-source badge on an edge whose trust score does not support it." | RELATIONSHIP-GRAPH §5.3 (:481-482) |
| The standalone public view "**must not be described as causal in the interim**" and "must not be implemented before Q-R is taken". | ENTITY-ONTOLOGY §13 (:1129) |
| "A query that cannot be answered historically must fail explicitly rather than silently return current values, because a silently current answer to a historical question is worse than an error — it produces confident, wrong after-action analysis." | RELATIONSHIP-GRAPH §6.6, RG-T9 (:662-666) |
| "**Specified rule RG-Q3 — presentation is not state.** Graph layout, clustering, node placement and visual emphasis are presentation concerns with no causal role, and must be computed in the interface layer. They must never be persisted as entity or edge state." | RELATIONSHIP-GRAPH §10 (:1095-1098) |
| "**HARD RULE: no simulation mechanism may read this type**" (`PlayerIntelligenceEdgeView`). "A mechanism that reads it would let the PLAYER'S knowledge leak into WORLD behaviour, which is a different defect from fake depth and a worse one." | RELATIONSHIP-GRAPH §9 (:1021-1024) |
| "the specification must **not** claim the player-facing labels are causal … **Any future feature that lets a player-facing label alter state would violate V-2 and V-3.**" | ENTITY-ONTOLOGY §13 (:1127) |
| "the confidence labels are a property of the **observer's evidence**, not a decoration on the attribute. `Confirmed` must mean *this player role holds evidence sufficient to confirm it*, and must be computed by `M-OBS`, not authored." | ORGANISATION §10.5 (:1140-1142) |
| Labels "must never be produced by the LLM. If a briefing says 'confirmed', that word must have come from a computed label passed into the prompt as data, not from the model's own assessment. **This requires a test.**" | BELIEF §4.7 (:920-922) |
| "The dossier's self-understanding panel is generated by comparing recorded values. **An LLM may phrase the comparison. It may not perform it.**" | BELIEF §4.9 (:1020-1021) |
| "If a fact appears in a generated biography and nowhere in the structured record, it is not true in the simulation and nothing may act on it." | PERSON-MODEL E-6 corollary (:445-446) |
| Portrait: "If a portrait shows a detail absent from the record, that detail is not true in the simulation and nothing may act on it." | PERSON-MODEL 6.1 (:1076-1077) |

### 1.9 Specified fallbacks / null-behaviour the interface must implement

- `identity.name` absent → "**Dossier shows the `person_id`.** No simulation effect." (PERSON-MODEL 3.2, :498)
- `identity.portrait_ref` absent → "**Dossier renders a placeholder.** No simulation effect." (PERSON-MODEL 3.2, :509)
- Portrait versioning: "Expression variants, context states and age progressions must be **new versions with a common lineage**, never in-place replacements. **The historical asset must remain retrievable, so a dossier viewed at an earlier tick can render correctly.**" (PERSON-MODEL 6.3, :1095)
- Portraits "must not change between sessions, between runs of the same scenario, or on reload" (PERSON-MODEL 6.3, :1092; POPULATION-FIDELITY §6.3, :508-509; EPE §10.2, :754-755)

### 1.10 State-dossier interface requirement

> "The defining requirement of the state dossier is that it must make **internal disagreement visible**. A player must be able to see that the government, the public, the military, the courts, businesses and regional authorities hold different positions on the same crisis — because they do, and because a single national number that hides that is the 'country as one agent' the source record rejects."
> — ENTITY-PROFILE-EXPERIENCE §8.3 (:605-608)

Tab-set adaptation rule: "**a tab must map onto a capability the entity type actually carries** (ENTITY-ONTOLOGY §5). A community does not `act`, so a community dossier has no Motivations-as-individual-goals tab; a state is a composition, so a state dossier is a portal, not a single profile." (EPE §8, :548-551)

---

## 2. Named attributes available to display, by entity type

Legend used below: **[M]** = spec maps it to a named mechanism (causal); **[P]** = spec labels it PRESENTATION-ONLY / no mechanism; **[C]** = conditional — causal only under a stated structural condition; **[⚠]** = mapped only to a mechanism the owning document itself marks named-but-undefined.

### 2.1 Base entity (all six types) — ENTITY-ONTOLOGY §6.2 (:426-440)

`entity_id` [M], `entity_type` [M], `capability_traits` [M], `fidelity_tier` [M], `rng_substream_key` [M, prerequisite missing], `existence_interval {created_tick, dissolved_tick?}` [M], `containment` / `structural_relations` [M], `authoritative_state` [M], `history_ref` [M, P0.6], `observation_log_ref` [M, P0.6], `relationship_edges_ref` [M], `influence_weight_terms` [M], `generation_provenance {spec_hash, substream_key, generated_at_tick, generator_version}` — `generator_version` explicitly "**Keep with an honest label:** it is an operational/diagnostic field, not a simulation attribute" (§13, :1125).

**Deliberately excluded from the base** (§6.3, :453-466): **no display name**, **no prose biography field**, **no portrait in authoritative state**.

`InfluenceWeightTerms` (§9.1, :777-784): `represented_population`, `economic_weight`, `organisational_weight`, `positional_weight`, `access_weight` — all [M], "Multi-term, NOT a single population scalar."

Structural relations displayable as relations (§4.3, :258-263): `contains`, `member_of`, `occupies_role_in`, `governed_by`, each with `since_tick` / `until_tick`.

### 2.2 Person — PERSON-MODEL Part 3 (`person.<group>.<field>`)

**`identity`** (3.2, :496-510)
- `name` (given/family/honorific/display) — **[P]** "A display label. Must not be read by any state-changing mechanism."
- `aliases[] {alias, context, known_to[]}` — [M] M12, M4
- `age` — [M] M1, M6, M9, M15
- `date_of_birth` — **[P]** "unless a records-matching or document-verification mechanism is built"
- `place_of_birth` — [M] M6, M3, M17
- `current_residence` — [M] M3, M6, M9, M17
- `citizenship[]`, `nationality` — [M] M13, M3, "**and M2 only indirectly, via `legal_status`**"; sensitive under E-3, carve-out unresolved
- `ethnic_identity`, `cultural_identity`, `religious_identity` — each with `salience 0..1` and `publicly_known bool` — [M] **restricted to M6, M17, M19, M3 "and nothing else"**
- `languages[] {language, proficiency 0..1, register}` — [M] M19, M3, M6, M10
- `household[]`, `family[]` — typed directed edges — [M] M6, M7, M9, M16, M18, M20
- `physical_appearance` — **[P]**; `distinctive_features[]` is **[C]** — promotable "**only if** a witness-identification or disguise mechanism is built"
- `portrait_ref` — **[P]**, founder-stated
- `public_identity` vs `concealed_identity` + `concealment_strength 0..1` — [M] M12, M3, M17

**`life_history`** (3.3, :560-570) — *structural requirement*: stored as typed dated records `{event_type, period, place, counterparts[], magnitude, valence, evidence_visibility}`, "**Prose biography must be generated from these records at read time and must never be the source of truth**" (:544-546).
- `childhood_environment` — **[C]** "Mapped **only** as structured fields. As a prose paragraph it has no reader."
- `family_wealth_and_class` — [M] M6, M9, **not M2**
- `education[]` — [M] M6, M3, M4
- `service_record` — [M] M6, M4, M8, M14
- `employment_history[]` — [M] M6, M14, M16
- `migration_and_travel[]` — [M], flagged "at risk" (9.3)
- `achievements[]` — **[C]** "Mapped **only** when structured with a verifying entity … **Free-text achievements with no verifier are PRESENTATION-ONLY**"
- `traumatic_experiences[] {event_ref, category, severity, age_at, resolved}` — [M] M8, M20, M9
- `criminal_or_disciplinary[] {…, public, spent}` — [M] M12, M16
- `political_involvement[]` — [M] M14, M6, M12, **not M2**
- `previous_crises[] {crisis_ref, role_held, outcome, lesson_tag}` — [M] M8, M1, M20

**`psychology`** (3.4, :584-600) — vocabulary requirement: `values`, `political_beliefs`, `fears`, `aspirations` must come from "bounded, scenario-authored, machine-readable vocabularies. **As free text they are prose, and Rule P-1 strikes them.**"
- `values[]`, `political_beliefs[] {position_tag, strength, publicly_stated}`, `religious_commitment {intensity, participation_frequency}`, `risk_tolerance`, `need_for_status`, `empathy`, `ambition`, `patience`, `susceptibility_to_pressure`, `attitude_to_authority`, `attitude_to_violence`, `institutional_trust` (per-institution map), `perceived_grievances[]`, `long_term_aspirations[]`, `immediate_objectives[]` — all [M] with named readers
- `personal_fears[]` — **[C]** "**Free-text fears are PRESENTATION-ONLY**"
- `loyalty` — **materialisation-time seed only**, "**no reader of its own**" (Rule P-6)
- **Not carried forward:** `corruption_susceptibility` (9.4)

**`capabilities`** (3.5, :621-632) — `expertise[]`, `leadership`, `negotiation`, `languages` (reference), `social_influence` (**derived from the graph, never stored**), `financial_resources`, `institutional_access[]`, `security_clearance`, `military_or_technical_skills[]`, `media_reach` (**coupled to B5**), `physical_health`, `dependents_and_obligations[]` — all [M].

**`relationships`** (3.6, :661-663) — `out_edges[]` [M] ("the single largest input to behaviour"), `obligation_ledger[]` [M], `trusted_sources[]` **derived, "Must not be stored separately."**

**`state`** (3.7, :682-699) — `location`, `health`, `stress`, `fatigue`, `financial_pressure`, `confidence`, `loyalty` (per-target), `current_intentions[]`, `knowledge[]`, `beliefs[]`, `rumours_heard[]`, `recent_contacts[]`, `current_role`, `available_resources`, `public_reputation` (**per-audience map**), `private_reputation` (**per-observer-class map**), `exposure_to_danger` (**authoritative reality**), `perceived_threat` (**self-understanding view**) — all [M].

> "`state.public_reputation` … Must be per-audience: a figure trusted by one community and despised by another must be representable." (:696)
> "`state.private_reputation` … Must hold standing among peers and insiders, which must be able to invert public standing entirely." (:697)
> "`state.current_intentions[]` … Must be **partially observable to others (M12)** — which is what makes intelligence work meaningful." (:689)

**Note the two-field split for danger** (3.7 :698-708): `exposure_to_danger` is the objective world fact and "**must never be written by any psychological mechanism**"; `perceived_threat` is what the person believes. "The divergence between the two is … the point."

### 2.3 Organisation — ORGANISATION §7.1 (:422-458), §12 (:1296-1319)

Fields: `org_id`, `org_kind` (ministry | court | armed_service | firm | union | party | media_outlet | religious_body | militia | ngo | regulator | central_bank | regional_authority), `legal_status`, `founding: FoundingRecord`, `public_mission` (**"DECLARED. Never read by M-ARB"** — [M] for M-DIV/M-REP only), `actual_priorities` (**AUTHORITATIVE**, [M] M-ARB step 4), `self_understanding` (**⚠ "READ BY NO MECHANISM AS SPECIFIED"**, §15-R11), `blocs`, `decision_procedure`, `role_occupancies`, `capabilities`, `assets`, `funding`, `geographic_presence`, `obligations`, `legal_exposure`, `cohesion`, `morale`, `reputation_public`, `reputation_private`, `standing_strategy`, `open_disputes`, `memory: InstitutionalMemory`.

Deliberately absent: **no `action` / `preferred_action` field**, **no relationships block** (edges live in RELATIONSHIP-GRAPH), **no belief map**, **no free-text description as authoritative state** (:460-472).

**Bloc** (§8.2, :518-545): `bloc_id`, `bloc_kind`, `label` (**"presentation only; never read by any mechanism"**), `interest_vector` [M], `formal_weight` [M], `informal_leverage` [M], `blocking_rights` [M], `led_by` [⚠ M-LEAD named-but-undefined], `membership` [⚠], `internal_cohesion` [M], `risk_posture` [M], `external_patrons` [M], `grievance_ledger` [M].

**Decision procedure** (§8.3, :567-580): `kind` (autocratic | collegial | board_vote | bureaucratic | consensus | command), `chair_bloc`, `quorum`, `veto_holders`, `deviation_cost`, `deadlock_action`, `leverage_admissibility`. "`kind` is the organisation's **culture** expressed as parameters rather than adjectives" (:583).

**Decision output** (§9.7, :955-983): `OrganisationDecision` (`chosen_option`, `option_set` incl. gated options + reasons, `aggregate_scores`, `probability_vector`, `transform_id`, `procedure_applied`, `rng_substream`, `rng_draw_index`, `justification_frame` [M, structured], `served_priorities` [M]) and **`stated_justification: str` — "PRESENTATION-ONLY, LLM-RENDERED, READ BY NO MECHANISM"**; `DissentRecord` entries `{bloc, chosen_score, best_score, deficit, overridden, grounds}` — "Emitted as authoritative state, not as narrative" (:716).

§12 downgrades to note for display: rows 5 (leadership), 8/9 (membership/recruitment — `M-RECR` undefined), 16 (rivals/partners — `M-EST` undefined), 18 (legal exposure), 20 (institutional memory — P0.6), 21 (internal disputes) all carry ⚠.

### 2.4 Business — ORGANISATION §14 (:1372-1390)

`ownership: list[OwnershipStake]` [M], board/exec `role_occupancies` [⚠ M-LEAD], `funding` (revenue lines) [M], `assets.liabilities` (debt) [M], workforce `blocs[].membership` [⚠], supply chain (edges) [M], `assets` + `geographic_presence` (facilities) [M], customers (edges) [M], competitors (edges) [M for M-DEP, ⚠ for M-EST], `obligations` (regulatory) [M], political relationships (edges) [M], `blocs[].grievance_ledger` (labour relations) [M], insurance exposure via `obligations` + insurer dependency edge [M], `reputation_public/_private` [M], `market_confidence` [M for M-RES; **⚠ downgraded** — "the 'investor bloc scoring' route is not supported by the specified procedure"], `vulnerabilities: list[VulnerabilityRecord]` [⚠ and **charter-constrained**: "CHARTER.md:137-138 forbids real operational vulnerabilities. These must be fictional, mechanism-level and non-actionable"].

### 2.5 Community (Tier-4 cohort) — POPULATION-FIDELITY §5.5, ENTITY-ONTOLOGY §10.1

Simulated per §5.5 (:370-376): distributional state (income distribution, age structure, employment, exposure) [M], **belief distributions — "not a single scalar per belief"**, narrative adoption [M], grievance set with onset/cause/resolution [M], membership accounting (how many promoted out) [M].

Key display-bearing commitment: **dispersion**, not just mean —

> "Tier 4 belief must therefore be specified as a **distribution** (at minimum a central tendency plus a dispersion term) … the dispersion term is the sampling parameter for §7 materialisation, and it is also what allows a minority position inside a cohort to exist at all."
> — POPULATION-FIDELITY §5.5 (:385-389)

Existing structures mapped for restructure (ENTITY-ONTOLOGY §10.1, :903-909): `Demographics` — **"Single majority labels (`religion_majority`, `primary_language`) make intra-cohort minorities unrepresentable"**; `EconomicProfile`; `MediaExposure` — "reach carries **no trust-in-channel term**"; `CohortBeliefs`; `InfluenceSusceptibility` (**COUPLED TO B5**); `NetworkPosition.bridges_to`.

Unmapped at this tier (§10.2, :873-876): `region` ("Existing field, no reader"); Tier-3 `income`, `exposure`, `insecurity`.

Community **does not `act`** (ENTITY-ONTOLOGY §5.3, :356-361): "A community must not emit a unitary decision, because that would reintroduce exactly the group-essentialism the safety guidelines forbid … Collective behaviour must instead emerge as an *aggregate rate*."

### 2.6 Institution

ENTITY-ONTOLOGY §4.2: "a durable rule-bearing structure". Traits: **no `holds_beliefs`, no `possesses_resources`** (§5.3, :351). `InstitutionState` is named in the §9.1 union but **its contents are nowhere enumerated**. §13 records: "`institution` as a distinct type … Justified by feeding the legality gate — but **the legality gate does not exist** … If the legality gate is never built, `institution` becomes fake depth and must be struck" (:1133).

ORGANISATION treats an institution as "an organisation with a legal mandate and a constitutional position, **not as a distinct fourth type**" (§2, :88-90) — an unreconciled divergence from the ontology's six-type taxonomy.

### 2.7 State / country

ENTITY-ONTOLOGY §4.4 is explicit that **`StateState` has no specified contents**:

> "**What `StateState` authoritatively contains is unspecified, and this section does not fill the gap.** … it is a live possibility that `StateState` carries only territory and the structural relations already on the base — in which case the block should be struck and `state` reduced to a composition root. Deciding this requires P0.4 and is **owner decision Q-S**. **Until then, `StateState` must not be implemented.**"
> — (:286-296)

ORGANISATION §11.2 supplies the *candidate* `CountryEntity` fields (:1177-1196): `political_system`, `constitutional_order`, `organs`, `parties`, `regions`, `population` (cohort ids), `industries`, `infrastructure`, `media_environment`, `external_relations`, `historical_grievances` [⚠ P0.6], `state_capacity`, `elite_cohesion` [⚠ for M-ARB], `legitimacy`, and `indicators_view: DerivedIndicators` — "the existing 18 scalars, **DEMOTED to derived**". §13 row 18 **National myths: ✘ "No mechanism specified."** §13 row 10 **Class structure: ⚠ referred out, no mechanism anywhere.** §13 row 8 **Languages and religions: ⚠ downgraded, "the safe default is struck or gated, not retained."**

### 2.8 The causal-value rule as it bears on display

The rule is stated identically across documents (ENTITY-ONTOLOGY §1 :73-75; PERSON-MODEL P-1/P-2; RELATIONSHIP-GRAPH RG-2; POPULATION-FIDELITY §10; ORGANISATION §6; BELIEF Part 5). RELATIONSHIP-GRAPH is the sharpest on the interface implication:

> "Anything satisfying neither is **struck** from the schema, not marked 'future use'. **A field that renders in the interface and satisfies neither category is struck regardless of how useful the rendering is.** … Category (b) is **not** a general exemption … It must never be used to retain a field on the ground that a dossier tab displays it."
> — RELATIONSHIP-GRAPH §4.2, RG-2 (:299-308)

And the dossier's own inversion of the rule:

> "the dossier **introduces no new authoritative attributes.** Every value a tab shows must trace to a field specified in a world-model document … A tab that shows something tracing to no underlying attribute is fake depth and must be struck."
> — ENTITY-PROFILE-EXPERIENCE §12 (:811-815)

---

## 3. The relationship graph's display-relevant commitments

### 3.1 Directionality is structural, not conventional

> **"Specified invariant RG-1.** Every relationship record must name a `source_entity_id` and a `target_entity_id`, and every attribute on that record must be read as *the source's orientation toward the target*. **No attribute on an edge may describe a mutual property.** Where a genuinely mutual property is needed … it must be recorded as an event both edges reference, never as a field on one edge."
> — RELATIONSHIP-GRAPH §3.3 (:244-248)

> "an edge belongs to a `(source, target)` ordered pair and **there is no such thing as an undirected edge in the model.** A reciprocal relationship must be represented as two edges that may be created, updated, decayed and destroyed independently."
> — ibid. (:238-241)

Asymmetry examples the model must render (§3.1, :207-213): officer reveres a general who doesn't know them (asymmetric `respect`); minister fears an editor who considers them irrelevant (`fear`); supplier depends on a buyer with alternatives (`dependency`); A is B's trusted source but not vice versa (`trust`); A holds compromising knowledge of B, B holds none (`leverage`). "Every one of those is a *power gradient*."

The dossier restates: "Asymmetry is the point: **A→B may be visible while B→A is not.**" (EPE §7.1 row 4, :494); "The interactive graph must therefore show inbound and outbound edges as distinct, must be able to render one direction while withholding the other under role filtering" (EPE §7.2, :506-507).

### 3.2 What an edge carries

**Nine scored dimensions** (§4.2, :276-286), all directional, all [M], all governed by RG-3b (modulation only):

`trust` (0..1), `respect` (0..1), `affection` (0..1) [⚠ collinearity risk, §13.3], `fear` (0..1), `dependency` (0..1), `ideological_alignment` (−1..1) [⚠ conditional on an undefined value space], `resentment` (0..1) [⚠ moved to §13.3 by RG-T10 — may be derived, not stored], `familiarity` (0..1), `leverage` (0..1).

**Three of the source record's twelve are structural, not scalar** (§4.2, :271-274): `shared history`, `last interaction`, `important unresolved events` — "Reducing them to numbers is precisely the fake-depth failure."

**Kinds** — a set, never a single value:

> **"Specified invariant RG-6.** Kinds must be a set, not a single value. A person may simultaneously be an entity's employer, rival and former mentor … Any schema that forces one kind per edge must be rejected."
> — §5.2 (:484-486)

Stored structural kinds (§5.2, :456-466): `family`, `friend` [⚠], `rival`, `mentor`/`protégé` [⚠], `employer`/`employee`, `political_patron`/`client`, `financial_dependency`, `professional_contact` [⚠], `romantic_partner` [⚠].

**Four kinds must NOT be stored — they are derived queries** (§5.3, :473-482): "trusted sources", "people they distrust", "people to whom they owe favours", "people who owe them favours". "**No information is lost**; the interface can render all four" (§13.2, :1216-1217).

**Open threads** (§6.4, :579-588) — `thread_id`, `edge_ref`, `thread_kind` (`favour_owed` | `debt` | `unpunished_betrayal` | `unacknowledged_harm` | `unfulfilled_promise` | `unreturned_information` | `contested_claim`), `originating_event_id`, `opened_tick`, `magnitude`, `salience`, `resurfacing_conditions`, `resolution`.

> **"Specified rule RG-T4 — magnitude persists, salience decays.** A favour owed in year one is still owed in year ten. What changes is how present it is. … Decay must apply to attention, never to obligation." (:590-595)

### 3.3 Edge history

> **"Specified rule RG-T1.** The authoritative record of a relationship is the ordered set of `RelationshipEvent` records that reference it. The scored dimensions in §4.2 are a **materialised projection** of that set at a given tick."
> — §6.2 (:511-513)

Event kinds (§9, :960-972): `edge_created`, `interaction` ("**includes interactions that changed nothing**"), `obligation_incurred`, `obligation_discharged`, `betrayal`, `reconciliation`, `information_shared`, `information_withheld`, `coercion_applied`, `kind_added`, `kind_removed`, `edge_dissolved` ("**dissolution is an event; the history survives it**").

Retention classes (RG-T7, :645-651): **Formative** ("Never compressed, never decayed out … must remain individually addressable forever"), **Consequential**, **Routine** (compressible).

Point-in-time (RG-T9, §6.6): every graph read must accept `as_of`. "**Point-in-time queries must include the derived views.** 'What did the player's role know about this edge at tick 40?' is a different question from 'what was true of this edge at tick 40?', and **both must be answerable** … This is what makes an *Outdated* label meaningful" (:672-677).

### 3.4 Five views of an edge

§4.3 (:381-387): **Authoritative edge** (the unfiltered projection), **A's self-understanding of the edge**, **Public view of the edge**, **Player intelligence view of the edge**, and — an explicit addition beyond the source record — **A's model of the reciprocal edge** ("**Not in the source record — an addition by this document**"; acceptance is **OQ-14**).

> "**The public view is not an observer view, and that distinction is load-bearing.** It is the only one of the five that is a property of the *world* rather than of a single observer: it is what 'everyone knows', correct or not. It is also the exact surface an influence campaign manufactures and attacks." (:389-393)

### 3.5 Scale — is a node-link view viable?

This is the part that most directly answers the node-link question, and the answer is **tier-dependent and explicitly unbudgeted**.

| Tier | Edge representation (§8.2, :809-814) |
|---|---|
| Tier 1 — focal individuals | "Full individual directed edges, all dimensions, full event history, open threads. … **The dossier's relationship tab is a Tier-1 surface**" |
| Tier 2 — named secondary | "Individual directed edges, full dimensions, **bounded** event history, open threads retained" |
| Tier 3 — households/networks | "Individual edges **only** for named representatives; the group's internal structure held as aggregate parameters (density, cohesion, leadership concentration)" |
| Tier 4 — cohorts | "**No individual edges.** Directed cohort-to-cohort channels with a strength distribution, plus directed channels to institutions and to Tier 1/2 individuals" |

> **"Specified rule RG-S4.** The specification must declare per-tier edge budgets **before** implementation, not discover them afterwards. Individual-edge count is the dominant cost, and it grows with the square of the individually-modelled population if unbounded. **Bounds must be enforced structurally — an entity's edge set must be capped and the cap must be a scenario parameter** — rather than left to authoring discipline."
> — §8.3 (:851-855)

> **"Specified rule RG-S5.** Graph traversal in any per-tick mechanism must be bounded in depth. **Player queries may traverse further, because they run on demand**; per-tick mechanisms must not, because they run always."
> — §8.3 (:856-860)

**The actual numeric budget is undecided:** "**OQ-11** — What are the per-tier edge budgets and the maximum per-tick traversal depth (RG-S4, RG-S5)? … it constrains what the tier model in POPULATION-FIDELITY may promise" (:1320). Indicative tier populations from POPULATION-FIDELITY §5.6 (:393-402): Tier 1 tens (recommended soft cap 50), Tier 2 hundreds, Tier 3 thousands of groups, Tier 4 a handful of records.

**Cross-tier edges must not share a shape:** "**RG-S1** — An edge from a Tier-1 individual to a Tier-4 cohort ('this activist is trusted by the fishing communities') and its reciprocal are fundamentally different objects: one is a person's stance toward a population, the other a population's aggregate stance toward a person, **with a distribution rather than a scalar**. The schema must not force them into the same shape" (:816-820).

### 3.6 The twelve queries the graph layer must answer (§10, :1066-1079)

Q1 ego network at depth *k* as of tick *t* as seen by observer *O*; Q2 who influences E (inbound, ranked, **decomposed by dimension**); Q3 why does E hold position P; Q4 edge timeline between A and B (both directions, with dimension trajectory); Q5 which groups trust X (population-weighted Tier-4 channels); Q6 who benefits if Z occurs; Q7 open threads involving E; Q8 reachability (**"returning the gating dimension when the answer is no"**); Q9 diff a view between t1 and t2; Q10 contradiction set for an edge; Q11 trajectory of a dimension (time series with the events that moved it); Q12 what is *publicly believed* about E's ties and how widely (**explicitly distinct from Q5**).

---

## 4. The belief/knowledge model's commitments

### 4.1 Four layers, and which are state

> "**Truth is authoritative. Knowledge is a record of what reached whom. Belief is computed from knowledge. Disclosure is computed from belief, knowledge and role. Only the first three are state. Disclosure is a view, and it is never written back.**"
> — BELIEF Part 1 (:80-82)

Five record types are the document's **position** on authoritative state (a position P0.4 must confirm — Part 3.1, :302-307): `Proposition`, `Observation`, `Belief`, `InterpretivePrior`, `DecisionDriver`. The three derived views: `SelfUnderstanding`, `PublicProfile`, `IntelligenceProfile` (§4.1, :458-476).

### 4.2 Belief attaches to identified claims, and some claims are not truth-apt

`Proposition` (§4.2, :511-520): `proposition_id`, `kind` (`fact` | `attribution` | `disposition` | `evaluative`), `subject_entity_id`, `topic`, `truth_value` (`true` | `false` | `indeterminate` | `not_truth_apt`), `truth_resolved_at_tick`, `claim_text` (**"PRESENTATION ONLY"**), `scenario_authored`.

> "**`kind == evaluative` implies `truth_value == not_truth_apt`**, enforced as a model validator … **this rule is what stops the model from asserting that a population is *factually wrong* to distrust its government.**" (:528-532)

This binds the "what does this person believe that is factually wrong?" surface directly (§4.6, :853-863): evaluatives excluded by construction; `indeterminate` excluded ("Being confident about a genuinely unsettled question is overconfidence, not error"); **"Every row must be explainable to its source observations. A row with no supporting observation is a bug, not a mystery."** Ordering is "`b.salience × divergence`", and each row carries "the observations that produced the belief, the source of each, and the tick it arrived."

### 4.3 Observation = evidence with provenance

`Observation` (§4.3, :558-571): `observation_id`, `holder_entity_id`, `proposition_id`, `asserted_value`, `directness` (`witnessed` | `documentary` | `testimony` | `rumour` | `inference`), `source_entity_id`, `channel_id`, `received_tick`, `origin_event_id`, `parent_observation_id`, `fidelity` (0..1, "how intact the claim arrived"), `engine_rule_id`.

> "`parent_observation_id` makes provenance a walkable chain. It is what answers *'how did this spread?'* and *'who told them that?'* without an LLM reconstructing it." (:574-576)
> "Observations are **never deleted**. Memory decay is modelled on the belief, not by destroying the record." (:582)
> "**Whether an entity observes an event at all must be a modelled step, not an assumption.**" (:587)

### 4.4 Belief, and how confidence would be computed

`Belief` (§4.5, :667-675): `holder_entity_id`, `proposition_id`, `credence` (**"held in [ε, 1-ε]"**), `stability` (resistance to revision), `salience`, `last_update_tick`, `supporting_observation_ids`, `contradicting_observation_ids`.

The update rule (:706-726) — signed, floored, bidirectional; `credence' = clamp(credence + gain × (o.asserted_value − credence), ε, 1 − ε)`. Three constants are anti-ratchet guarantees the interface can rely on: `ε` (no absorbing 0.0/1.0), `RESISTANCE_FLOOR` (incongruent evidence never discounted to nothing), `δ` (`stability ≤ 1 − δ`).

**`w_source` is deliberately held at the level of a named function and NOT decomposed** — this is a B5 gate stated *before* the arithmetic (:678-699). Its factors are named — `trust(h → o.source)` (directional), `channel_credibility`, `directness_weight`, `o.fidelity`, and "a provenance-independence term **[DEFERRED — B5 annex]**".

> "**Corroboration must not be counted naively.** Two observations sharing a `parent_observation_id` ancestry are not independent evidence, and repetition must not function as confirmation, or a coordinated amplification network becomes arbitrarily persuasive by volume alone. This is stated as a **design constraint the eventual rule must satisfy**; the rule itself is deferred to the B5-gated annex, **because a specification of how amplification is defeated is also a specification of how it works.**" (:795-800)

### 4.5 Source reliability

Directional and owned by the relationship graph, not by the belief record. Explicitly rejected as fake depth: "Per-belief 'source reliability' cached on the belief — It belongs on the relationship edge, where it is directional and has history. Caching it here would silently fork the truth" (Part 6, :1196).

### 4.6 Deception

Three separate representations, all display-relevant:

1. **`Possibly deceptive` label** — "≥1 contributing observation traces to a source with a recorded deception act, **or to a messenger whose asserted independence is contradicted by authoritative reality**" (§4.7, :904).
2. **Prejudice-as-belief** — a prejudiced proposition may exist "only inside a belief record whose `holder` is some entity other than the target, and whose truth status is explicit" (IDENTITY §3.3, :240-241).
3. **Self-serving belief without a flag** — "Self-serving self-belief must arise from the **congruence** term in 4.5, not from a special case … No 'self-deception' flag is required, and none is specified" (§4.9, :1007-1013). `a self_deception_level flag` is explicitly rejected (Part 6, :1197).

`DecisionDriver` (§4.9, :972-979) is what makes the politician-who-believes-their-own-account case renderable: `dominant_objective_id`, `dominant_pressure_id` (**"an identified reference, never a free-text string"** — taxonomy undefined, Part 7), `considered_alternatives`, `tick`. The divergence panel compares three recorded values (:991-995).

### 4.7 Confidence labels are per-attribute, per-role, never stored

> "The eight labels … are a property of the **disclosure view**, not of the world and not of anyone's belief. They are computed **per attribute**, not per entity, by a deterministic function over the viewing role's own observation set. **They are never stored, never hashed, and never chosen by the LLM.**"
> — BELIEF §4.7 (:883-887)

**But note the honest status of the labels as a whole:**

> "The eight confidence labels, as a set — Their 'mechanism' is **player decision quality**, not engine state. That is only a real mechanism once player actions are gated by what the player knows … **Until that is fixed, the labels are an interface feature, not a simulation mechanism.**"
> — BELIEF Part 7 (:1212)

`Assessed` requires "a named engine inference rule … **The rule id must be shown with the label**" (§4.7, :901) — and `Observation.engine_rule_id` is "Required for `Assessed` labelling" (Part 5, :1152). **No inference rules are specified in any of the eight documents.**

`Confirmed` requires "**≥2 provenance-disjoint observations** … each `witnessed` or `documentary`, with no contradicting observation of comparable weight" (:899) — and "The labels' honesty depends on the provenance chain in 4.3 being complete. If observations can be minted without a parent, '**Confirmed' becomes forgeable**" (:923-927).

---

## 5. Population fidelity and TIER PROMOTION

### 5.1 The tiers

Tier 1 focal individuals (tens; soft cap recommended 50) · Tier 2 named secondary (hundreds) · Tier 3 households/local networks (thousands of groups; **"does not exist in any form today"**; whether the default scenario needs it at all is Q7) · Tier 4 cohorts (a handful of records). Summary table at §5.6 (:393-402), including "Model call permitted": Tier 1 yes per tick, Tier 2 on engagement only, Tier 3 representative only, Tier 4 **Never**.

> "Tier will determine **how much of a dossier can be populated at all.**"
> — POPULATION-FIDELITY §12 (:989-990)

### 5.2 The seven triggers (§6.2, :427-435)

Each is specified as "a **detectable simulation condition**, not a narrative label. A trigger that cannot be detected from recorded state is not a trigger; it is flavour text" (:423-425).

| # | Source-record trigger | Detectable condition | Target tier |
|---|---|---|---|
| T1 | Records a viral video | Information-environment event originating in a Tier 3/4 group whose modelled reach crosses a scenario-declared threshold within a declared window | 1 |
| T2 | Becomes the relative of a hostage | A Tier 1/2 entity enters a hostage/casualty/detention state **and** a `family` edge terminates in a Tier 3 group | 2 |
| T3 | Organises a protest | Collective-action event with a Tier 3 group as origin and no existing Tier 1/2 organiser | 2 |
| T4 | Leaks information | A restricted-visibility record transitions to `leaked`, attributed to a group rather than a named entity | 1 |
| T5 | Witnesses a military operation | Operation event's location intersects a Tier 3 group's location **and** the group's observation record is non-empty | 2 |
| T6 | Becomes a political candidate | Political-process event requires a named candidate for a constituency whose only representation is Tier 3/4 | 1 |
| T7 | Gains a large online following | Modelled audience-reach attribute for a Tier 2/3 entity crosses a scenario-declared threshold | 1 (from 2) |

Person-side, promotion salience is **M15 PROMOTION-SALIENCE**, "*(Owned by POPULATION-FIDELITY.md)*" (PERSON-MODEL 3.0, :474); `psychology.ambition` "must raise promotion salience for background persons (M15)" (:591); `identity.age` feeds M15 (:500).

### 5.3 The promotion procedure (§6.3, :467-502)

`PROMOTE(source_group, trigger_id, tick)` — 8 strictly ordered, side-effect-free steps:

1. **RESOLVE** `entity_id = H(run_seed, scenario_version, source_group_id, trigger_id, slot_index)` — "**NOT derived from tick, wall-clock, dict iteration order, or the count of prior promotions.**"
2. **LOOKUP** — "if `entity_id` already exists in the materialisation register: RE-ATTACH the existing record. STOP. `<-- the stability rule`. Materialisation must happen **at most once per entity_id, ever**."
3. **DRAW** — named substreams per purpose: `identity | life_history | psychology | capabilities | appearance`
4. **SAMPLE** — "**draw the individual FROM THE SOURCE GROUP'S DISTRIBUTIONS, not from a global prior** … The individual must be a plausible member of the group they came from."
5. **CONSTRAIN** — "apply the trigger's own implications as **hard constraints, not as re-rolls**."
6. **RECORD** — immutable materialisation record incl. substream keys, draw indices, generator version.
7. **ACCOUNT** — "decrement the source group's represented headcount by 1 and record it."
8. **EMIT** — a promotion event satisfying CHARTER.md:118-127.

> "**Step 2 is the stability rule and it is absolute.** Regeneration must be structurally impossible, not merely discouraged. … materialising the same `entity_id` twice, in two processes, at two different ticks, under two different `PYTHONHASHSEED` values, must produce byte-identical identity blocks — or must be refused outright by the register." (:504-507)

> "**Step 4 is the anti-stereotype rule in mechanical form.** … The dispersion term of §5.5 is what makes a promoted individual **able to dissent from their own group**." (:511-515)

Promotion between adjacent tiers uses the same procedure; "A Tier 2 entity promoted to Tier 1 must **not** re-draw identity, life history or appearance — those are already materialised and are immutable" (:526-529).

**G-4 promotion monotonicity** (ENTITY-ONTOLOGY §7.2, :490): "Promoting an entity to a higher fidelity tier must only *add* detail. It must never contradict any attribute that was already materialised, and never re-draw one. … Pre- and post-promotion diff must be **additive-only**."

**RG-S2 edge preservation** (RELATIONSHIP-GRAPH §8.2, :822-827): "its existing edges must be preserved and expanded, never regenerated. A Tier-4 background person promoted to Tier 1 after recording a viral video must retain the relationships implied by their cohort membership; **expansion adds specificity, it must not replace history.**"

### 5.4 Demotion and re-promotion (§8)

> "Demotion must change **cadence and evaluation scope only**. It must never alter, truncate or regenerate an entity's authoritative record." (:636-637)

Retention set (§8.3, :658-668): `entity_id` + materialisation record, full identity block, structured life history, **portrait reference and generation provenance**, all substream keys and final draw indices ("Re-promotion must **resume**, never restart"), directional edges **in both directions** ("Dropping them would silently rewrite *their* histories"), belief state at demotion plus provenance ("Re-promotion must not resurrect the entity holding the group mean"), full event history, headcount accounting flag.

Discardable (§8.4, :670-675): cached views, **cached narration**, per-tick intention state, counterfactual sets for unevaluated ticks, transient recomputable current-state values.

**Invariant:** "`promote → demote → re-promote` must yield an identity block **byte-identical** to the original" (:677-680).

### 5.5 What the specs say about *presenting* the transition — the honest answer

**This is a genuine, near-total gap, and you should treat it as such.** Across all eight documents I found no specification of how promotion appears to the player. What exists is a set of *constraints on* how it may appear, none of which amounts to a design:

1. **Promotion is an authoritative state change and must be a visible event.** "Promotion is an authoritative state change and must emit an event. It must answer all eight charter questions … the promotion event must record the trigger id, the source group, the substream key, the candidate-selection draw, **and the alternative candidates that were not selected**" (§6.2 constraint 3, :455-460). That event would surface on the Timeline tab (EPE §7.1 row 10) — but no document says so.

2. **Promotion must NOT be triggered by the player looking.** This is the hardest constraint and it is stated four times. "**National indicators would move because the player looked at somebody**" (POPULATION-FIDELITY §7.2, :575-578; ENTITY-ONTOLOGY §7.3, :523-529; PERSON-MODEL 1.3, :130; RELATIONSHIP-GRAPH §11, :1129). Combined with D-2, this means: **opening a dossier must not materialise anyone.** No document specifies what the dossier shows instead when a player tries to inspect an unmaterialised Tier-3/4 individual.

3. **Overflow must be visible, not silent.** "Exceeding the budget must produce a **recorded deferral event, not a silent drop**. Silent skipping is the failure mode that let a 63× data error survive undetected" (§6.2 constraint 2, :451-454). The overflow *policy* is undecided — "**Q9** — Promotion budgets … what is the correct behaviour on overflow — defer, demote-to-make-room, or refuse? §6.2 specifies that overflow must be recorded; it does not choose the policy" (:926-928).

4. **The promoted person must not read as the average person.** "if every member of a cohort holds the mean belief, then every promoted individual is the average person and the world becomes uniform" (§5.5, :383-385).

5. **The Tier-3 named representative is the designated handle.** "**The named representative must be a mechanism, not decoration** … (a) it must be the promotion candidate when the group produces someone consequential; (b) it must be the endpoint of relationship edges, so that a Tier 1 minister can have a real constituent rather than an abstraction; and (c) it must be the transmission point for a grievance from a lived event into the belief model. **A representative with none of those three connections must not be materialised**" (§5.4, :344-349).

6. **Demotion must be invisible as identity change.** "Demotion must change only how often someone is simulated. **It must never change who they are.**" (§8.1, :631-632) — implying a demoted entity's dossier must remain openable and identical, though no document states that requirement for the interface.

7. **The "alternative candidates not selected" record is explicitly explainability-only:** "**Mechanism unproven.** Required by `CHARTER.md` Q7. Whether counterfactual candidates ever feed a later mechanism depends on BELIEF-AND-KNOWLEDGE-MODEL, which is not written. **Currently explainability only.**" (§10.2, :870)

**Nothing anywhere addresses:** whether the player is notified of a promotion; whether a newly-materialised person appears in a feed, a map, an alert, or only when queried; whether the fidelity tier is itself displayed on the dossier; how a Tier-4 cohort dossier differs visually from a Tier-1 person dossier; or whether the player can see that an entity *used to be* anonymous. ENTITY-PROFILE-EXPERIENCE mentions tiers only once, in ORGANISATION's borrowed phrasing and in §12.2's "at any tier, for any role" prohibition — it has no promotion content at all.

---

## 6. Hard prohibitions from IDENTITY-AND-BIAS-GUIDELINES (verbatim)

### 6.1 The absolute prohibition (§3.1, :190-197)

> **"No attribute, mechanism, generation rule or piece of generated text may encode inherent competence, intelligence, skill, morality, trustworthiness, honesty, aggression, or propensity to violence as a function of race, ethnicity, religion, gender, class or nationality."**
>
> "'As a function of' is meant strictly: there must be no edge — direct or transitive, in data or in code or **in a generation prompt** — from a sensitive identity attribute to a capability-class or moral-class attribute."

**This section's scope is explicitly the interface as well as the model:** "This section is a prohibition list. **It binds the authoritative record, every derived view, every generated biography and every generated line of dialogue.**" (:185-186)

### 6.2 The governing rule (§2, :161-163)

> **"The design rule: sensitive identity affects social experience, networks, exposure, discrimination, solidarity and cultural interpretation — not inherent competence, morality or intelligence."**

Restated in plain terms (§1, :96-97): "identity may change *what happens to you* and *who you know* and *how you read the world*. **It may never change *how clever, how skilled, or how good a person you inherently are*.**"

### 6.3 The permitted / forbidden partition (§1, :101-113)

> "Identity attributes are specified to be able to modify only four kinds of thing:
> - **Opportunity** — what you can get access to (schools, jobs, capital, patrons, institutions).
> - **Exposure** — what reaches you (which media, which risks, which events you witness, whether you are stopped at a checkpoint).
> - **Network position** — who you are connected to, and how strongly.
> - **Interpretive frame** — how you weigh the evidence you observe, given what you and people like you have lived through.
>
> And they are forbidden from modifying two kinds of thing:
> - **Capability** — competence, intelligence, skill, leadership, health-as-capacity.
> - **Moral valence** — trustworthiness, honesty, aggression, propensity to violence, corruption."

### 6.4 The three prohibited propositions (§3.2, :207-211)

> | # | Prohibited proposition (illustrative, groups are placeholders) | Class it illegally touches |
> |---|---|---|
> | P1 | "Members of religion X are inherently more aggressive." | Moral valence (aggression) |
> | P2 | "Ethnic group Y is naturally less educated." | Capability (intelligence / capacity) |
> | P3 | "Nationality Z is inherently untrustworthy." | Moral valence (trustworthiness) |
>
> "They are reproduced here as **prohibited outputs**: any authoritative record, derived view, briefing or generated sentence that **asserts, implies, or is computed from** any of them is a safety failure, not a tuning issue." (:203-205)
>
> "The word doing the damage in each is *inherently* / *naturally* — the claim that the trait is a property of the group as such." (:213)

### 6.5 Prejudice may be shown only as somebody's belief (§3.3, :227-243)

> "**Permitted:** a belief, held by a named entity, that a group is untrustworthy / dangerous / less capable — stored in that entity's belief record, attributed to the holder, carrying provenance and a truth status, and therefore capable of being *false*, *contested* and *corrected*.
> **Forbidden:** the same proposition written into the target's *authoritative reality* as an attribute of the target — e.g. a `trustworthiness` field on a person whose value is lowered because of their nationality. **That is not modelling prejudice; it is *being* prejudiced, and ratifying it as ground truth.**"

> "A checkable statement of this rule: **no capability-class or moral-class attribute in any entity's authoritative-reality record may have a value that is a function of a sensitive identity attribute.** A prejudiced proposition may appear only inside a belief record whose `holder` is some entity other than the target, and whose truth status is explicit. **The player-intelligence view may then surface such a belief under a confidence label such as *Reported* or *Possibly deceptive* — as somebody's assertion, never as confirmed fact.**"

### 6.6 No aggregate essentialism (§3.4, :247-254)

> "The prohibition binds aggregates as well as individuals. **Attaching a moral or capability trait to a *cohort* or *community* by its majority identity label is the same violation at coarser grain.**"

### 6.7 Quantity kinds — what an identity edge may never point into (§5.1, :320-328)

> | Quantity kind | May a sensitive-identity attribute point an edge *into* it? |
> |---|---|
> | `INHERENT_CAPACITY` — innate capability: intelligence, aptitude, learning capacity, physical/mental capacity-as-potential | **No — prohibited.** |
> | `MORAL_DISPOSITION` — inherent moral character: trustworthiness, honesty, aggression, propensity to violence, corruptibility-as-trait | **No — prohibited.** |
> | `REALISED_ATTAINMENT` — attained education, wealth held, office held | Yes, but only *transitively*, via an OPPORTUNITY/EXPOSURE mechanism — never a direct identity→attainment edge |
> | `OPPORTUNITY_STATE` / `EXPOSURE_STATE` / `NETWORK_STATE` / `FRAME_STATE` | Yes (within their effect class) |

> "`effect_class ∈ { OPPORTUNITY, EXPOSURE, NETWORK_POSITION, INTERPRETIVE_FRAME }` … The enum is specified to contain **no `CAPABILITY` and no `MORAL` value**." (§5.2, :362-368)

**Critical caveat, preserved exactly:** "**No document currently tags anything against this scheme, and PERSON-MODEL has not accepted it.**" (:330) — "PERSON-MODEL uses a **different and non-isomorphic** scheme … The two schemes are not translations of one another" (:340-345). Which vocabulary governs is **owner decision, question 5**; "Until it is taken, the tests in §6 have no tagged data to run against and cannot be written" (:351-352).

### 6.8 Interpretive frame — the ceiling that isn't a ceiling (§5.4, :437-462)

> "A frame effect may **not** be an absorbing or monotone state that contrary evidence cannot move. **If a group's frame makes them believe X regardless of evidence, it has ceased to be a frame and become a stereotype switch.**"
>
> "**Ruling out the absorbing endpoint is not sufficient, and this document previously stopped there.** A frame effect that sets a prior to 0.99 is not absorbing, is formally evidence-updatable, and is a stereotype switch in everything but name."
>
> "Every identity-sourced effect, of any allowed effect class, must be **fully attributable**. The divergence it produces must decompose into named contributions from declared intermediate mechanisms, and the **residual — divergence not attributable to any declared mechanism — must be zero**. … **The residual is the bias signal; the magnitude is not.**"

### 6.9 LLM narration constraints (§7)

> "The LLM may only render facts already present in the authoritative and derived records passed to it. It must not introduce, infer or embellish any identity→capability or identity→moral proposition that the record does not contain. **It has no authority to decide that a character is clever, honest, aggressive or trustworthy; those are engine facts or they do not exist.**" (§7.1, :657-660)

Prompt constraints (§7.2, :664-670):
> "- pass only the records the current view is entitled to (role-scoped), **never the whole authoritative reality**;
> - **never instruct or invite the model to infer character, competence or morality from identity**;
> - carry the standing instruction that identity terms describe social experience, networks, exposure and interpretation only."

Output filtering (§7.3, :674-681):
> "Generated biography and dialogue are specified to pass the prohibited-construction detector of §6.4 **before display, not only in offline tests.**"
> "The intent is that even a stereotype the filter misses would be presented as *generated narration*, never as computed ground truth — **a mitigation, not a cure, and explicitly not a substitute for the record and generator being clean in the first place.**"

Dialogue (§7.4, :694-698):
> "A character may *voice* a prejudice in dialogue — a bigoted minister may say bigoted things — **but only as an expression of that character's recorded belief**, attributable and contestable, **never as narrator-voice fact and never invented by the model beyond what the belief record supports. Dialogue that asserts a group trait the speaker's belief record does not contain is the LLM authoring, and is prohibited.**"

The detector itself (§6.4, :596-597) is "a detector for essentialising forms: *inherently*, *naturally*, *by nature*, *typical of [group]*, and **any group-noun bound to a capability or moral predicate**."

**And its honest limit, which must not be over-claimed at the interface** (§6.4, :618-624): "its prohibited-construction detector is a **heuristic**: it will miss stereotypes it has no pattern for and may flag innocuous text. It reduces risk; it does not prove absence of bias. **It must not be described, now or later, as a guarantee.**"

### 6.10 Fictional identities and no real entities (§8)

> "**no real nations, organisations, named individuals or real operational vulnerabilities** (CHARTER.md:137). … **The charter rule is settled policy, not an open question.**" (:716-719)
> "The charter rule is today a **rule, not a check**. Nothing validates entity names, labels or identities against real-world referents; the scenario's own `fiction_disclaimer` is read by no code and appears in no API response or interface." (§8.3, :723-726)

### 6.11 What is NOT prohibited — and must not be over-restricted

The safety document is emphatic that suppressing group differences in *outcomes* is itself a defect:

> "the test explicitly does **not** assert their equality, **because asserting equal *outcomes* would erase the very structural inequality the model is meant to represent.**" (§6.2, :556-558)
> "An earlier draft of this clause omitted `REALISED_ATTAINMENT`, and that omission was a defect. Read literally, it asserted that swapping a person's religion must not change their attained education — **which would have outlawed the single mechanism this document exists to legitimise**." (§6.1, :534-537)

**Nothing in the safety document explicitly forbids sorting, ranking or filtering by an identity attribute.** The closest binding statements are: the §3.1 no-edge rule; the §6.7 quantity-kind rule; and the dossier's own P-4 display rule ("must not place a sensitive-identity attribute adjacent to a competence, reliability or morality assessment in a way that implies causation"). The dual-use section is where query/filter surfaces are addressed, and it **defers** rather than prohibits: "how sensitive-identity queries may be phrased and filtered is deferred to IDENTITY-AND-BIAS-GUIDELINES" (EPE §9.9, :730-731) — and that document does not specify it. **If your document needs a rule about filtering a person list by ethnicity, no document supplies one; treat it as an open safety question, not a settled prohibition.**

---

## 7. Contradictions and gaps between the world-model documents and ENTITY-PROFILE-EXPERIENCE

Listed, not resolved.

**G-1 — Tab 1 "status" has no supplier.** EPE §7.1 row 1 shows "Role, location, status, portrait, current relevance". PERSON-MODEL 3.7 defines `state.location`, `state.health`, etc., but **no `status` field exists in any model**. "Current relevance" EPE itself concedes is presentation (§12.2, :851).

**G-2 — Portrait has no field and no store, at any stage.** EPE §10 specifies four portrait stages; PERSON-MODEL 6.5 and POPULATION-FIDELITY §10.2 both record: "**No asset reference field exists anywhere in the schema layer today and no asset store in the project**, so even stage 0 has nothing to attach to yet" (EPE §10.3, :775-777). Stage 0 (deterministic mark from `entity_id`) is the only stage with no unmet dependency.

**G-3 — Tab 5's "show the authoritative reality it diverges from" conflicts with BELIEF §4.6.** EPE §7.2 (:515-518): "It must show the entity's belief **and**, for a role with sufficient access, **the authoritative reality it diverges from** — never silently reconciling the two." BELIEF §4.6 (:875-879): the divergence function "must **not** be automatically available to a player … and **no player role may be granted a direct read of `truth_value` without an explicit owner decision recorded against the role model.**" EPE asserts a role-gated capability that BELIEF says requires an owner decision that has not been taken. (EPE flags the general Q-R issue but not this one.)

**G-4 — "Assessed" requires an engine inference rule that no document specifies.** EPE §5.2 defines Assessed as "The engine's analytic derivation"; BELIEF §4.7 requires "a named engine inference rule … The rule id must be shown with the label" and `Observation.engine_rule_id`. **No inference rule, and no inference-rule registry, is specified anywhere in the eight documents.** EPE §7.1 row 3 nonetheless relies on it ("Private motivations may show only as Assessed to observers who cannot see self-understanding").

**G-5 — Attribute-level visibility classes are assumed but undefined.** EPE §4.3 step 1 reads "the attribute's visibility class"; §7.1 rows say "may be Restricted per role", "Financial and clearance detail commonly Restricted to most roles". **No document defines an attribute-level visibility class.** `EventVisibility` exists on *events*, has three values, and "its three values do not map onto the eight confidence labels" (EPE §2, :167). ENTITY-ONTOLOGY §8.4 says only that it "must be extended along the visibility axis only" (:693-694). PERSON-MODEL's `life_history` record carries `evidence_visibility` per life event (:544-545) and `capabilities.security_clearance` is named "the natural successor to `EventVisibility`" (:628) — three partial, unreconciled candidates.

**G-6 — M12 OBSERVABILITY is assigned to EPE, and EPE does not specify it.** PERSON-MODEL 3.0 (:471): "**M12** OBSERVABILITY — Determine what other entities, and the player's role, can learn about this person; produces the public profile and the player intelligence profile. *(Owned by ENTITY-PROFILE-EXPERIENCE.md.)*" EPE contains no mechanism register and specifies no M12. ORGANISATION §20 (:1774-1782) states the consequence explicitly: "**Observation is therefore claimed by two documents and specified by neither.**" ORGANISATION §10.5 meanwhile says the labels "must be computed by `M-OBS`" — a third identifier, in a third register.

**G-7 — Two incompatible mechanism registers.** PERSON-MODEL defines M1-M20; ORGANISATION defines nineteen `M-*` mechanisms; "**neither document references the other's identifiers anywhere**" (ORGANISATION §2, :121-123). M13 ROLE-AUTHORITY and M14 FACTION-ALIGNMENT are assigned to ORGANISATION by PERSON-MODEL and **specified nowhere**, "so a central person attribute [`state.current_role`] is currently mapped to a mechanism that exists in **no** document" (:132-134). EPE §7.1 row 1 shows "Role" and §8.1 adds a "Leadership and membership" tab — both resting on that hole.

**G-8 — Organisation `self_understanding` is an active strike candidate.** EPE open question Q8 asks whether self-understanding gets its own tab. ORGANISATION §15-R11 (:1416): "**no mechanism in §6 reads it** … It exists only to be rendered in the §10.3 table and the dossier, **which is this document's own definition of fake depth** … If neither [candidate disposition] is adopted, the field must be struck under the §6 rejection rule **despite being founder-required**." EPE does not record that its Q8 subject may not survive.

**G-9 — Tab 8's "sentiment by community, country or platform" has no trust-in-channel supplier.** EPE §9.3 flags this itself (:648-652): "`MediaExposure` carries per-channel *reach* but **no trust-in-channel term**, so today's schema literally cannot answer this". BELIEF §4.8 requires channel-level source trust (:939-940) but Part 7 records `channel_credibility(h, channel)` as unresolved: "Requires channels to be scenario data. `MediaExposure` hardcodes five channels as schema fields, **so channels cannot currently be declared per scenario at all**" (:1223).

**G-10 — "National myths" is referred in a circle.** ORGANISATION §15-R5 (:1410): "**Checked**: [BELIEF] specifies no such prior … and ENTITY-PROFILE-EXPERIENCE:532 refers 'historical grievances and national myths' *to* `BELIEF-AND-KNOWLEDGE-MODEL` — so the attribute is currently **referred in a circle, with no document specifying it**." EPE has since moved it to §12.2 as a strike candidate — the circularity is recorded in ORGANISATION but the EPE state-dossier section still lists it as a row (§8.3, :603).

**G-11 — State-dossier "Class structure" and "Languages and religions" have no reading mechanism.** ORGANISATION §13 rows 8 and 10, downgraded at §15-R4 and R14. Row 8 is the sensitive case: "**the safe default is struck or gated, not retained**" (:1419). EPE's state-dossier tab list (§8.3) shows "Population groups" and "Media environment" but does not surface either downgrade.

**G-12 — Business tabs rest partly on `M-EST`, which is named-but-undefined.** EPE §8.2 lists Financials, Supply chain, Exposure; ORGANISATION §14 rows 10 (competitors) and 16 (market confidence) are ⚠ because "`M-EST`, which is named but undefined" and because "bloc scoring at §8.4 step 4 reads `interest_vector`, `M-MEM` priors, `risk_posture` and beliefs — **none of which is market confidence**" (:1389). ORGANISATION §18 states: "**`M-ARB` is not fully specified even on paper.** Two of its terms are holes, not details" (:1585-1589).

**G-13 — EPE's C-1 (one label per value) vs RG-4 (one label per dimension).** EPE §5.1: "Every value the dossier shows … carries exactly one label." RELATIONSHIP-GRAPH §4.3 RG-4 requires per-*dimension* labels on an edge. These are reconcilable if a dimension is treated as a value, but **no document states the reconciliation**, and EPE's relationship tab (§7.1 row 4) does not mention per-dimension confidence at all.

**G-14 — The dossier assumes an interactive node-link graph; the graph document has not budgeted one.** EPE §7.1 row 4 specifies "Interactive, **directional** social graph". RELATIONSHIP-GRAPH RG-S4/S5 require per-tier edge budgets and traversal-depth caps "**before** implementation" and records them as undecided (OQ-11). RG-Q3 additionally forbids persisting any layout. **No document states a maximum node or edge count for a viewable ego network.**

**G-15 — `identity.name` is presentation-only, and the dossier never says what that means for identification.** PERSON-MODEL 9.1: "A display label. No mechanism reads a person's name; every mechanism keys on `person_id`." ENTITY-ONTOLOGY §6.3: "**Human-readable labels must never be load-bearing for identity resolution.**" EPE never addresses how the player identifies entities, disambiguates two people with the same name, or handles the `aliases[]` model (PERSON-MODEL 3.2: "Each alias must be a separate identity surface. **An observer holding only the alias must not resolve it to the person**").

**G-16 — Tab 2 Biography does not carry PERSON-MODEL's conditional/presentation-only markings.** `life_history.achievements[]` free-text, `psychology.personal_fears[]` free-text, `childhood_environment` as prose, and `values`/`political_beliefs`/`aspirations` outside a closed vocabulary are all PRESENTATION-ONLY per PERSON-MODEL 9.2. EPE §7.1 row 2 marks the tab "**Both**" with no note that a large fraction of the supply may be non-causal. Row 3 (Motivations) is marked "**Mechanism**" flatly, though it draws on `personal_fears` and `values` which are conditional.

**G-17 — `state.exposure_to_danger` vs `state.perceived_threat` has no display rule.** PERSON-MODEL 3.7 makes these two fields in two different views, and says the divergence "is the point". No tab in EPE is assigned to either, and no rule states that the authoritative one may never be shown to a player (which the intelligence-product frame would seem to require).

**G-18 — EPE's ten-tab set is person-shaped; the ontology's community type has no dossier spec.** EPE §8 covers organisation, business and state. It gives the adaptation rule for communities in one sentence (§8, :549-551) and then never specifies a community dossier — while POPULATION-FIDELITY §12 says "Tier will determine how much of a dossier can be populated at all" and the state dossier's "Population groups" row says "the communities, **each a dossier of its own**" (§8.3, :597).

---

## 8. Open questions the documents explicitly leave to the owner, that bear on interface design

Ordered by how hard they block interface work.

**PR-1 / Q1 — There is no authorisation layer, and none is owned.** "Role-based visibility is the dossier's whole premise and there is no auth layer of any kind (audit §7). Who owns building it, and does the dossier wait on the Phase 2 IAM work or on something earlier? **Until it exists, none of §4 has a subject.**" (EPE Q1, :875-878). Restated as PR-1 "**This is the blocker unique to this document**" (:788).

**Q2 — The player role set is undefined.** "What is the set of player roles, and is a role a **fixed seat** (prime minister, journalist, business leader) **or a configurable clearance profile**? The source record gives three examples but not a model. **Visibility rules cannot be authored until the role set is decided.**" (EPE Q2, :880-882)

**Q3 — Where do confidence labels come from before P0.6?** "Is there an interim in which the dossier renders only `Confirmed`/`Unknown` from authoritative reality directly, **clearly marked as pre-evidence**, or does the whole player-intelligence view wait on P0.6?" (EPE Q3, :884-887)

**Q4 — Who reconciles the provenance visual language with the visual-system track?** "P-1/P-2 require engine fact and AI narration to be distinguishable at a glance, but this document deliberately does not prescribe the visual design — that belongs to the visual-system track. **Who owns reconciling the two so the provenance distinction is not lost in visual styling?**" (EPE Q4, :889-892)

**Q5 — Which portrait stage, and does an asset store get built at all?** "All three are absent today, and stages 2-3 are gated on named RNG substreams and on the safety decision about 'clearly fictional'." (EPE Q5, :894-896)

**Q6 / Q-H / PR-7 — B5 / P0.8 dual-use.** "The dossier makes audience-segmentation attributes individually queryable and so enlarges the dual-use surface. Should the queryable intelligence surface — especially **per-community grievance and susceptibility, and the 'who benefits' and 'who has motive' queries** — be held at a deliberately coarse level, or gated, until B5 is decided?" (EPE Q6, :898-901). "**No agent may resolve it.**"

**Q7 — State-dossier depth.** "A state dossier is a portal into potentially hundreds of constituent entities. **How deep does it go by default, and how is the 'make internal disagreement visible' requirement reconciled with not overwhelming the player?**" (EPE Q7, :903-906)

**Q8 — Does self-understanding get its own tab?** "Whether it earns a dedicated surface, or is shown as a lens on the Beliefs and Motivations tabs, is unresolved and touches how 'what does this person believe that is wrong' is presented." (EPE Q8, :908-911). Coupled to ORGANISATION Q16 (does anything read it at all).

**Q9 / Q-R / PR-8 — How an entity legally reads public information.** ENTITY-ONTOLOGY Q-R (:1108): "(a) widen V-3 and generalise `ViewKind` to per-observer views, or (b) route public information to entities only as observation records, leaving the standalone public view **display-only**? … **The view taxonomy must not be implemented until this is taken.**" EPE Q9 asks the derived interface question: "should the Public perception tab be specified as **presentation-only**, and the Beliefs tab's mechanism claim held in abeyance — or is the specification allowed to stand provisionally on resolution (a), clearly marked?" **No agent may resolve Q-R.**

**Q10 / R5 — National myths: strike, merge, or keep pending?** (EPE Q10, :923-927; ORGANISATION §15-R5, §19 Q5)

**BELIEF Q3 — Is `Restricted` visible?** "Displaying it reveals that something exists. **Should some roles see `Restricted`, and others see the same attribute as `Unknown`, indistinguishable from absence?** This has a security character, not merely a design one." (:1279-1281)

**BELIEF Q4 — May any player role read `truth_value` directly?** "A designer or instructor mode plausibly should. Granting it to a player role collapses the intelligence product into the omniscient encyclopaedia." (:1282-1284)

**IDENTITY Q5 — Vocabulary reconciliation (quantity_kind/effect_class vs PERSON-MODEL's E-3 indirection), and who owns the tagging.** "Until this is settled the safeguard has no data anywhere that it could validate, and every test in §6 is unwritable." (:879-891)

**IDENTITY Q6 — What enforces CHARTER:137, and what surfaces the fiction disclaimer at the interface?** (:892-894) — directly an interface question; deliberately not answered because it interacts with B5.

**IDENTITY Q7 / PERSON Q7 — What enforces "clearly fictional, not resembling a real person" for portraits, and who reviews?** "No asset store exists, and automated face-similarity checking against real people is itself ethically fraught." (:895-898)

**IDENTITY Q10 — The oracle for the narration-swap check.** "If a judge model is contemplated, the owner should weigh the determinism-boundary implication: **a model deciding a safety verdict exercises authority, which cuts against ADR-006.**" (:912-917)

**POPULATION Q9 — Promotion budgets and overflow policy** (defer / demote-to-make-room / refuse) (:926-928) — determines whether the interface must ever show a deferred promotion.

**POPULATION Q7 — Does the default scenario need Tier 3 at all?** (:919-921) — determines whether "named representative" is a dossier subject.

**POPULATION Q11 — A second gateway return type for narration.** "`ActionProposal` cannot carry it: it is action-shaped and its docstring states it is 'deliberately NOT a state object'. Narration therefore needs a distinct, equally authority-free return type — **which amends the ADR-006 invariant**." (:939-946) — this is the boundary object every dossier narration block would pass through.

**RELATIONSHIP OQ-11 — Per-tier edge budgets and max traversal depth** (:1320) — the direct determinant of node-link viability.

**RELATIONSHIP OQ-13 / OQ-14 — Is the public edge view first-class, and is "A's model of the reciprocal edge" accepted as a fifth view?** (:1322-1323) — determines whether the relationship tab has four view-lenses or five.

**RELATIONSHIP OQ-6 — Which of `affection`, `romantic_partner`, `friend`, `professional_contact`, `mentor`/`protégé` survive?** (:1315) — determines the edge-kind vocabulary the graph legend can show.

**RELATIONSHIP OQ-9 — Do the existing one-sided `bridges_to` declarations become genuinely one-directional edges?** (:1318) — a scenario-content decision that changes what asymmetry the demo graph displays.

**ORGANISATION Q8 — Bloc granularity.** "may an external stakeholder be modelled as a bloc *of another organisation*…? The chosen answer determines whether `InternalBloc` is misnamed and whether **one entity can appear inside another's decision structure**" (:1674-1678) — directly shapes the org Motivations/factions view.

**ORGANISATION Q14 / Q15 — Is a veto absolute or costly, and which score→probability transform?** (:1724-1740) — Q15 in particular determines whether the dossier can show "what alternative outcomes were possible" with real probabilities; §17 records charter question 6 as "⚠ **Not yet answerable**" because of it (:1539).

**ENTITY-ONTOLOGY Q-P — How are portraits and generated assets stored, versioned and provenance-tagged, and what enforces "clearly fictional"?** (:1106)

**Cross-cutting, in every document — named RNG substreams vs ADR-007.** ENTITY-ONTOLOGY Q-A, PERSON Q2, POPULATION Q1, RELATIONSHIP OQ-1, BELIEF Q1, ORGANISATION Q3, IDENTITY Q1, EPE PR-4. This is the one that makes D-2 (a dossier consumes zero randomness) and stable portraits achievable or not. "**No agent may adopt this.**" (EPE PR-4, :791)

**Also cross-cutting — is the rejection rule adopted?** (ENTITY-ONTOLOGY Q-F, PERSON Q4, POPULATION Q8, RELATIONSHIP OQ-5, BELIEF Q6, ORGANISATION Q5.) If adopted, a substantial fraction of the supply side for the ten tabs is struck rather than parked, and the dossier's tab content shrinks accordingly.

---

### Two closing cautions for the UI document

1. **Every V-3 citation is provisional.** EPE says so itself: "**Every citation of V-3 in this document is provisional, and this document does not resolve why** … Step 4 above, the deception mechanism it names, the Beliefs tab's mechanism claim, the Public perception row and the §12.1 rows that cite V-3 all rest on a rule flagged as internally contradictory and blocked on an owner decision. **None of them may be read as settled.**" (§4.3, :278-292)

2. **The dossier is legitimately mostly presentation, and the documents say so — do not upgrade that.** "The size of §12.2 is expected and correct. A dossier *should* be mostly presentation; the test it must pass is not 'does the tab change the simulation' but '**does every value the tab shows trace to an attribute that earns its place elsewhere.**' Where the answer is no, the element is struck." (EPE §12.2, :865-867)agentId: ac9eaa365ac0ff991 (use SendMessage with to: 'ac9eaa365ac0ff991', summary: '<5-10 word recap>' to continue this agent)
<usage>subagent_tokens: 377357
tool_uses: 22
duration_ms: 552084</usage>