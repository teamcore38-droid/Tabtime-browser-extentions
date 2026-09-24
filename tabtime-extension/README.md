# Tab Time browser extension

Tab Time is a privacy-preserving Manifest V3 extension for Chrome, Edge, Brave, and Firefox. The first working build targets Chrome and Edge.

Tracking starts disabled. Open the toolbar popup and choose **Enable tracking** after reading the local privacy notice. Only the hostname and active duration are stored in the browser. URL paths, query strings, page contents, titles, and private windows are excluded.

## Codebase

```text
tabtime-extension/
├── manifest.json         # Manifest V3 permissions and entry points
├── background.js          # Service worker entry point
├── browser-runtime.js     # Browser event wiring, consent, focus, and messages
├── tracking-core.js       # Pure tracking, categorization, scoring, and time rules
├── storage.js             # IndexedDB sessions, summaries, migration, and checkpoints
├── popup.html / .css / .js
├── dashboard.html / .css / .js
├── settings.html / .css / .js
├── blocked.html / .css / .js
├── libs/chart.umd.js      # Offline Chart.js bundle
└── icons/                 # Toolbar and Web Store icons
```

## Load the unpacked build

1. Open Chrome or Edge and go to `chrome://extensions`.
2. Turn on **Developer mode**.
3. Choose **Load unpacked**.
4. Select `D:\My Project\Browser Extenstion project\tabtime-extension`.
5. Open the Tab Time popup, review the notice, and click **Enable tracking**. The same button pauses tracking later.

The extension requests `storage`, `tabs`, `idle`, `alarms`, and `declarativeNetRequest`, plus HTTP(S) host access for configurable focus redirects. It makes no outbound HTTP requests; Chart.js is bundled locally.

## Current build boundary

Step 1 implements explicit consent, focused active-tab tracking, local IndexedDB sessions and daily summaries, the 60-second idle cutoff, category matching, the report score formula, worker checkpoint recovery, the live popup, and real-data dashboard states. Focus controls remain available and are covered by the integration smoke test. Visual dashboard refinement, editable settings verification, exports, cross-browser support, and measured CPU/memory checks are scheduled in [the staged build plan](../documents/development/BUILD_PLAN.md).

## Screenshots and validation

For report screenshots, capture the popup, dashboard, settings page, and `blocked.html?blocked=twitter.com` after recording real activity. Do not use fabricated sample values as evaluation evidence.

From the project root, run `npm test` for the deterministic tracking suite and `npm run check` for manifest, syntax, local-resource, and network-policy checks. The isolated Chromium integration check is `scripts/browser-smoke.mjs`; its screenshots and JSON results are saved under `archive/qa/step-1/`.
