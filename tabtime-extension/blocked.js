/**
 * Tab Time - Focus Mode Holding Page Logic
 */

document.addEventListener('DOMContentLoaded', async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const blockedDomain = urlParams.get('blocked');

  if (blockedDomain) {
    document.getElementById('blocked-target-domain').textContent = blockedDomain;
  }

  const countdownEl = document.getElementById('focus-countdown-display');

  async function updateCountdown() {
    const { focusState } = await chrome.storage.local.get('focusState');
    if (focusState && focusState.active && focusState.endTime > Date.now()) {
      const remaining = Math.max(0, Math.round((focusState.endTime - Date.now()) / 1000));
      const mins = Math.floor(remaining / 60);
      const secs = remaining % 60;
      countdownEl.textContent = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    } else {
      countdownEl.textContent = '00:00';
    }
  }

  updateCountdown();
  setInterval(updateCountdown, 1000);

  document.getElementById('return-work-btn').addEventListener('click', () => {
    window.location.href = 'https://docs.google.com';
  });

  document.getElementById('open-dashboard-btn').addEventListener('click', () => {
    window.location.href = chrome.runtime.getURL('dashboard.html');
  });
});
