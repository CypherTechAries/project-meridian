/**
 * Briefing constants.
 *
 * The Briefing is no longer a screen. It is the first answer in the Ask MERIDIAN thread — see
 * `briefing-card.ts` and the note at the top of `main.ts`. The 2,635px document this file used to
 * render was deleted rather than left dormant: dead screens rot, and a reader of this codebase
 * should not have to work out which of two Briefings is live.
 *
 * What survives here is the vocabulary other modules depend on.
 */

import { NOTHING_EXECUTES } from '../engine/presentation.ts'

export { NOTHING_EXECUTES }

/**
 * Stated wherever the situation diagram is offered. A reader who opens it is entitled to know it
 * has not met the bar the rest of the interface was rebuilt to meet.
 *
 * Delete this when a cold reader has actually passed the five-second test — because it stopped
 * being true, not because it is inconvenient.
 */
export const MAP_LIMITATION =
  'This diagram is supporting evidence and has not yet passed the five-second comprehension test — ' +
  'no first-time reader has been asked to explain it yet. It replaces a map, because MERIDIAN does ' +
  'not model locations, distances or routes. Nothing on this screen depends on reading it.'
