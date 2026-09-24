import test from 'node:test';
import assert from 'node:assert/strict';
import { TrackingEngine, extractDomain, categoryForDomain, emptySummary, addToSummary, productivityScore, localDate, splitInterval } from '../tabtime-extension/tracking-core.js';

class MemoryRepository {
  state = null;
  records = [];
  failNext = false;
  async getTrackingState() { return structuredClone(this.state); }
  async commitTracking(records, state) {
    if (this.failNext) { this.failNext = false; throw new Error('disk full'); }
    this.records.push(...structuredClone(records));
    this.state = structuredClone(state);
  }
}
const base = new Date(2026, 8, 13, 12).getTime();
const rules = { 'github.com': 'Productive', 'youtube.com': 'Entertainment', 'yorksj.ac.uk': 'Educational', 'docs.google.com': 'Productive' };
const snapshot = (seconds, overrides = {}) => ({ at: base + seconds * 1000, enabled: true, idleState: 'active', focused: true, tab: { id: 1, windowId: 1, active: true, url: 'https://github.com/private?secret=1', incognito: false }, ...overrides });
const tab = (id, url, windowId = 1) => ({ id, windowId, active: true, url });
const sum = repo => repo.records.reduce((total, record) => total + record.duration, 0);
function setup(sessionId = 'browser-1') {
  const repo = new MemoryRepository();
  let id = 0;
  return { repo, engine: new TrackingEngine(repo, sessionId, () => String(++id)) };
}

test('only HTTP(S) hostnames are retained, without path, query or title', () => {
  assert.equal(extractDomain('https://WWW.GitHub.COM./secret?token=123'), 'github.com');
  for (const url of ['chrome://extensions', 'edge://newtab', 'about:blank', 'file:///report.docx', 'chrome-extension://abcd/popup.html', 'ftp://example.com', 'not a URL']) assert.equal(extractDomain(url), null);
});
test('most specific domain rule wins with safe label boundaries', () => {
  assert.equal(categoryForDomain('library.yorksj.ac.uk', rules), 'Educational');
  assert.equal(categoryForDomain('github.com.evil.test', rules), 'Neutral');
  assert.equal(categoryForDomain('notgithub.com', rules), 'Neutral');
  assert.equal(categoryForDomain('docs.google.com', { 'google.com': 'Neutral', ...rules }), 'Productive');
  assert.equal(categoryForDomain('github.com', { 'github.com': 'Unknown' }), 'Neutral');
});
test('report score formula, empty history and neutral weighting', () => {
  const summary = emptySummary('2026-09-13');
  assert.equal(productivityScore(summary), 0);
  addToSummary(summary, { domain: 'github.com', category: 'Productive', duration: 3600 });
  addToSummary(summary, { domain: 'x.com', category: 'Social', duration: 3600 });
  assert.equal(productivityScore(summary), 50);
  addToSummary(summary, { domain: 'search.test', category: 'Neutral', duration: 7200 });
  assert.equal(productivityScore(summary), 50);
});
test('special hostname keys cannot change summary object prototypes', () => {
  const summary = addToSummary(emptySummary('today'), { domain: '__proto__', category: 'Neutral', duration: 1 });
  assert.equal(summary.domains.__proto__, 1);
  assert.equal(Object.getPrototypeOf(summary.domains), Object.prototype);
});
test('local calendar dates and midnight split preserve fractional seconds', () => {
  const start = new Date(2026, 8, 13, 23, 59, 59, 500).getTime();
  const records = splitInterval({ id: 'a', domain: 'github.com', category: 'Productive', startTime: start }, start + 2000);
  assert.equal(localDate(start), '2026-09-13');
  assert.deepEqual(records.map(row => [row.date, row.duration]), [['2026-09-13', 0.5], ['2026-09-14', 1.5]]);
});
test('120 seconds recorded through checkpoints without double counting', async () => {
  const { repo, engine } = setup();
  for (const second of [0, 30, 60, 90, 120]) await engine.observe(snapshot(second), rules);
  assert.equal(sum(repo), 120);
  assert.equal(engine.status().elapsedSeconds, 120);
  assert.ok(repo.records.every(row => row.domain === 'github.com' && !Object.hasOwn(row, 'url')));
});
test('tracking stays off before consent', async () => {
  const { repo, engine } = setup();
  await engine.observe(snapshot(0, { enabled: false }), rules);
  await engine.observe(snapshot(60, { enabled: false }), rules);
  assert.equal(sum(repo), 0);
  assert.equal(engine.status().reason, 'paused');
});
test('pause and resume do not record the paused gap', async () => {
  const { repo, engine } = setup();
  await engine.observe(snapshot(0), rules);
  await engine.observe(snapshot(20, { enabled: false }), rules);
  await engine.observe(snapshot(70, { enabled: false }), rules);
  await engine.observe(snapshot(80), rules);
  await engine.observe(snapshot(90), rules);
  assert.equal(sum(repo), 30);
});
test('idle cutoff counts the initial 60 seconds then freezes until active', async () => {
  const { repo, engine } = setup();
  await engine.observe(snapshot(0), rules);
  await engine.observe(snapshot(30), rules);
  await engine.observe(snapshot(60, { idleState: 'idle' }), rules);
  await engine.observe(snapshot(75, { idleState: 'idle' }), rules);
  assert.equal(sum(repo), 60);
  await engine.observe(snapshot(80), rules);
  await engine.observe(snapshot(90), rules);
  assert.equal(sum(repo), 70);
});
for (const [reason, override] of [
  ['unfocused', { focused: false }], ['locked', { idleState: 'locked' }],
  ['private', { tab: { ...tab(2, 'https://secret.test'), incognito: true } }],
  ['unsupported', { tab: tab(2, 'chrome://extensions') }],
  ['unsupported', { tab: { ...tab(2, 'https://discarded.test'), discarded: true } }]
]) test('stops accumulation for ' + reason, async () => {
  const { repo, engine } = setup();
  await engine.observe(snapshot(0), rules);
  await engine.observe(snapshot(10, override), rules);
  await engine.observe(snapshot(30, override), rules);
  assert.equal(sum(repo), 10);
  assert.equal(engine.status().reason, reason);
  assert.equal(engine.status().currentDomain, null);
});
test('tab switch attributes elapsed time to the old domain', async () => {
  const { repo, engine } = setup();
  await engine.observe(snapshot(0), rules);
  await engine.observe(snapshot(10, { tab: tab(2, 'https://youtube.com/watch?v=1') }), rules);
  await engine.observe(snapshot(25, { tab: tab(2, 'https://youtube.com/watch?v=2') }), rules);
  assert.deepEqual(repo.records.map(row => [row.domain, row.duration]), [['github.com', 10], ['youtube.com', 15]]);
});
test('category changes affect subsequent time without rewriting history', async () => {
  const { repo, engine } = setup();
  await engine.observe(snapshot(0), rules);
  await engine.observe(snapshot(10), { ...rules, 'github.com': 'Neutral' });
  await engine.observe(snapshot(20), { ...rules, 'github.com': 'Neutral' });
  assert.deepEqual(repo.records.map(row => row.category), ['Productive', 'Neutral']);
});
test('service worker recreation resumes the committed cursor exactly once', async () => {
  const { repo, engine } = setup();
  await engine.observe(snapshot(0), rules);
  await engine.observe(snapshot(30), rules);
  const restarted = new TrackingEngine(repo, 'browser-1');
  await restarted.observe(snapshot(60), rules);
  await restarted.observe(snapshot(60), rules);
  assert.equal(sum(repo), 60);
});
test('browser restart retains history without charging browser downtime', async () => {
  const { repo, engine } = setup();
  await engine.observe(snapshot(0), rules);
  await engine.observe(snapshot(30), rules);
  const restarted = new TrackingEngine(repo, 'browser-2');
  await restarted.observe(snapshot(3600), rules);
  await restarted.observe(snapshot(3610), rules);
  assert.equal(sum(repo), 40);
});
test('long sleep or delayed alarm gap is excluded conservatively', async () => {
  const { repo, engine } = setup();
  await engine.observe(snapshot(0), rules);
  await engine.observe(snapshot(30), rules);
  await engine.observe(snapshot(3600), rules);
  await engine.observe(snapshot(3610), rules);
  assert.equal(sum(repo), 40);
});
test('subsecond tab hops are ignored and fractional durations are not rounded up', async () => {
  const { repo, engine } = setup();
  for (let index = 0; index < 10; index++) await engine.observe(snapshot(index / 5, { tab: tab(index, 'https://github.com') }), rules);
  assert.equal(sum(repo), 0);
  await engine.observe(snapshot(3.05, { tab: tab(9, 'https://github.com') }), rules);
  assert.equal(sum(repo), 1.25);
});
test('failed storage commit leaves the cursor retryable', async () => {
  const { repo, engine } = setup();
  await engine.observe(snapshot(0), rules);
  repo.failNext = true;
  await assert.rejects(engine.observe(snapshot(20), rules), /disk full/);
  assert.equal(engine.state.observedAt, base);
  await engine.observe(snapshot(30), rules);
  assert.equal(sum(repo), 30);
});
test('clock moving backwards does not create negative records', async () => {
  const { repo, engine } = setup();
  await engine.observe(snapshot(0), rules);
  await engine.observe(snapshot(30), rules);
  await engine.observe(snapshot(20), rules);
  await engine.observe(snapshot(40), rules);
  assert.equal(sum(repo), 40);
  assert.ok(repo.records.every(record => record.duration >= 0));
});
