/**
 * Rasterises every SVG in assets/img/ to WebP + PNG at 2x, for the WordPress
 * media library (the page itself uses the SVGs directly).
 *
 *   npm i -D playwright   # or use the bundled Chromium
 *   node tools/rasterise.mjs
 */
import { chromium } from 'playwright';
import { readdir, readFile, mkdir } from 'node:fs/promises';
import path from 'node:path';

const IMG = path.resolve('assets/img');
const OUT = path.resolve('assets/img/raster');
const SCALE = 2;

const size = (svg) => {
  const m = svg.match(/viewBox="0 0 ([\d.]+) ([\d.]+)"/);
  return m ? { w: Math.round(+m[1]), h: Math.round(+m[2]) } : { w: 1200, h: 800 };
};

// CHROMIUM_PATH lets you point at an already-installed Chromium instead of
// Playwright's own download (handy in CI images that ship one).
const browser = await chromium.launch({
  executablePath: process.env.CHROMIUM_PATH || undefined,
});
await mkdir(OUT, { recursive: true });

for (const file of (await readdir(IMG)).filter((f) => f.endsWith('.svg'))) {
  const svg = await readFile(path.join(IMG, file), 'utf8');
  const { w, h } = size(svg);
  const page = await browser.newPage({
    viewport: { width: w, height: h },
    deviceScaleFactor: SCALE,
  });
  await page.setContent(
    `<style>html,body{margin:0;background:transparent}svg{display:block}</style>${svg}`,
    { waitUntil: 'networkidle' },
  );
  const base = file.replace(/\.svg$/, '');
  for (const type of ['webp', 'png']) {
    await page.screenshot({
      path: path.join(OUT, `${base}.${type}`),
      type,
      omitBackground: true,
      ...(type === 'webp' ? { quality: 90 } : {}),
    });
  }
  await page.close();
  console.log(`  ${base}  ${w}x${h} @${SCALE}x → webp + png`);
}

await browser.close();
