/**
 * Tab Time - Settings Logic
 * Manages domain categorization rules, blocklists, and data purging.
 */

import { TabTimeStorage, DEFAULT_CATEGORY_RULES, DEFAULT_BLOCKLIST } from './storage.js';

const storage = new TabTimeStorage();

document.addEventListener('DOMContentLoaded', async () => {
  setupNavigation();
  await loadCategoryRules();
  await loadBlocklist();
  setupEventListeners();
});

function setupNavigation() {
  document.getElementById('back-dashboard-btn').addEventListener('click', () => {
    chrome.tabs.create({ url: chrome.runtime.getURL('dashboard.html') });
  });
}

async function loadCategoryRules() {
  const { categoryRules = DEFAULT_CATEGORY_RULES } = await chrome.storage.local.get('categoryRules');
  const tbody = document.getElementById('rules-tbody');
  tbody.innerHTML = '';

  Object.entries(categoryRules).forEach(([domain, category]) => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${domain}</strong></td>
      <td><span class="badge badge-${category.toLowerCase()}">${category}</span></td>
      <td style="text-align: center;">
        <button class="delete-btn" data-domain="${domain}">Delete</button>
      </td>
    `;
    tbody.appendChild(tr);
  });

  document.querySelectorAll('.delete-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      const dom = e.target.dataset.domain;
      delete categoryRules[dom];
      await chrome.storage.local.set({ categoryRules });
      await loadCategoryRules();
    });
  });
}

async function loadBlocklist() {
  const { focusBlocklist = DEFAULT_BLOCKLIST } = await chrome.storage.local.get('focusBlocklist');
  const container = document.getElementById('blocklist-chips-container');
  container.innerHTML = '';

  focusBlocklist.forEach(domain => {
    const chip = document.createElement('div');
    chip.className = 'chip';
    chip.innerHTML = `
      <span>${domain}</span>
      <span class="chip-remove" data-domain="${domain}">&times;</span>
    `;
    container.appendChild(chip);
  });

  document.querySelectorAll('.chip-remove').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      const dom = e.target.dataset.domain;
      const updated = focusBlocklist.filter(d => d !== dom);
      await chrome.storage.local.set({ focusBlocklist: updated });
      await loadBlocklist();
    });
  });
}

function setupEventListeners() {
  // Add Rule
  document.getElementById('add-rule-btn').addEventListener('click', async () => {
    const domInput = document.getElementById('new-domain-input');
    const catSelect = document.getElementById('new-category-select');

    let domain = domInput.value.trim().toLowerCase();
    if (domain.startsWith('http://') || domain.startsWith('https://')) {
      try {
        domain = new URL(domain).hostname;
      } catch (e) {}
    }
    if (domain.startsWith('www.')) domain = domain.substring(4);

    if (domain) {
      const { categoryRules = DEFAULT_CATEGORY_RULES } = await chrome.storage.local.get('categoryRules');
      categoryRules[domain] = catSelect.value;
      await chrome.storage.local.set({ categoryRules });
      domInput.value = '';
      await loadCategoryRules();
    }
  });

  // Add Block
  document.getElementById('add-block-btn').addEventListener('click', async () => {
    const blockInput = document.getElementById('new-block-domain');
    let domain = blockInput.value.trim().toLowerCase();
    if (domain.startsWith('http://') || domain.startsWith('https://')) {
      try {
        domain = new URL(domain).hostname;
      } catch (e) {}
    }
    if (domain.startsWith('www.')) domain = domain.substring(4);

    if (domain) {
      const { focusBlocklist = DEFAULT_BLOCKLIST } = await chrome.storage.local.get('focusBlocklist');
      if (!focusBlocklist.includes(domain)) {
        focusBlocklist.push(domain);
        await chrome.storage.local.set({ focusBlocklist });
        blockInput.value = '';
        await loadBlocklist();
      }
    }
  });

  // Export JSON
  document.getElementById('settings-export-btn').addEventListener('click', async () => {
    const allSessions = await storage.getAllSessions();
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(allSessions, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute('href', dataStr);
    downloadAnchor.setAttribute('download', `tabtime_export_${Date.now()}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  });

  // Purge Data
  document.getElementById('settings-purge-btn').addEventListener('click', async () => {
    if (confirm('Are you sure you want to permanently delete all tracking history? This action cannot be undone.')) {
      const response = await chrome.runtime.sendMessage({ action: 'CLEAR_HISTORY' });
      if (!response?.success) {
        alert(response?.error || 'Unable to clear history. Please try again.');
        return;
      }
      alert('Tracking history was cleared. Your category rules and focus blocklist were kept.');
      location.reload();
    }
  });
}
