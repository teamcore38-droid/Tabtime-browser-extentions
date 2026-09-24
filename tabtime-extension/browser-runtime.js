import { TrackingEngine, IDLE_SECONDS, localDate, productivityScore } from './tracking-core.js';
import { DEFAULT_CATEGORY_RULES, DEFAULT_BLOCKLIST } from './storage.js';

const TRACKING_ALARM = 'TRACKING_CHECKPOINT';
const FOCUS_ALARM = 'FOCUS_SESSION_END';

export function createRuntime(api, storage, now = () => Date.now()) {
  let tail = Promise.resolve();
  let engine;
  let ready;
  const enqueue = work => {
    const result = tail.then(work);
    tail = result.catch(error => console.error('[Tab Time]', error));
    return result;
  };

  async function initialize() {
    const settings = await api.storage.local.get(['categoryRules', 'focusBlocklist', 'focusState', 'trackingEnabled']);
    const defaults = {};
    if (!settings.categoryRules) defaults.categoryRules = DEFAULT_CATEGORY_RULES;
    if (!settings.focusBlocklist) defaults.focusBlocklist = DEFAULT_BLOCKLIST;
    if (!settings.focusState) defaults.focusState = { active: false, endTime: null, durationMinutes: 25 };
    // Existing prototype data is retained, but new collection requires explicit consent.
    if (typeof settings.trackingEnabled !== 'boolean') defaults.trackingEnabled = false;
    if (Object.keys(defaults).length) await api.storage.local.set(defaults);
    await api.storage.local.setAccessLevel({ accessLevel: 'TRUSTED_CONTEXTS' });
    const session = await api.storage.session.get('browserSessionId');
    const browserSessionId = session.browserSessionId || crypto.randomUUID();
    if (!session.browserSessionId) await api.storage.session.set({ browserSessionId });
    engine = new TrackingEngine(storage, browserSessionId);
    if (!await api.alarms.get(TRACKING_ALARM)) await api.alarms.create(TRACKING_ALARM, { periodInMinutes: 0.5 });
    await reconcileFocus();
  }

  async function capture(hint = {}) {
    await ready;
    const at = now();
    const [settings, idleState, window] = await Promise.all([
      api.storage.local.get(['trackingEnabled', 'categoryRules']),
      hint.idleState ? Promise.resolve(hint.idleState) : api.idle.queryState(IDLE_SECONDS),
      hint.windowId >= 0 ? api.windows.get(hint.windowId) : api.windows.getLastFocused({ windowTypes: ['normal'] }).catch(() => null)
    ]);
    // Activations/navigation in another window must not interrupt the foreground session.
    if (hint.tabId !== undefined && !window?.focused) return { ignore: true };
    let tab = null;
    if (window && hint.windowId !== api.windows.WINDOW_ID_NONE) {
      tab = hint.tabId !== undefined
        ? await api.tabs.get(hint.tabId).catch(() => null)
        : (await api.tabs.query({ active: true, windowId: window.id }))[0];
    }
    return { at, enabled: settings.trackingEnabled === true, idleState,
      focused: hint.windowId !== api.windows.WINDOW_ID_NONE && window?.focused === true && window?.type === 'normal',
      tab, rules: settings.categoryRules || DEFAULT_CATEGORY_RULES };
  }

  function schedule(hint) {
    // Begin browser reads at event receipt, then apply completed observations in FIFO order.
    const snapshot = capture(hint).then(value => ({ value }), error => ({ error }));
    return enqueue(async () => {
      const result = await snapshot;
      if (result.error) throw result.error;
      if (result.value.ignore) return engine.status();
      // A queued observation cannot re-enable collection after pause or history deletion.
      const latest = await api.storage.local.get(['trackingEnabled', 'categoryRules']);
      result.value.enabled = latest.trackingEnabled === true;
      result.value.rules = latest.categoryRules || result.value.rules;
      return engine.observe(result.value, result.value.rules);
    });
  }

  async function stopFocus() {
    const rules = await api.declarativeNetRequest.getDynamicRules();
    await api.declarativeNetRequest.updateDynamicRules({ removeRuleIds: rules.map(rule => rule.id), addRules: [] });
    await api.storage.local.set({ focusState: { active: false, endTime: null, durationMinutes: 25 } });
    await api.alarms.clear(FOCUS_ALARM);
  }

  async function reconcileFocus() {
    const { focusState } = await api.storage.local.get('focusState');
    if (focusState?.active && focusState.endTime > now()) {
      await api.alarms.create(FOCUS_ALARM, { when: focusState.endTime });
    } else if (focusState?.active || (await api.declarativeNetRequest.getDynamicRules()).length) {
      await stopFocus();
    }
  }

  async function startFocus(durationMinutes) {
    if (!Number.isInteger(durationMinutes) || durationMinutes < 1 || durationMinutes > 180) throw new Error('Choose a focus duration between 1 and 180 minutes.');
    const { focusBlocklist = DEFAULT_BLOCKLIST } = await api.storage.local.get('focusBlocklist');
    const domains = [...new Set(focusBlocklist)].filter(domain => typeof domain === 'string' && /^(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z]{2,}$/i.test(domain));
    const current = await api.declarativeNetRequest.getDynamicRules();
    await api.declarativeNetRequest.updateDynamicRules({
      removeRuleIds: current.map(rule => rule.id),
      addRules: domains.map((domain, index) => ({
        id: index + 1, priority: 1,
        action: { type: 'redirect', redirect: { url: `${api.runtime.getURL('blocked.html')}?blocked=${encodeURIComponent(domain)}` } },
        condition: { requestDomains: [domain], resourceTypes: ['main_frame'] }
      }))
    });
    const endTime = now() + durationMinutes * 60_000;
    try {
      await api.storage.local.set({ focusState: { active: true, endTime, durationMinutes } });
      await api.alarms.create(FOCUS_ALARM, { when: endTime });
    } catch (error) { await stopFocus(); throw error; }
  }

  async function message(action) {
    await ready;
    if (action.action === 'START_FOCUS_MODE') await startFocus(action.durationMinutes ?? 25);
    else if (action.action === 'STOP_FOCUS_MODE') await stopFocus();
    else if (action.action === 'SET_TRACKING_ENABLED') {
      if (typeof action.enabled !== 'boolean') throw new Error('Tracking choice must be true or false.');
      const before = await capture();
      await engine.observe(before, before.rules);
      await api.storage.local.set({ trackingEnabled: action.enabled });
      if (action.enabled) await api.storage.local.set({ trackingConsentAt: now() });
      const after = await capture();
      await engine.observe(after, after.rules);
    } else if (action.action === 'CLEAR_HISTORY') {
      // One writer owns deletion and tracking, so an old cursor cannot recreate purged history.
      await api.storage.local.set({ trackingEnabled: false });
      await storage.clearAllData();
      engine.state = null;
      await api.storage.local.remove(['activeSessionCheckpoint', 'todayTotals']);
      await stopFocus();
    } else if (!['GET_ACTIVE_STATUS', 'GET_TODAY_ANALYTICS', 'GET_ALL_SESSIONS'].includes(action.action)) {
      throw new Error('Unknown Tab Time action.');
    }
    const snapshot = await capture();
    const status = await engine.observe(snapshot, snapshot.rules);
    if (action.action === 'GET_ALL_SESSIONS') return { success: true, sessions: await storage.getAllSessions() };
    const summary = await storage.getDaySummary(localDate(snapshot.at));
    return { success: true, ...status, trackingEnabled: snapshot.enabled, summary, score: productivityScore(summary) };
  }

  function register() {
    ready = initialize();
    api.idle.setDetectionInterval(IDLE_SECONDS);
    const observe = hint => { void schedule(hint).catch(() => {}); };
    api.tabs.onActivated.addListener(info => observe(info));
    api.tabs.onUpdated.addListener((tabId, change, tab) => { if ((change.url || change.discarded) && tab.active) observe({ tabId, windowId: tab.windowId }); });
    api.tabs.onRemoved.addListener(() => observe());
    api.windows.onFocusChanged.addListener(windowId => observe({ windowId }));
    api.idle.onStateChanged.addListener(idleState => observe({ idleState }));
    api.runtime.onInstalled.addListener(() => observe());
    api.runtime.onStartup.addListener(() => observe());
    api.storage.onChanged.addListener((changes, area) => {
      if (area === 'local' && changes.categoryRules) observe();
    });
    api.alarms.onAlarm.addListener(alarm => {
      if (alarm.name === TRACKING_ALARM) {
        observe();
        void enqueue(async () => { await ready; await reconcileFocus(); }).catch(() => {});
      }
      if (alarm.name === FOCUS_ALARM) void enqueue(async () => { await ready; await reconcileFocus(); }).catch(() => {});
    });
    api.runtime.onMessage.addListener((request, sender, respond) => {
      if (sender.id !== api.runtime.id || !sender.url?.startsWith(api.runtime.getURL(''))) return false;
      enqueue(() => message(request)).then(respond, error => respond({ success: false, error: error.message }));
      return true;
    });
    observe();
  }

  return { register, schedule, dispatch: request => enqueue(() => message(request)), settled: () => tail };
}
