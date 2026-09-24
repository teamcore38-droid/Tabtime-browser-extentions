# TabTime staged build plan

The first implementation target is Chrome and Microsoft Edge, as confirmed on 13 September 2026. We are developing the final extension in four reviewable steps. The existing prototype is preserved in `archive/build-baselines/tabtime-extension-before-step-1.zip`.

## Requirements sources

- [Updated master report](../reports/TabTime_Final_Master_Report_Updated.docx), Chapter 3, sections 5.2 to 5.4, and Appendix C: numbered requirements, score formula, architecture, and acceptance scenarios.
- [Original IRP](../research/IRP%20.docx), sections 3.3, 3.6, 3.7, and 4.4: functional scope, local privacy, explicit consent, pause controls, and modular implementation.
- [Earlier master report](../reports/TabTime_Final_Master_Report.docx): compared for requirements consistency. The comprehensive Word report and updated master report have identical contents. The Markdown report contains the abstract, contents, and figure/table lists rather than the full chapters.
- [Interface references](../../images/screenshots/interface/): popup, dashboard, and settings visual direction for Step 2.

## Four steps

| Step | Deliverable | Completion boundary |
| --- | --- | --- |
| 1. Tracking foundation | Consent and pause/resume; active HTTP(S) tab timing; idle, focus, and private-window exclusions; categories; local persistence and daily score; working live popup | Implemented with unit and isolated Chromium checks. Manual Chrome/Edge and performance checks remain part of release validation. |
| 2. Popup and dashboard | Match the supplied interface references; improve hierarchy, top sites, daily/weekly summaries, empty/error states, keyboard access, and accessible chart alternatives | Review the user-facing screens with real recorded activity. |
| 3. Focus and settings | Complete timed focus controls, redirects and expiry recovery; validate editable category rules/blocklists; finish export and history controls | Verify end-to-end blocking, expiry, setting changes, exports, and deletion. |
| 4. Release validation | Chrome/Edge installation and upgrade checks, stopwatch comparisons, sleep/restart tests, performance measurement, privacy review, and release package | Deliver a tested unpacked build and usage guide. Firefox gets its own manifest and test pass after the agreed initial browser target. |

## Requirement mapping

| Requirement | Expected behavior | Build step |
| --- | --- | --- |
| FR-01 | Automatically measure time for the active domain in the focused normal browser window | 1 |
| FR-02 | Pause when idle detection reaches 60 seconds or the screen is locked | 1 |
| FR-03 | Productive, Educational, Social, Entertainment, and fallback Neutral categories | 1; editing completed in 3 |
| FR-04 | Score = 100 × (Productive + Educational + 0.5 × Neutral) / total active time | 1 |
| FR-05 | Live toolbar popup with daily totals and category chart | Functional in 1; visual completion in 2 |
| FR-06 | Dashboard with daily/weekly trends and top sites | Prototype demo values removed in 1; completed in 2 |
| FR-07 | Timed focus session with local redirect and automatic unblock | Existing controls retained and startup expiry reconciled in 1; full verification in 3 |
| FR-08 | User-editable categorization and blocklist | 3 |
| FR-09 | Export JSON history and delete history on demand | Deletion synchronized with tracker in 1; controls and export completed in 3 |
| NFR-01 | Less than 30 MB memory and less than 1% CPU target | Measure in 4; not yet demonstrated |
| NFR-02 | No telemetry or cloud processing; local-only persistence | 1 through 4 |
| NFR-03 | Simple accessible UI and SUS score above 75 | UI in 2; requires a new user evaluation |
| NFR-04 | Recover saved history and tracking state after worker/browser restart | 1; extended real-device testing in 4 |
| IRP 3.7 | Explicitly enable tracking before collection; user can pause and delete history | 1 |

## Implementation decisions and report discrepancies

- Tracking starts disabled, including when upgrading the prototype without a saved consent choice. Enabling it records domains and timing only. No page titles, paths, queries, page contents, or private browsing are recorded.
- Daily totals use the device's local calendar date, including midnight splits. This avoids UTC day boundaries shifting Sri Lankan activity into the wrong day. Existing v1 record dates are preserved because they cannot be safely reinterpreted without a migration decision.
- Timing pauses when the browser emits its 60-second idle transition. The initial 60 seconds count, matching Appendix C, TC-02. Browser scheduling delay still needs stopwatch validation.
- Subsecond transient intervals are ignored; retained durations preserve fractional seconds. Category changes affect subsequent time, preserving historical classifications.
- Checkpoints run every 30 seconds when the popup is closed. A shared browser-session identifier distinguishes ordinary worker suspension from a browser restart. Session rows, daily summaries, and the cursor commit in one IndexedDB transaction.
- On crash/restart, only committed observations are trusted. No browser-closed time is added. A gap over 90 seconds is treated conservatively as unobserved time, including long device sleep or delayed alarms. This can undercount activity; it does not establish the report's claim of zero data loss. Under normal alarm scheduling, an unexpected termination can lose the tail since the last checkpoint, usually up to 30 seconds. Short device sleeps within that gap threshold still need real-device evaluation.
- This first build sets Chrome 120 as its minimum for 30-second alarms, rather than the report's Chrome 110 target. [Chrome service-worker lifecycle](https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/lifecycle) documents the alarm change.
- The report says redirect blocking needs no host permissions. Chrome's redirect behavior does require the applicable host access, so the prototype's host permissions are narrowed to HTTP(S). Their presence is disclosed in the installation guide. Permission minimization for configurable blocking is part of Step 3. See the [Chrome declarativeNetRequest documentation](https://developer.chrome.com/docs/extensions/reference/api/declarativeNetRequest).
- Privacy is supported by local storage, no network client code, bundled Chart.js, and a `connect-src 'none'` extension policy. Absence of host permissions alone would not prove privacy. [Chrome storage documentation](https://developer.chrome.com/docs/extensions/reference/api/storage) explains session storage lifetime.
- The report's historical survey results, timing accuracy, CPU/memory figures, and PASS labels are source material, not test results for this implementation. No survey responses are bundled into the extension, and dashboard sample values were removed.

## Current checks

Run `npm test` for the deterministic tracking cases and `npm run check` for syntax, manifest resources, and network API checks. `scripts/browser-smoke.mjs` uses Playwright and an isolated temporary browser profile for integration checks; provide `TABTIME_PLAYWRIGHT_DIR` and optionally `TABTIME_CHROMIUM_PATH` if those dependencies are not on the normal Node resolution path. Headless Chromium reports the operating-system idle state and cannot expose a real desktop user gesture, so the smoke harness seeds one committed local fixture in that branch; active/idle accumulation itself is tested deterministically in `tests/tracking.test.js`. Results and UI screenshots are saved in `archive/qa/step-1/`.

Next review: Step 2, the popup and dashboard interface based on the supplied screenshots.
