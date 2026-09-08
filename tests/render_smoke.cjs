// Development-only browser check. CI installs Playwright in a temporary prefix.
// Run: node tests/render_smoke.cjs <artifact-directory>
const assert = require('node:assert/strict');
const { execFileSync } = require('node:child_process');
const fs = require('node:fs');
const path = require('node:path');
const { pathToFileURL } = require('node:url');
const { chromium } = require('playwright');
const PYTHON = process.env.PYTHON || (process.platform === 'win32' ? 'python' : 'python3');

async function main() {
  assert(process.argv[2], 'Provide an artifact directory outside the checkout');
  const output = path.resolve(process.argv[2]);
  fs.mkdirSync(output, { recursive: true });
  const root = path.resolve(__dirname, '..');
  const browser = await chromium.launch({
    timeout: 15000,
    ...(process.env.DISO_BROWSER_CHANNEL ? { channel: process.env.DISO_BROWSER_CHANNEL } : {}),
  });
  try {
    for (const mode of ['kid', 'standard', 'deep']) {
      const file = path.join(output, `${mode}.html`);
      execFileSync(PYTHON, [path.join(root, 'scripts/build.py'),
        path.join(root, 'examples/btree-index.json'), '--mode', mode, '-o', file], { timeout: 15000 });
      for (const width of [390, 1440]) {
        const start = performance.now();
        const page = await browser.newPage({ viewport: { width, height: 900 } });
        page.setDefaultTimeout(15000);
        const requests = [];
        const errors = [];
        page.on('request', request => { if (/^https?:/.test(request.url())) requests.push(request.url()); });
        page.on('pageerror', error => errors.push(error.message));
        await page.goto(pathToFileURL(file).href, { waitUntil: 'load' });
        await page.waitForFunction(() => document.fonts.status === 'loaded');
        const geometry = await page.evaluate(() => {
          const rect = document.querySelector('main').getBoundingClientRect();
          const svgs = [...document.querySelectorAll('figure svg')];
          return {
            title: document.querySelector('h1').textContent.trim(),
            width: document.documentElement.clientWidth,
            scroll: document.documentElement.scrollWidth,
            main: { width: rect.width, height: rect.height },
            figures: svgs.map(svg => ({ width: svg.getBoundingClientRect().width, height: svg.getBoundingClientRect().height })),
          };
        });
        assert(geometry.title.length > 0 && geometry.main.height > 0, 'Empty document');
        assert(geometry.figures.length > 0 && geometry.figures.every(f => f.width > 0 && f.height > 0), 'Missing figures');
        assert(geometry.scroll <= geometry.width + 1, `Horizontal overflow: ${JSON.stringify(geometry)}`);
        if (mode === 'deep') {
          await page.locator('details > summary').click();
          assert(await page.locator('details').evaluate(el => el.open), 'Deep details did not open');
          assert(await page.locator('.dbody').isVisible(), 'Deep content is hidden');
        }
        await page.screenshot({ path: path.join(output, `${mode}-${width}.png`), fullPage: true });
        assert.deepEqual(requests, [], 'Page requested external rendering resources');
        assert.deepEqual(errors, [], 'Browser errors');
        console.log(`${mode} ${width}px: rendered, checked and captured in ${Math.round(performance.now() - start)}ms`);
        await page.close();
      }
    }
  } finally {
    await browser.close();
  }
}

main().catch(error => { console.error(error); process.exitCode = 1; });
