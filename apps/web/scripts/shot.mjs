import { chromium } from "playwright";

const OUT = "C:/Users/tanma/AppData/Local/Temp/opencode/shots";
const BASE = "http://localhost:3000";

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });

await page.goto(`${BASE}/login`, { waitUntil: "networkidle" });
await page.waitForTimeout(500);
await page.screenshot({ path: `${OUT}/login.png` });

await page.goto(`${BASE}/cases`, { waitUntil: "networkidle" });
await page.waitForTimeout(1000);
await page.screenshot({ path: `${OUT}/cases.png` });

await page.goto(`${BASE}/cases/case-0417`, { waitUntil: "networkidle" });
await page.waitForTimeout(2500); // timeline animation
await page.screenshot({ path: `${OUT}/overview.png` });

for (const tab of ["Findings", "Governance", "Evidence"]) {
  await page.getByRole("tab", { name: tab }).click();
  await page.waitForTimeout(600);
  await page.screenshot({ path: `${OUT}/${tab.toLowerCase()}.png` });
}

await browser.close();
console.log("shots done");
