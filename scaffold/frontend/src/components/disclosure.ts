/**
 * Persistent disclosures — founder-specified wording, verbatim.
 *
 * These are B5 interface controls, not decoration. `CHARTER.md` records that no provenance tag
 * exists at any interface and that B5 is the one publication blocker that cannot be cleared by
 * correcting text — it clears only when controls like these are implemented and verified.
 *
 * Implementing them contributes to B5 enforcement. It does NOT clear the B5 publication gate:
 * the backend and policy controls (world_mode: fictional failing closed, real-world scenario
 * import disabled, prohibited target classes, protected-characteristic restrictions) still
 * require implementation and verification.
 *
 * Non-dismissible by construction: there is no close control and no state that hides them.
 */

export const FICTION_DISCLOSURE = 'FICTIONAL SIMULATION — NOT REAL-WORLD INTELLIGENCE OR PREDICTION'

export const FIXTURE_DISCLOSURE =
  'INTERACTIVE PROTOTYPE — FIXTURE DATA — NOT CONNECTED TO THE SIMULATION ENGINE'

/**
 * Rendered at the top of the viewport AND repeated in the footer, so the pair survives a
 * top-crop or a bottom-crop of a screenshot. Individual cards additionally carry their own
 * FIXTURE marker for the case where a single card is cropped out.
 */
export function disclosureBands(): string {
  return `<div class="disclosures" role="region" aria-label="Prototype disclosures">
    <div class="disclose disclose--fiction">
      <span class="disclose__glyph" aria-hidden="true">⚠</span>
      <span class="disclose__text">${FICTION_DISCLOSURE}</span>
    </div>
    <div class="disclose disclose--fixture">
      <span class="disclose__glyph" aria-hidden="true">▨</span>
      <span class="disclose__text">${FIXTURE_DISCLOSURE}</span>
    </div>
  </div>`
}

/** Footer repetition — crop resistance in the other direction. */
export function disclosureFooter(): string {
  return `<div class="disclosures disclosures--footer" role="region" aria-label="Prototype disclosures, repeated">
    <div class="disclose disclose--fiction">
      <span class="disclose__glyph" aria-hidden="true">⚠</span>
      <span class="disclose__text">${FICTION_DISCLOSURE}</span>
    </div>
    <div class="disclose disclose--fixture">
      <span class="disclose__glyph" aria-hidden="true">▨</span>
      <span class="disclose__text">${FIXTURE_DISCLOSURE}</span>
    </div>
  </div>`
}
