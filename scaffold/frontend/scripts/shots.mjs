import { chromium } from 'playwright'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'
import { mkdirSync } from 'node:fs'
const here = dirname(fileURLToPath(import.meta.url))
const out = resolve(here, '..', 'screenshots')
mkdirSync(out, { recursive: true })
const tag = process.argv[2] ?? 'final'
const URL = process.env.MERIDIAN_URL ?? 'http://localhost:5173/'

const browser = await chromium.launch()
const errors = []
for (const [w, h, name] of [[1440, 900, 'laptop'], [1600, 1000, 'desktop']]) {
  const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 2 })
  page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text()) })
  page.on('pageerror', (e) => errors.push(String(e)))
  await page.goto(URL, { waitUntil: 'networkidle' })
  await page.waitForSelector('.bignum__value')
  await page.screenshot({ path: resolve(out, `scc-${tag}-${name}.png`) })
  {
    const m = await page.evaluate(() => ({
      doc: document.documentElement.scrollHeight,
      vp: window.innerHeight,
      hOverflow: document.documentElement.scrollWidth > window.innerWidth,
      panels: document.querySelectorAll('.panel').length,
      fmarks: document.querySelectorAll('.fmark').length,
      badges: document.querySelectorAll('.ob').length,
      // Acceptance criteria, measured rather than eyeballed.
      clippedBodies: Array.from(document.querySelectorAll('.panel__body'))
        .filter((b) => b.scrollHeight - b.clientHeight > 1)
        .map((b) => b.closest('.panel').className.replace('panel panel--', '')),
      propagationRows: document.querySelectorAll('.chainsum__step').length,
      propagationClipped: (() => {
        const box = document.querySelector('.panel--options').getBoundingClientRect()
        return Array.from(document.querySelectorAll('.chainsum__step'))
          .filter((r) => r.getBoundingClientRect().bottom > box.bottom + 0.5).length
      })(),
      chartClipped: (() => {
        const c = document.querySelector('.panel--crisis .chart')
        if (!c) return 'no-chart'
        const box = document.querySelector('.panel--crisis').getBoundingClientRect()
        return c.getBoundingClientRect().bottom > box.bottom + 0.5
      })(),
      wrappedSubs: Array.from(document.querySelectorAll('.panel__sub'))
        .filter((el) => el.getBoundingClientRect().height > parseFloat(getComputedStyle(el).lineHeight) * 1.4)
        .map((el) => el.textContent.trim()),
      truncatedSubs: Array.from(document.querySelectorAll('.panel__sub'))
        .filter((el) => el.scrollWidth > el.clientWidth + 1)
        .map((el) => el.textContent.trim()),
    }))
    console.log(`  ${name} ${w}x${h}:`, JSON.stringify(m, null, 1))
    if (name === 'laptop') {
      const el = await page.$('.panel--cohorts')
      if (el) await el.screenshot({ path: resolve(out, `scc-${tag}-crop.png`) })
    }
  }
  await page.close()
}
await browser.close()
console.log('console errors:', errors.length ? errors : 'none')
