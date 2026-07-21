/**
 * The one place the frontend decides where the backend is.
 *
 * Every screen that talks to MERIDIAN resolves its URL through `apiUrl()`. There is deliberately
 * no second convention: a screen that builds its own path is a defect, because the two screens
 * then disagree about what "the backend" means and one of them silently talks to the dev server.
 *
 * That is not hypothetical. Ask MERIDIAN previously used a bare relative path while the Briefing
 * used an absolute one, so in the real browser the Briefing reached the engine on :8000 and Ask
 * posted to Vite on :5173 and received a 404 HTML page. Every test passed, because no test
 * compared the two.
 *
 * The base is a **development default**, overridable at build time by `VITE_MERIDIAN_API_BASE`
 * for any deployment where the API is not on localhost:8000.
 */

/** Where the backend runs in local development. */
export const DEFAULT_API_BASE = 'http://localhost:8000'

/** Resolved once, so both screens cannot drift apart at runtime. */
export const API_BASE: string = readConfiguredBase() ?? DEFAULT_API_BASE

/** Paths are declared here too, so an endpoint is never spelled out twice. */
export const RUN_PATH = '/api/demo/kestral-strait/run'
export const ASK_PATH = '/api/ask-meridian/query'

function readConfiguredBase(): string | null {
  // `import.meta.env` is absent in some non-Vite contexts; treat that as "unset", not an error.
  const configured = import.meta.env?.VITE_MERIDIAN_API_BASE
  if (typeof configured !== 'string') return null
  const trimmed = configured.trim()
  return trimmed === '' ? null : trimmed.replace(/\/+$/, '')
}

/**
 * Join the shared base to an API path.
 *
 * Absolute in every case: a relative URL would resolve against whatever origin is serving the
 * page, which is exactly the defect this module exists to prevent.
 */
export function apiUrl(path: string): string {
  const suffix = path.startsWith('/') ? path : `/${path}`
  return `${API_BASE}${suffix}`
}
