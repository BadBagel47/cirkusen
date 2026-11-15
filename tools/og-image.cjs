// Renders the share image (1200x630) for one poster: the top part of the poster, as a JPEG.
// Usage: node tools/og-image.cjs <public-dir> <slug> <output.jpg>
// Needs Playwright with Chromium (npm i -g playwright). Normally started by tools/posters.py.
const fs = require("fs");
const http = require("http");
const path = require("path");
const { chromium } = require("playwright");

const [publicDir, slug, out] = process.argv.slice(2);
if (!publicDir || !slug || !out) {
  console.error("usage: node og-image.cjs <public-dir> <slug> <output.jpg>");
  process.exit(2);
}
const root = path.resolve(publicDir);
const types = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json",
  ".woff2": "font/woff2", ".jpg": "image/jpeg", ".svg": "image/svg+xml", ".png": "image/png", ".webp": "image/webp" };

// Small static server so that absolute paths like /assets/poster.css work, like on the real site.
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]);
  if (p.endsWith("/")) p += "index.html";
  const file = path.join(root, p);
  if (!file.startsWith(root) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, { "content-type": types[path.extname(file)] || "application/octet-stream" });
  res.end(fs.readFileSync(file));
});

(async () => {
  await new Promise((r) => server.listen(0, "127.0.0.1", r));
  const browser = await chromium.launch();
  try {
    const W = 1080, H = Math.round(1080 * 630 / 1200); // poster width and the matching height of a 1200x630 crop
    const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1200 / W, reducedMotion: "reduce" });
    const errors = [];
    page.on("pageerror", (e) => errors.push(String(e)));
    await page.goto(`http://127.0.0.1:${server.address().port}/${slug}/`);
    await page.addStyleTag({ content: "#nav{display:none!important}" });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: out, type: "jpeg", quality: 85, clip: { x: 0, y: 0, width: W, height: H } });
    if (errors.length) throw new Error(errors.join("; "));
  } finally {
    await browser.close();
    server.close();
  }
})().catch((e) => { console.error(e.message || e); process.exit(1); });
