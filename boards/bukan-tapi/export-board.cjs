// Renders the scene studies and the style board to PNG, and syncs assets/ into the motion preview
// (the HyperFrames renderer does not follow symlinks out of its project). Run before rendering the preview.
// Usage: NODE_PATH=<global node_modules> node boards/bukan-tapi/export-board.cjs [studies|board|all|t=<seconds>]
const path = require("path");
const http = require("http");
const fs = require("fs");
const puppeteer = require("puppeteer");

const root = __dirname;
const mime = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".png": "image/png", ".ttf": "font/ttf", ".mp4": "video/mp4" };
const server = http.createServer((req, res) => {
  const file = path.join(root, decodeURIComponent(req.url.split("?")[0]));
  if (!file.startsWith(root) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) return res.writeHead(404).end();
  res.writeHead(200, { "content-type": mime[path.extname(file)] || "application/octet-stream" });
  fs.createReadStream(file).pipe(res);
});

(async () => {
  const what = process.argv[2] || "all";
  fs.cpSync(path.join(root, "assets"), path.join(root, "motion-preview", "assets"), { recursive: true, force: true });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  const base = `http://127.0.0.1:${server.address().port}`;
  const browser = await puppeteer.launch({ executablePath: process.env.CHROME_EXECUTABLE || undefined, args: ["--no-sandbox"] });
  try {
    const page = await browser.newPage();
    page.on("pageerror", (error) => console.error("pageerror:", error.message));
    page.on("console", (message) => message.type() === "error" && console.error("console:", message.text()));
    const shoot = async (query, out) => {
      await page.setViewport({ width: 1080, height: 1920, deviceScaleFactor: 1 });
      await page.goto(`${base}/studies/studies.html?${query}`);
      await page.waitForFunction("window.__ready === true", { timeout: 60000 });
      await page.screenshot({ path: out });
      console.log(out);
    };
    if (what.startsWith("t=")) await shoot(what, path.join(root, "studies", `pilot-${what.slice(2)}.png`));
    else {
      if (what !== "board") for (const study of ["hook", "dialogue", "cutaway", "reveal"]) await shoot(`study=${study}`, path.join(root, "studies", `${study}.png`));
      if (what !== "studies") {
        await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
        await page.goto(`${base}/style-board.html`, { waitUntil: "networkidle0" });
        await page.evaluate(() => document.fonts.ready);
        await page.screenshot({ path: path.join(root, "style-board.png"), fullPage: true });
        console.log("board");
      }
    }
  } finally {
    await browser.close();
    server.close();
  }
})();
