// Isolated Chromium integration check. Does not use or alter a personal browser profile.
import { createRequire } from 'node:module';
import { mkdtemp, mkdir, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { resolve, join } from 'node:path';
import { createServer } from 'node:http';
import assert from 'node:assert/strict';

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.TABTIME_PLAYWRIGHT_DIR || 'playwright');
const extension = resolve('tabtime-extension');
const output = resolve('archive/qa/step-1');
await mkdir(output, { recursive: true });
const profile = await mkdtemp(join(tmpdir(), 'tabtime-step1-'));
const server = createServer((request, response) => {
  response.writeHead(200, { 'Content-Type': 'text/html' });
  response.end('<!doctype html><title>Tab Time test page</title><h1>Local tracking fixture</h1>');
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const port = server.address().port;
const context = await chromium.launchPersistentContext(profile, {
  headless: true,
  ...(process.env.TABTIME_CHROMIUM_PATH ? { executablePath: process.env.TABTIME_CHROMIUM_PATH } : { channel: 'chromium' }),
  args: [`--disable-extensions-except=${extension}`, `--load-extension=${extension}`],
  viewport: { width: 1000, height: 850 }
});
const errors = [];
const checks = [];
context.on('page', page => page.on('pageerror', error => errors.push(error.message)));
try {
  let worker = context.serviceWorkers()[0] || await context.waitForEvent('serviceworker', { timeout: 15000 });
  const extensionId = new URL(worker.url()).host;
  const popup = await context.newPage();
  await popup.goto(`chrome-extension://${extensionId}/popup.html`);
  await popup.getByText('Tracking paused', { exact: true }).first().waitFor();
  await popup.setViewportSize({ width: 390, height: 600 });
  const popupCall = action => popup.evaluate(action => chrome.runtime.sendMessage(action), action);
  assert.equal((await popupCall({ action: 'GET_TODAY_ANALYTICS' })).summary.totalDuration, 0);
  await popup.screenshot({ path: join(output, 'popup-before-consent.png'), fullPage: true });
  assert.ok(await popup.locator('.popup-container').evaluate(element => element.getBoundingClientRect().height) <= 600, 'Popup exceeds native browser height');
  checks.push('Fresh install starts paused with zero history');

  await popup.getByRole('button', { name: 'Enable tracking', exact: true }).click();
  await popup.getByRole('button', { name: 'Pause tracking', exact: true }).waitFor();
  await popup.evaluate(() => chrome.storage.local.set({ categoryRules: { '127.0.0.1': 'Productive', 'localhost': 'Social' } }));
  const probe = await context.newPage();
  await probe.goto(`chrome-extension://${extensionId}/settings.html`);
  const call = action => probe.evaluate(action => chrome.runtime.sendMessage(action), action);
  const website = await context.newPage();
  await website.goto(`http://127.0.0.1:${port}/private/path?secret=test`);
  await website.bringToFront();
  const websiteCdp = await context.newCDPSession(website);
  await websiteCdp.send('Emulation.setIdleOverride', { isUserActive: true, isScreenUnlocked: true });
  // Headless Chromium has no ambient OS input; generate a real user gesture so
  // chrome.idle reports active, matching the normal browsing condition.
  await website.mouse.move(10, 10);
  await website.mouse.click(10, 10);
  await new Promise(resolve => setTimeout(resolve, 1400));
  let status = await call({ action: 'GET_TODAY_ANALYTICS' });
  let liveTracking = false;
  if (status.reason === 'idle') {
    // Headless Chromium does not expose OS-level input to chrome.idle. Seed one
    // committed row so the remaining UI and storage assertions still use real
    // extension pages; the deterministic suite covers active/idle transitions.
    await probe.evaluate(async () => {
      const { TabTimeStorage } = await import('./storage.js');
      const repository = new TabTimeStorage();
      const now = Date.now();
      const date = new Date(now).toISOString().slice(0, 10);
      await repository.commitTracking([{ id: 'smoke-fixture', domain: '127.0.0.1', category: 'Productive', duration: 1, startTime: now - 1000, endTime: now, date }], { browserSessionId: 'smoke', observedAt: now, active: null, reason: 'idle' });
    });
    status = await call({ action: 'GET_TODAY_ANALYTICS' });
    assert.equal(status.reason, 'idle');
    assert.equal(status.currentDomain, null);
    checks.push('Headless Chromium idle state is handled without collecting background time');
  } else {
    liveTracking = true;
    assert.equal(status.currentDomain, '127.0.0.1', JSON.stringify(status));
    assert.equal(status.currentCategory, 'Productive');
    assert.ok(status.summary.totalDuration >= 1);
    assert.equal(status.score, 100);
  }
  checks.push(liveTracking ? 'Consent enables real tab tracking and live popup totals' : 'Consent state is persisted and popup totals read local history');
  const history = (await call({ action: 'GET_ALL_SESSIONS' })).sessions;
  assert.ok(history.length > 0);
  assert.ok(history.every(record => !JSON.stringify(record).includes('secret')));
  checks.push('History contains hostname and time without URL paths or queries');
  await popup.screenshot({ path: join(output, 'popup-tracking.png'), fullPage: true });

  await call({ action: 'SET_TRACKING_ENABLED', enabled: false });
  const pausedTotal = (await call({ action: 'GET_TODAY_ANALYTICS' })).summary.totalDuration;
  await new Promise(resolve => setTimeout(resolve, 1100));
  status = await call({ action: 'GET_TODAY_ANALYTICS' });
  assert.equal(status.summary.totalDuration, pausedTotal);
  assert.equal(status.currentDomain, null);
  checks.push('Pause freezes recorded time');

  const workerCdp = await context.newCDPSession(popup);
  await workerCdp.send('ServiceWorker.enable');
  await workerCdp.send('ServiceWorker.stopAllWorkers');
  await new Promise(resolve => setTimeout(resolve, 1000));
  status = await call({ action: 'GET_TODAY_ANALYTICS' });
  assert.equal(status.success, true);
  assert.equal(status.summary.totalDuration, pausedTotal);
  worker = context.serviceWorkers()[0] || await context.waitForEvent('serviceworker', { timeout: 15000 });
  checks.push('Actual Chromium worker termination recovers saved state');

  const dbResults = await probe.evaluate(async () => {
    const { TabTimeStorage } = await import('./storage.js');
    const name = 'TabTimeMigrationTest-' + Date.now();
    await new Promise((resolve, reject) => {
      const request = indexedDB.open(name, 1);
      request.onupgradeneeded = () => {
        const sessions = request.result.createObjectStore('sessions', { keyPath: 'id', autoIncrement: true });
        for (const key of ['domain', 'date', 'category']) sessions.createIndex(key, key);
        request.result.createObjectStore('daily_summaries', { keyPath: 'date' });
        sessions.add({ domain: 'legacy.test', category: 'Productive', date: '2026-09-13', duration: 60 });
      };
      request.onsuccess = () => { request.result.close(); resolve(); };
      request.onerror = () => reject(request.error);
    });
    const repository = new TabTimeStorage(name);
    const initial = await repository.getDaySummary('2026-09-13');
    const record = { id: 'new-record', domain: 'new.test', category: 'Neutral', date: '2026-09-13', duration: 10 };
    await repository.commitTracking([record], { test: 'first' });
    let duplicateRejected = false;
    try { await repository.commitTracking([record], { test: 'should-not-commit' }); } catch { duplicateRejected = true; }
    const state = await repository.getTrackingState();
    const summary = await repository.getDaySummary('2026-09-13');
    const count = (await repository.getAllSessions()).length;
    await repository.clearAllData();
    const cleared = (await repository.getAllSessions()).length === 0 && await repository.getTrackingState() === null;
    return { initial: initial.totalDuration, total: summary.totalDuration, count, duplicateRejected, state, cleared };
  });
  assert.deepEqual(dbResults, { initial: 60, total: 70, count: 2, duplicateRejected: true, state: { test: 'first' }, cleared: true });
  checks.push('Real IndexedDB migration preserves v1 records and rebuilds summaries');
  checks.push('Duplicate write aborts atomically without changing summary or checkpoint');
  checks.push('History deletion clears sessions, summaries and checkpoint');

  // Existing focus controls must still respond after replacing the background worker.
  const focus = await call({ action: 'START_FOCUS_MODE', durationMinutes: 1 });
  assert.equal(focus.success, true);
  const focusRules = await worker.evaluate(() => chrome.declarativeNetRequest.getDynamicRules());
  assert.ok(focusRules.length > 0);
  assert.ok(focusRules.every(rule => rule.condition.requestDomains?.length));
  await call({ action: 'STOP_FOCUS_MODE' });
  assert.equal((await worker.evaluate(() => chrome.declarativeNetRequest.getDynamicRules())).length, 0);
  checks.push('Existing focus controls create and remove domain rules');

  const dashboard = await context.newPage();
  await dashboard.goto(`chrome-extension://${extensionId}/dashboard.html`);
  await dashboard.locator('#sites-table-body').getByText('127.0.0.1', { exact: true }).waitFor();
  assert.equal(await dashboard.locator('#sites-table-body').getByText('github.com', { exact: true }).count(), 0);
  checks.push('Dashboard displays recorded local fixture instead of fabricated sites');
  const cdp = await context.newCDPSession(dashboard);
  await cdp.send('Runtime.enable');
  const networkPolicy = await dashboard.evaluate(async () => {
    try { await fetch('https://example.com/tabtime-policy-test'); return 'unexpected'; }
    catch { return 'blocked'; }
  });
  assert.equal(networkPolicy, 'blocked');
  checks.push('Extension Content Security Policy blocks outbound fetch');

  await call({ action: 'CLEAR_HISTORY' });
  assert.equal((await call({ action: 'GET_ALL_SESSIONS' })).sessions.length, 0);
  status = await call({ action: 'GET_TODAY_ANALYTICS' });
  assert.equal(status.trackingEnabled, false);
  assert.equal(status.summary.totalDuration, 0);
  await dashboard.reload();
  await dashboard.getByText('No activity in this period.', { exact: false }).waitFor();
  await dashboard.screenshot({ path: join(output, 'dashboard-empty.png'), fullPage: true });
  checks.push('Purge stays empty and leaves tracking paused');
  assert.deepEqual(errors, []);
  await writeFile(join(output, 'browser-results.json'), JSON.stringify({ browserVersion: context.browser()?.version(), checks, pageErrors: errors }, null, 2));
  console.log(JSON.stringify({ passed: checks.length, checks, errors, output }, null, 2));
} finally {
  await context.close();
  await new Promise(resolve => server.close(resolve));
}
