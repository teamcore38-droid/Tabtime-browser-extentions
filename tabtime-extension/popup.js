import { CATEGORIES } from './tracking-core.js';

const CATEGORY_COLORS = { Productive: '#2E7D32', Educational: '#1565C0', Social: '#E65100', Entertainment: '#C2185B', Neutral: '#607D8B' };
let categoryChart;
let trackingEnabled = false;
let refreshing = false;

async function send(message) {
  const result = await chrome.runtime.sendMessage(message);
  if (!result?.success) throw new Error(result?.error || 'Unable to reach Tab Time. Reload the extension and try again.');
  return result;
}
function showError(error) {
  const element = document.getElementById('popup-error');
  element.textContent = error.message;
  element.hidden = false;
}
document.addEventListener('DOMContentLoaded', () => {
  for (const [id, page] of [['open-dashboard-btn', 'dashboard.html'], ['view-dashboard-link', 'dashboard.html'], ['open-settings-btn', 'settings.html']]) {
    document.getElementById(id).addEventListener('click', () => chrome.tabs.create({ url: chrome.runtime.getURL(page) }));
  }
  document.getElementById('toggle-tracking-btn').addEventListener('click', async event => {
    event.target.disabled = true;
    try { await send({ action: 'SET_TRACKING_ENABLED', enabled: !trackingEnabled }); await refresh(); }
    catch (error) { showError(error); }
    finally { event.target.disabled = false; }
  });
  setupFocusControls();
  refresh();
  setInterval(refresh, 1000);
});

async function refresh() {
  if (refreshing) return;
  refreshing = true;
  try {
    const result = await send({ action: 'GET_TODAY_ANALYTICS' });
    trackingEnabled = result.trackingEnabled;
    const labels = { paused: 'Tracking paused', idle: 'Paused while idle', locked: 'Paused while locked', unfocused: 'Browser not focused', private: 'Private window excluded', unsupported: 'This page is not tracked', tracking: 'Tracking active tab' };
    document.getElementById('tracking-status').textContent = labels[result.reason] || 'Tracking paused';
    document.getElementById('toggle-tracking-btn').textContent = trackingEnabled ? 'Pause tracking' : 'Enable tracking';
    document.getElementById('current-domain').textContent = result.currentDomain || labels[result.reason];
    const badge = document.getElementById('current-category-badge');
    badge.textContent = result.currentDomain ? result.currentCategory : 'Paused';
    badge.className = 'badge badge-' + (result.currentDomain ? result.currentCategory.toLowerCase() : 'neutral');
    document.getElementById('today-time').textContent = formatDuration(result.summary.totalDuration);
    const score = document.getElementById('today-score');
    score.textContent = result.summary.totalDuration ? result.score + '%' : '—';
    score.style.color = result.summary.totalDuration ? result.score >= 70 ? '#2E7D32' : result.score >= 45 ? '#A55A00' : '#C62828' : '#607D8B';
    document.getElementById('chart-empty').hidden = result.summary.totalDuration > 0;
    document.getElementById('chart-summary').textContent = CATEGORIES.map(category => category + ': ' + formatDuration(result.summary.categories[category] || 0)).join('. ');
    renderDonutChart(result.summary.categories);
    document.getElementById('popup-error').hidden = true;
  } catch (error) {
    document.getElementById('tracking-status').textContent = 'Tracking status unavailable';
    showError(error);
  } finally { refreshing = false; }
}

function formatDuration(value) {
  const seconds = Math.max(0, Math.floor(value));
  if (seconds < 60) return seconds + 's';
  const minutes = Math.floor(seconds / 60);
  return minutes < 60 ? minutes + 'm ' + seconds % 60 + 's' : Math.floor(minutes / 60) + 'h ' + minutes % 60 + 'm';
}

function renderDonutChart(totals) {
  const values = CATEGORIES.map(cat => totals[cat] || 0);
  const total = values.reduce((a, b) => a + b, 0);
  const data = {
    labels: total ? CATEGORIES : ['No activity yet'],
    datasets: [{ data: total ? values : [1], backgroundColor: total ? CATEGORIES.map(cat => CATEGORY_COLORS[cat]) : ['#E0E4EC'], borderWidth: 2, borderColor: '#FFFFFF' }]
  };
  if (categoryChart) {
    categoryChart.data = data;
    categoryChart.update('none');
    return;
  }
  categoryChart = new Chart(document.getElementById('todayCategoryChart'), {
    type: 'doughnut', data,
    options: {
      responsive: true, maintainAspectRatio: false, cutout: '70%', animation: false,
      plugins: {
        legend: { position: 'right', labels: { boxWidth: 10, font: { size: 10 } } },
        tooltip: { callbacks: { label: context => context.label === 'No activity yet' ? 'No browsing recorded today' : context.label + ': ' + formatDuration(context.raw) } }
      }
    }
  });
}

// Focus Mode Button & Timer Logic
function setupFocusControls() {
  const toggleBtn = document.getElementById('toggle-focus-btn');
  const statusBadge = document.getElementById('focus-status-badge');
  const countdownEl = document.getElementById('focus-countdown');

  let countdownInterval = null;

  async function updateFocusUI() {
    const { focusState } = await chrome.storage.local.get('focusState');
    if (focusState && focusState.active && focusState.endTime > Date.now()) {
      toggleBtn.textContent = 'Stop Focus Session';
      toggleBtn.className = 'btn btn-danger';
      statusBadge.textContent = 'Active';
      statusBadge.className = 'badge badge-active';
      countdownEl.classList.remove('hidden');

      if (countdownInterval) clearInterval(countdownInterval);
      countdownInterval = setInterval(() => {
        const remaining = Math.max(0, Math.ceil((focusState.endTime - Date.now()) / 1000));
        if (remaining <= 0) {
          clearInterval(countdownInterval);
          updateFocusUI().catch(showError);
        } else {
          const mins = Math.floor(remaining / 60);
          const secs = remaining % 60;
          countdownEl.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }
      }, 1000);
    } else {
      toggleBtn.textContent = 'Start 25m Focus Session';
      toggleBtn.className = 'btn btn-primary';
      statusBadge.textContent = 'Ready';
      statusBadge.className = 'badge badge-idle';
      countdownEl.classList.add('hidden');
      if (countdownInterval) clearInterval(countdownInterval);
    }
  }

  updateFocusUI().catch(showError);

  toggleBtn.addEventListener('click', async () => {
    toggleBtn.disabled = true;
    try {
    const { focusState } = await chrome.storage.local.get('focusState');
    if (focusState && focusState.active) {
      await send({ action: 'STOP_FOCUS_MODE' });
    } else {
      await send({ action: 'START_FOCUS_MODE', durationMinutes: 25 });
    }
    await updateFocusUI();
    } catch (error) { showError(error); } finally { toggleBtn.disabled = false; }
  });
}
