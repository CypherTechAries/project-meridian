/**
 * Capture the approved product screenshots.
 *
 * Briefing is the default mode, so that is what loads first. Analysis is reached through the
 * visible switch — the same route a user takes, which also proves the switch works and is
 * two-way.
 *
 * Acceptance criteria are measured here rather than eyeballed: no clipped panel, no ellipsised
 * headline, no horizontal overflow, disclosure present, origin markers present, and no raw engine
 * machinery leaking into Briefing.
 */
import { chromium } from 'playwright'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'
import { mkdirSync } from 'node:fs'

const here = dirname(fileURLToPath(import.meta.url))
const out = resolve(here, '..', 'screenshots', 'current')
mkdirSync(out, { recursive: true })
const URL = process.env.MERIDIAN_URL ?? 'http://localhost:5173/'

const measure = () => ({
  doc: document.documentElement.scrollHeight,
  vp: window.innerHeight,
  hOverflow: document.documentElement.scrollWidth > window.innerWidth,
  mode: document.querySelector('.modesw__btn.is-on')?.textContent?.trim(),
  disclosure: !!document.body.textContent?.includes(
    'FICTIONAL SIMULATION — NOT REAL-WORLD INTELLIGENCE OR PREDICTION',
  ),
  originBadges: document.querySelectorAll('.ob').length,
  consequenceCards: document.querySelectorAll('.ccard').length,
  decisions: document.querySelectorAll('.dcard').length,
  clipped: Array.from(
    document.querySelectorAll('.bviz,.bsum,.bneeds,.bsince,.ccard,.panel__body'),
  )
    .filter((b) => b.scrollHeight - b.clientHeight > 1)
    .map((b) => b.className.split(' ')[0]),
  ellipsised: Array.from(
    document.querySelectorAll('.ccard__state,.dcard__title,.bsum__head,.panel__sub'),
  )
    .filter((e) => e.scrollWidth > e.clientWidth + 1)
    .map((e) => e.textContent.trim().slice(0, 40)),
  // No raw engine machinery may appear in Briefing.
  rawLeak: /@1\.0\.0|M-[A-Z-]+@|NOT_APPLICABLE|state revision|rule pack/i.test(
    document.querySelector('.main--briefing')?.textContent ?? '',
  ),
})

const browser = await chromium.launch()
const errors = []

for (const [w, h, name] of [
  [1440, 900, 'laptop'],
  [1600, 1000, 'desktop'],
]) {
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 })
  page.on('console', (m) => m.type() === 'error' && errors.push(m.text()))
  page.on('pageerror', (e) => errors.push(String(e)))
  await page.goto(URL, { waitUntil: 'networkidle' })
  await page.waitForSelector('.briefing')
  await page.waitForTimeout(400)

  await page.screenshot({ path: resolve(out, `briefing-${name}.png`) })
  console.log(`  briefing ${w}x${h}:`, JSON.stringify(await page.evaluate(measure), null, 1))

  if (name === 'laptop') {
    // Crop safety: one card alone must still carry its origin marker.
    const card = await page.$('.ccard--politics')
    if (card) await card.screenshot({ path: resolve(out, 'briefing-crop.png') })

    // Reach Analysis the way a user does — through the visible switch.
    await page.click('.modesw__btn[data-mode="analysis"]')
    await page.waitForSelector('.scc')
    await page.waitForTimeout(400)
    await page.screenshot({ path: resolve(out, 'analysis-technical.png') })
    console.log('  analysis 1440x900:', JSON.stringify(await page.evaluate(measure), null, 1))

    await page.click('.modesw__btn[data-mode="briefing"]')
    await page.waitForSelector('.briefing')
    console.log('  returned to briefing: OK')
  }
  await page.close()
}

await browser.close()
console.log('console errors:', errors.length ? errors : 'none')
