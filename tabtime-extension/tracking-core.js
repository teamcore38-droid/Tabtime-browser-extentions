// Pure tracking rules shared by the background worker, UI, and tests.
export const CATEGORIES = ['Productive', 'Educational', 'Social', 'Entertainment', 'Neutral'];
export const IDLE_SECONDS = 60;
export const MAX_OBSERVATION_GAP_MS = 90_000;

export function localDate(timestamp = Date.now()) {
  const date = new Date(timestamp);
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}

export function extractDomain(url) {
  try {
    const parsed = new URL(url);
    if (!['http:', 'https:'].includes(parsed.protocol)) return null;
    return parsed.hostname.toLowerCase().replace(/^www\./, '').replace(/\.$/, '') || null;
  } catch { return null; }
}

export function categoryForDomain(domain, rules = {}) {
  // Longest configured suffix wins, including multi-label domains such as ac.uk.
  const match = Object.keys(rules)
    .filter(rule => domain === rule || domain.endsWith(`.${rule}`))
    .sort((a, b) => b.length - a.length)[0];
  const category = rules[match];
  return CATEGORIES.includes(category) ? category : category === 'Education' ? 'Educational' : 'Neutral';
}

export function emptySummary(date) {
  return { date, totalDuration: 0, categories: Object.fromEntries(CATEGORIES.map(cat => [cat, 0])), domains: {} };
}

export function addToSummary(summary, record) {
  const duration = Math.max(0, Number(record.duration) || 0);
  const category = CATEGORIES.includes(record.category) ? record.category : 'Neutral';
  summary.totalDuration += duration;
  summary.categories[category] = (summary.categories[category] || 0) + duration;
  // Define an own key so even a single-label hostname like __proto__ is safe.
  Object.defineProperty(summary.domains, record.domain, {
    value: (Object.hasOwn(summary.domains, record.domain) ? summary.domains[record.domain] : 0) + duration,
    writable: true, enumerable: true, configurable: true
  });
  return summary;
}

export function productivityScore(summary) {
  if (!summary.totalDuration) return 0;
  const c = summary.categories;
  return Math.max(0, Math.min(100, Math.round(100 * ((c.Productive || 0) + (c.Educational || 0) + 0.5 * (c.Neutral || 0)) / summary.totalDuration)));
}

export function splitInterval(active, endTime) {
  const records = [];
  let startTime = active.startTime;
  while (startTime < endTime) {
    const midnight = new Date(startTime);
    midnight.setHours(24, 0, 0, 0);
    const end = Math.min(endTime, midnight.getTime());
    records.push({
      id: `${active.id}:${startTime}:${end}`,
      domain: active.domain, category: active.category,
      startTime, endTime: end, duration: (end - startTime) / 1000, date: localDate(startTime)
    });
    startTime = end;
  }
  return records;
}

export function trackingTarget(snapshot, rules) {
  const tab = snapshot.tab;
  if (!snapshot.enabled) return { reason: 'paused' };
  if (snapshot.idleState !== 'active') return { reason: snapshot.idleState === 'locked' ? 'locked' : 'idle' };
  if (!snapshot.focused) return { reason: 'unfocused' };
  if (tab?.incognito) return { reason: 'private' };
  const domain = tab?.active && !tab.discarded ? extractDomain(tab.url) : null;
  if (!domain) return { reason: 'unsupported' };
  return { reason: 'tracking', domain, category: categoryForDomain(domain, rules), tabId: tab.id, windowId: tab.windowId };
}

export class TrackingEngine {
  constructor(repository, browserSessionId, newId = () => crypto.randomUUID()) {
    this.repository = repository;
    this.browserSessionId = browserSessionId;
    this.newId = newId;
    this.state = null;
  }

  async observe(snapshot, rules = {}) {
    const previous = this.state || await this.repository.getTrackingState() || { active: null, observedAt: snapshot.at };
    // Queued event timestamps are monotonic, even if an OS clock adjustment occurs.
    const at = Math.max(snapshot.at, previous.observedAt);
    const target = trackingTarget(snapshot, rules);
    const old = previous.active;
    const sameBrowser = previous.browserSessionId === this.browserSessionId;
    const continuous = sameBrowser && snapshot.at >= previous.observedAt && at - previous.observedAt <= MAX_OBSERVATION_GAP_MS;
    const endTime = continuous ? at : previous.observedAt;
    let records = [];
    let cursor = old?.startTime;
    if (old && endTime - old.startTime >= 1000) {
      records = splitInterval(old, endTime);
      cursor = endTime;
    }
    const sameTarget = continuous && old && target.reason === 'tracking' &&
      old.domain === target.domain && old.category === target.category &&
      old.tabId === target.tabId && old.windowId === target.windowId;
    const active = target.reason !== 'tracking' ? null : sameTarget ? { ...old, startTime: cursor } : {
      id: this.newId(), domain: target.domain, category: target.category,
      tabId: target.tabId, windowId: target.windowId, startTime: at, visitStartTime: at
    };
    const next = { browserSessionId: this.browserSessionId, observedAt: at, active, reason: target.reason };
    // History, summaries and the cursor commit together. Failed writes leave the old state retryable.
    await this.repository.commitTracking(records, next);
    this.state = next;
    return this.status();
  }

  status() {
    const state = this.state;
    return {
      reason: state?.reason || 'paused', activeSession: state?.active || null,
      currentDomain: state?.active?.domain || null, currentCategory: state?.active?.category || 'Neutral',
      elapsedSeconds: state?.active ? Math.max(0, (state.observedAt - state.active.visitStartTime) / 1000) : 0
    };
  }
}
