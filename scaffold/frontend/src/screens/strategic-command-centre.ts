/**
 * Strategic Command Centre — C0.
 *
 * DESIGN INTENT: the societal propagation chain is the visual spine of this screen. That is the
 * deliberate move that stops it reading as a military map, a chatbot, a generic metrics dashboard
 * or a cabinet-only interface. The centre of the screen is a crisis moving through insurers,
 * carriers, workers, households, media, families and politics — people and institutions, not units
 * on terrain.
 *
 * EVERYTHING HERE IS FIXTURE DATA. The chain is hand-authored (founder decision G3) and must never
 * be described as computed, simulated, live or emergent. MERIDIAN's tiers do not causally
 * influence one another today.
 */

import type { ChainHop, Claim, Panel, QueueItem, ScenarioFixture, StreamEvent } from '../fixtures/types.ts'
import { absenceValue, confidenceChip, epistemicChip, escapeHtml } from '../components/epistemic.ts'
import { card, provenanceLine } from '../components/provenance.ts'

function chainHop(hop: ChainHop): string {
  const unresolved = hop.epistemic_status === 'UNKNOWN'
  const entities = hop.entities
    .map((e) => {
      // Founder decision G1: non-materialised entities are aggregate/minimal-reference only.
      // Selecting one must never generate biography, beliefs or identity.
      const cls = e.materialised ? 'ent ent--materialised' : 'ent ent--aggregate'
      const title = e.materialised
        ? `${e.name} — materialised fixture entity`
        : `${e.name} — aggregate only. Not materialised; no individual detail exists.`
      return `<span class="${cls}" title="${escapeHtml(title)}">${escapeHtml(e.name)}${
        e.materialised ? '' : ' <span class="ent__tag">aggregate</span>'
      }</span>`
    })
    .join('')

  // Ranked contributors, each naming its mechanism (research T18 — one of the few fact-checked
  // findings: an aggregate that cannot name what drove it does not ship). Rendered inline rather
  // than as a stacked list so eight hops fit above the fold without hiding the mechanisms.
  const contributors = hop.contributors.length
    ? `<ul class="contribs">${hop.contributors
        .map(
          (c) =>
            `<li><span class="contrib__w" data-w="${escapeHtml(c.weight)}">${escapeHtml(c.weight)}</span>
             <span class="contrib__label">${escapeHtml(c.label)}</span>
             <span class="contrib__via" aria-hidden="true">via</span>
             <span class="contrib__mech">${escapeHtml(c.mechanism)}</span></li>`,
        )
        .join('')}</ul>`
    : ''

  return `<li class="hop ${unresolved ? 'hop--unresolved' : ''}" data-epistemic="${hop.epistemic_status}"
      data-card-id="${escapeHtml(hop.id)}" tabindex="0" role="button"
      aria-label="Chain hop ${hop.ordinal}: ${escapeHtml(hop.stage)} — select to inspect provenance">
    <div class="hop__gutter" aria-hidden="true"></div>
    <div class="hop__inner">
      <div class="hop__head">
        <span class="hop__ord" aria-hidden="true">${hop.ordinal}</span>
        <span class="hop__stage">${escapeHtml(hop.stage)}</span>
        ${epistemicChip(hop.epistemic_status)}${confidenceChip(hop.confidence)}
      </div>
      <div class="hop__actor">${escapeHtml(hop.actor)}</div>
      <p class="hop__summary">${
        hop.summary
          ? escapeHtml(hop.summary)
          : absenceValue('UNKNOWN') +
            ' <span class="hop__nomech">No engine evaluates government options. This hop is present so the gap is visible rather than hidden.</span>'
      }</p>
      ${entities ? `<div class="hop__ents">${entities}</div>` : ''}
      ${contributors}
      <div class="hop__prov">${provenanceLine(hop)}</div>
    </div>
  </li>`
}

function claimRow(c: Claim): string {
  // Unknown / unavailable / zero must look different. A missing row silently reads as zero.
  const value = c.value === null ? absenceValue(c.absence ?? 'UNKNOWN') : escapeHtml(c.value)
  return `<li class="claim" data-epistemic="${c.epistemic_status}" data-card-id="${escapeHtml(c.id)}"
      tabindex="0" role="button" aria-label="${escapeHtml(c.label)} — select to inspect provenance">
    <div class="claim__gutter" aria-hidden="true"></div>
    <div class="claim__main">
      <span class="claim__label">${escapeHtml(c.label)}</span>
      <span class="claim__value">${value}</span>
    </div>
    <div class="claim__chips">${epistemicChip(c.epistemic_status)}${confidenceChip(c.confidence)}</div>
  </li>`
}

function panelBlock(p: Panel): string {
  return card(p, {
    id: p.id,
    title: p.title,
    standfirst: p.standfirst,
    body: `<ul class="claims">${p.claims.map(claimRow).join('')}</ul>`,
  })
}

function queueItem(q: QueueItem): string {
  // An item with no affordance is not a decision — it is a stream event. Enforced in tests.
  return `<li class="qitem" data-card-id="${escapeHtml(q.id)}" data-epistemic="${q.epistemic_status}"
      tabindex="0" role="button" aria-label="${escapeHtml(q.title)} — select to inspect provenance">
    <div class="qitem__gutter" aria-hidden="true"></div>
    <div class="qitem__inner">
      <div class="qitem__head">
        <span class="qitem__title">${escapeHtml(q.title)}</span>
        ${q.deadline_label ? `<span class="qitem__deadline">${escapeHtml(q.deadline_label)}</span>` : ''}
      </div>
      <p class="qitem__detail">${escapeHtml(q.detail)}</p>
      <ul class="affordances">${q.affordances
        .map((a) => `<li class="afford">${escapeHtml(a)}</li>`)
        .join('')}</ul>
      <p class="qitem__note">Display only — no action can be submitted, validated or priced in this prototype.</p>
    </div>
  </li>`
}

function streamRow(s: StreamEvent): string {
  // Low-relevance rows are DIMMED, never filtered out.
  return `<li class="sev sev--${s.relevance}" data-card-id="${escapeHtml(s.id)}" data-epistemic="${s.epistemic_status}"
      tabindex="0" role="button" aria-label="Tick ${s.tick}: ${escapeHtml(s.text)} — select to inspect provenance">
    <span class="sev__tick">t${s.tick}</span>
    <span class="sev__text">${escapeHtml(s.text)}</span>
    ${epistemicChip(s.epistemic_status)}
  </li>`
}

export function strategicCommandCentre(fx: ScenarioFixture): string {
  const c = fx.crisis
  return `
  <section class="scc" aria-label="Strategic Command Centre">

    <header class="crisis" data-epistemic="${c.epistemic_status}" data-card-id="${escapeHtml(c.id)}"
        tabindex="0" role="button" aria-label="${escapeHtml(c.name)} — select to inspect provenance">
      <div class="crisis__gutter" aria-hidden="true"></div>
      <div class="crisis__inner">
        <div class="crisis__meta">
          <span class="crisis__day">${escapeHtml(c.day_label)}</span>
          <span class="crisis__loc">${escapeHtml(c.location_label)}</span>
          ${epistemicChip(c.epistemic_status)}${confidenceChip(c.confidence)}
        </div>
        <h2 class="crisis__name">${escapeHtml(c.name)}</h2>
        <p class="crisis__standfirst">${escapeHtml(c.standfirst)}</p>
        ${provenanceLine(c)}
      </div>
    </header>

    <div class="scc__chainblock">
      <h3 class="secthead">
        How this is moving through society
        <span class="secthead__warn">Hand-authored fixture trace — not computed, not simulated, not live</span>
      </h3>
      <ol class="chain">${fx.chain.map(chainHop).join('')}</ol>
    </div>

    <div class="scc__panelblock">
      <h3 class="secthead">Reactions</h3>
      <div class="panelgrid">${fx.panels.map(panelBlock).join('')}</div>
    </div>

  </section>`
}

/** Full-width bottom bar. Kept out of the centre column so the crisis picture fits above the fold. */
export function eventStream(fx: ScenarioFixture): string {
  return `<section class="streambar" aria-label="Event stream">
    <h3 class="secthead">Event stream <span class="secthead__hint">low-relevance rows are dimmed, never removed</span></h3>
    <ul class="stream" role="log" aria-live="polite" aria-label="Event stream">${fx.stream
      .map(streamRow)
      .join('')}</ul>
  </section>`
}

export function decisionQueue(fx: ScenarioFixture): string {
  return `<section class="queue" aria-label="Decisions awaiting you">
    <h3 class="secthead">Decisions awaiting you <span class="count">${fx.queue.length}</span></h3>
    <ul class="qlist">${fx.queue.map(queueItem).join('')}</ul>
  </section>`
}
