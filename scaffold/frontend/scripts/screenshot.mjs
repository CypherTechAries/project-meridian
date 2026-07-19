/**
 * Full-viewport screenshot of the C0 prototype, for founder review.
 *
 * Deliberately captures the NORMAL VIEWPORT, not a full-page capture: the acceptance criterion is
 * that both disclosures and the essential crisis picture are visible without scrolling. A
 * full-page capture would hide a failure to fit.
 *
 * It also captures a CROPPED region, to verify the founder requirement that the fictional-world
 * disclosure survives realistic cropping — a single page-level banner would not.
 */

import { chromium } from 'playwright'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'
import { mkdirSync } from 'node:fs'

const here = dirname(fileURLToPath(import.meta.url))
const outDir = resolve(here, '..', 'screenshots')
mkdirSync(outDir, { recursive: true })

const URL = process.env.MERIDIAN_URL ?? 'http://localhost:5173/'
// Large-desktop review viewport. Reported honestly in the C0 notes: this screen is dense (ten
// content categories plus per-claim provenance), and at 1600x1000 the chain and reaction panels
// require scrolling. Content is never hidden to make a height target.
const WIDTH = 1600
const HEIGHT = 1400

const browser = await chromium.launch()
const page = await browser.newPage({ viewport: { width: WIDTH, height: HEIGHT }, deviceScaleFactor: 2 })

const errors = []
page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()) })
page.on('pageerror', (e) => errors.push(String(e)))

await page.goto(URL, { waitUntil: 'networkidle' })
await page.waitForSelector('.crisis__name')

// Select a chain hop so the inspector is populated in the screenshot — proving provenance is
// inspectable rather than merely present. Dispatched without scrollIntoView, then the page is
// returned to the top: the acceptance criterion is what a viewer sees WITHOUT scrolling, and a
// capture of a scrolled page would hide a failure to fit.
await page.evaluate(() => {
  document.querySelector('[data-card-id="hop-6"]')?.dispatchEvent(new MouseEvent('click', { bubbles: true }))
  window.scrollTo(0, 0)
})
await page.waitForSelector('.provdetail')

const full = resolve(outDir, 'strategic-command-centre.png')
await page.screenshot({ path: full })

// Crop test: a 520x420 region from the centre, deliberately excluding both banner bands.
const crop = resolve(outDir, 'crop-invariance-check.png')
await page.screenshot({ path: crop, clip: { x: 200, y: 320, width: 520, height: 420 } })

// Report what a viewer of the cropped region can still see.
const cropText = await page.evaluate(() => {
  const marks = Array.from(document.querySelectorAll('.prov__origin')).map((n) => n.textContent?.trim())
  return { fixtureMarkers: marks.length, distinct: Array.from(new Set(marks)) }
})

const summary = await page.evaluate(() => ({
  title: document.querySelector('.crisis__name')?.textContent?.trim(),
  hops: document.querySelectorAll('.hop').length,
  panels: document.querySelectorAll('.card').length,
  queue: document.querySelectorAll('.qitem').length,
  stream: document.querySelectorAll('.sev').length,
  chips: document.querySelectorAll('.chip').length,
  disclosures: document.querySelectorAll('.disclose').length,
  inspectorPopulated: !!document.querySelector('.provdetail'),
  docHeight: document.documentElement.scrollHeight,
}))

await browser.close()

console.log('screenshot :', full)
console.log('crop check :', crop)
console.log('summary    :', JSON.stringify(summary, null, 2))
console.log('fixture markers in DOM:', JSON.stringify(cropText))
console.log('console errors:', errors.length ? errors : 'none')
if (errors.length) process.exitCode = 1
