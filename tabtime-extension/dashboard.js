/**
 * Tab Time - Full Analytics Dashboard Logic
 * Provides multi-day trend analysis, category aggregations, and data export.
 */

import { TabTimeStorage, DEFAULT_CATEGORY_RULES } from './storage.js';
import { CATEGORIES, localDate } from './tracking-core.js';

const storage = new TabTimeStorage();

let weeklyChart = null;
let donutChart = null;
let currentRange = 'today';

const CATEGORY_COLORS = {
  Productive: '#2E7D32',
  Educational: '#1565C0',
  Social: '#E65100',
  Entertainment: '#C2185B',
  Neutral: '#607D8B'
};

document.addEventListener('DOMContentLoaded', async () => {
  setupFilterPills();
  setupActionButtons();
  await refreshDashboardData();
});

function setupFilterPills() {
  const pills = document.querySelectorAll('.pill-btn');
  pills.forEach(pill => {
    pill.addEventListener('click', async () => {
      pills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');
      currentRange = pill.dataset.range;
      await refreshDashboardData();
    });
  });
}

function setupActionButtons() {
  document.getElementById('settings-nav-btn').addEventListener('click', () => {
    chrome.tabs.create({ url: chrome.runtime.getURL('settings.html') });
  });

  document.getElementById('export-json-btn').addEventListener('click', async () => {
    const allSessions = await storage.getAllSessions();
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(allSessions, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute('href', dataStr);
    downloadAnchor.setAttribute('download', `tabtime_backup_${new Date().toISOString().split('T')[0]}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  });
}

async function refreshDashboardData() {
  const result = await chrome.runtime.sendMessage({ action: 'GET_ALL_SESSIONS' });
  if (!result?.success) throw new Error(result?.error || 'Unable to load history.');
  const sessions = result.sessions;

  // Filter sessions based on selected range
  const filtered = filterSessionsByRange(sessions, currentRange);

  updateKPICards(filtered);
  renderWeeklyStackedChart(filtered);
  renderCategoryDonutChart(filtered);
  renderSitesTable(filtered);
}

function filterSessionsByRange(sessions, range) {
  const now = new Date();
  let daysCutoff = 7;
  if (range === 'today') daysCutoff = 1;
  if (range === 'month') daysCutoff = 30;

  now.setHours(0, 0, 0, 0);
  now.setDate(now.getDate() - daysCutoff + 1);
  const cutoffDate = localDate(now.getTime());
  const today = localDate();
  return sessions.filter(s => s.date >= cutoffDate && s.date <= today);
}

function updateKPICards(sessions) {
  let totalSec = 0;
  const categoryTotals = { Productive: 0, Educational: 0, Social: 0, Entertainment: 0, Neutral: 0 };
  const domainTotals = {};

  sessions.forEach(s => {
    const dur = s.duration || 0;
    const cat = s.category || 'Neutral';
    const dom = s.domain;

    totalSec += dur;
    categoryTotals[cat] = (categoryTotals[cat] || 0) + dur;
    domainTotals[dom] = (domainTotals[dom] || 0) + dur;
  });

  // KPI 1: Total Active Time
  document.getElementById('kpi-total-time').textContent = formatHoursMins(totalSec);

  // KPI 2: Productivity Score
  let prodScore = 0;
  if (totalSec > 0) {
    const weighted = categoryTotals.Productive + categoryTotals.Educational + (0.5 * categoryTotals.Neutral);
    prodScore = Math.round((weighted / totalSec) * 100);
  }
  document.getElementById('kpi-score').textContent = `${prodScore}%`;

  // KPI 3: Top Productive Site
  let topSite = '--';
  let topTime = 0;
  Object.entries(domainTotals).forEach(([dom, dur]) => {
    if (dur > topTime) {
      topTime = dur;
      topSite = dom;
    }
  });
  document.getElementById('kpi-top-site').textContent = topSite;
  document.getElementById('kpi-top-time').textContent = `${formatHoursMins(topTime)} spent`;

  // KPI 4: Distraction Time
  const distractSec = categoryTotals.Social + categoryTotals.Entertainment;
  const distractPct = totalSec > 0 ? Math.round((distractSec / totalSec) * 100) : 0;
  document.getElementById('kpi-distract-time').textContent = formatHoursMins(distractSec);
  document.getElementById('kpi-distract-pct').textContent = `${distractPct}% of total browsing`;
}

function renderWeeklyStackedChart(sessions) {
  const ctx = document.getElementById('weeklyBarChart').getContext('2d');

  const count = currentRange === 'today' ? 1 : currentRange === 'month' ? 30 : 7;
  const dates = Array.from({ length: count }, (_, index) => {
    const day = new Date();
    day.setDate(day.getDate() - count + 1 + index);
    return localDate(day.getTime());
  });
  const days = dates.map(date => new Date(date + 'T12:00:00').toLocaleDateString(undefined, { month: 'short', day: 'numeric' }));
  const dataByDay = Object.fromEntries(CATEGORIES.map(cat => [cat, dates.map(() => 0)]));
  for (const session of sessions) {
    const index = dates.indexOf(session.date);
    const category = CATEGORIES.includes(session.category) ? session.category : 'Neutral';
    if (index >= 0) dataByDay[category][index] += session.duration / 3600;
  }

  if (weeklyChart) weeklyChart.destroy();

  weeklyChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: days,
      datasets: Object.keys(dataByDay).map(cat => ({
        label: cat,
        data: dataByDay[cat],
        backgroundColor: CATEGORY_COLORS[cat],
        borderRadius: 4
      }))
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { stacked: true, grid: { display: false } },
        y: {
          stacked: true,
          title: { display: true, text: 'Hours' },
          ticks: { stepSize: 2 }
        }
      },
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } },
        tooltip: {
          callbacks: {
            label: (ctx) => ` ${ctx.dataset.label}: ${ctx.raw} hrs`
          }
        }
      }
    }
  });
}

function renderCategoryDonutChart(sessions) {
  const ctx = document.getElementById('categoryDonutChart').getContext('2d');

  const categoryTotals = Object.fromEntries(CATEGORIES.map(cat => [cat, 0]));
  for (const session of sessions) {
    const category = CATEGORIES.includes(session.category) ? session.category : 'Neutral';
    categoryTotals[category] += session.duration / 3600;
  }

  const labels = Object.keys(categoryTotals);
  const data = Object.values(categoryTotals);
  const total = data.reduce((a, b) => a + b, 0);

  if (donutChart) donutChart.destroy();

  donutChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: data,
        backgroundColor: labels.map(l => CATEGORY_COLORS[l]),
        borderWidth: 2,
        borderColor: '#FFFFFF'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '65%',
      plugins: {
        legend: { position: 'right', labels: { boxWidth: 12, font: { size: 11 } } },
        tooltip: {
          callbacks: {
            label: (ctx) => {
              const val = ctx.raw;
              const pct = total ? Math.round((val / total) * 100) : 0;
              return ` ${ctx.label}: ${val} hrs (${pct}%)`;
            }
          }
        }
      }
    }
  });
}

function renderSitesTable(sessions) {
  const tbody = document.getElementById('sites-table-body');
  tbody.innerHTML = '';

  const domainAggregates = Object.create(null);
  for (const session of sessions) {
    const aggregate = domainAggregates[session.domain] ||= { category: session.category, duration: 0 };
    aggregate.duration += session.duration;
  }
  if (!sessions.length) {
    const row = tbody.insertRow();
    const cell = row.insertCell();
    cell.colSpan = 5;
    cell.textContent = 'No activity in this period. Enable tracking in the popup and browse to get started.';
  }

  const totalTime = Object.values(domainAggregates).reduce((a, b) => a + b.duration, 0);

  Object.entries(domainAggregates).sort((a, b) => b[1].duration - a[1].duration).forEach(([dom, info]) => {
    const tr = document.createElement('tr');
    const pct = Math.round((info.duration / totalTime) * 100);

    tr.innerHTML = `
      <td><strong>${dom}</strong></td>
      <td><span class="badge badge-${info.category.toLowerCase()}">${info.category}</span></td>
      <td>${formatHoursMins(info.duration)}</td>
      <td>${pct}%</td>
      <td>
        <select class="category-select" data-domain="${dom}">
          <option value="Productive" ${info.category === 'Productive' ? 'selected' : ''}>Productive</option>
          <option value="Educational" ${info.category === 'Educational' ? 'selected' : ''}>Educational</option>
          <option value="Social" ${info.category === 'Social' ? 'selected' : ''}>Social</option>
          <option value="Entertainment" ${info.category === 'Entertainment' ? 'selected' : ''}>Entertainment</option>
          <option value="Neutral" ${info.category === 'Neutral' ? 'selected' : ''}>Neutral</option>
        </select>
      </td>
    `;
    tbody.appendChild(tr);
  });

  // Re-classification event
  document.querySelectorAll('.category-select').forEach(sel => {
    sel.addEventListener('change', async (e) => {
      const dom = e.target.dataset.domain;
      const newCat = e.target.value;
      const { categoryRules = DEFAULT_CATEGORY_RULES } = await chrome.storage.local.get('categoryRules');
      categoryRules[dom] = newCat;
      await chrome.storage.local.set({ categoryRules });
      await refreshDashboardData();
    });
  });
}

function formatHoursMins(totalSec) {
  const hours = Math.floor(totalSec / 3600);
  const minutes = Math.floor((totalSec % 3600) / 60);
  if (hours > 0) return `${hours}h ${minutes}m`;
  return `${minutes}m`;
}
