#!/usr/bin/env node
"use strict";

/**
 * Snapshot plus console-error check.
 * Uses Playwright already installed in this project. Does not install packages.
 *
 * Usage:
 *   node check-snapshot-console.cjs <url> [screenshot.png]
 *
 * Exit 0 if the page loads with no pageerror / console-error events.
 * Exit 1 on navigation or console failures.
 * Exit 2 if Playwright is not installed.
 */

const fs = require("fs");
const path = require("path");

function loadPlaywright() {
  const names = ["playwright", "playwright-core", "@playwright/test"];
  for (const name of names) {
    try {
      return require(name);
    } catch (_err) {
      // try the next package name
    }
  }
  console.error("VERIFY command: check-snapshot-console");
  console.error("VERIFY_FAIL");
  console.error(
    "Playwright is not installed in this project. Install it yourself; this template will not.",
  );
  process.exit(2);
}

async function main() {
  const url = process.argv[2];
  const shot = process.argv[3] || "verify-snapshot.png";
  if (!url) {
    console.error("usage: node check-snapshot-console.cjs <url> [screenshot.png]");
    process.exit(2);
  }

  const playwright = loadPlaywright();
  const chromium = playwright.chromium;
  if (!chromium) {
    console.error("VERIFY_FAIL");
    console.error("Playwright loaded but chromium is missing.");
    process.exit(2);
  }

  const errors = [];
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage();
    page.on("pageerror", (err) => {
      errors.push(`pageerror: ${err.message}`);
    });
    page.on("console", (msg) => {
      if (msg.type() === "error") {
        errors.push(`console.error: ${msg.text()}`);
      }
    });
    const started = new Date().toISOString();
    console.log(`VERIFY command: check-snapshot-console ${url}`);
    console.log(`VERIFY started: ${started}`);
    const response = await page.goto(url, { waitUntil: "networkidle" });
    const status = response ? response.status() : 0;
    await page.screenshot({ path: shot, fullPage: true });
    const shotPath = path.resolve(shot);
    const exists = fs.existsSync(shotPath);
    console.log(`VERIFY screenshot: ${exists ? shotPath : "missing"}`);
    console.log(`VERIFY http_status: ${status}`);
    if (!response || status >= 400 || errors.length) {
      console.log(`VERIFY exit: 1`);
      for (const line of errors) {
        console.log(`VERIFY console: ${line}`);
      }
      console.log("VERIFY_FAIL");
      process.exitCode = 1;
      return;
    }
    console.log("VERIFY exit: 0");
    console.log("VERIFY_PASS");
  } finally {
    await browser.close();
  }
}

main().catch((err) => {
  console.error("VERIFY_FAIL");
  console.error(err && err.stack ? err.stack : String(err));
  process.exit(1);
});
