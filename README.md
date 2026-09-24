# TabTime: Privacy-Preserving Browser Extension for Digital Wellbeing

[![Manifest V3](https://img.shields.io/badge/Manifest-V3-blue.svg)](https://developer.chrome.com/docs/extensions/mv3/intro/)
[![Tests](https://img.shields.io/badge/Tests-22%2F22%20Passing-success.svg)](tests/)
[![Privacy](https://img.shields.io/badge/Privacy-100%25%20On--Device-brightgreen.svg)](#privacy-guarantee)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

**TabTime** is an open-source, client-side browser extension designed for Google Chrome, Microsoft Edge, Brave, and other Chromium browsers (with Firefox support). It provides automated time tracking, semantic activity categorization, transparent mathematical productivity scoring, interactive Chart.js visual analytics, and a non-coercive Focus Mode using `declarativeNetRequest`.

Under a strict **Privacy-by-Design** architecture, **100% of telemetry, timestamps, domain visits, and user configurations remain strictly on your local machine** inside browser `IndexedDB` and `chrome.storage.local`. No accounts, no cloud servers, and zero remote tracking.

---

## Table of Contents

- [Quick Start: Run on Any Laptop in 2 Minutes](#quick-start-run-on-any-laptop-in-2-minutes)
- [How to Run on a Different Laptop (Detailed Guide)](#how-to-run-on-a-different-laptop-detailed-guide)
  - [Prerequisites](#prerequisites)
  - [Step 1: Clone or Download the Repository](#step-1-clone-or-download-the-repository)
  - [Step 2: Load the Unpacked Extension in Your Browser](#step-2-load-the-unpacked-extension-in-your-browser)
  - [Step 3: Enable Tracking & Grant Local Consent](#step-3-enable-tracking--grant-local-consent)
  - [Step 4: Explore Features (Popup, Dashboard, Focus Mode)](#step-4-explore-features)
- [Running Automated Tests & Code Verification](#running-automated-tests--code-verification)
- [Viva Presentation & Academic Deliverables](#viva-presentation--academic-deliverables)
- [Repository Structure](#repository-structure)
- [Privacy Guarantee & Technical Architecture](#privacy-guarantee--technical-architecture)
- [Troubleshooting & FAQs](#troubleshooting--faqs)

---

## Quick Start: Run on Any Laptop in 2 Minutes

1. **Clone the repo**:
   ```bash
   git clone https://github.com/teamcore38-droid/Tabtime-browser-extentions.git
   cd Tabtime-browser-extentions
   ```
2. Open your browser at `chrome://extensions` (or `edge://extensions` on Microsoft Edge).
3. Toggle on **Developer mode** (top-right corner).
4. Click **Load unpacked** and select the folder:
   ```
   tabtime-extension
   ```
5. Click the TabTime extension icon in your browser toolbar and click **Enable tracking**.

That's it! TabTime is now running locally on your laptop.

---

## How to Run on a Different Laptop (Detailed Guide)

### Prerequisites

| Component | Minimum Version | Purpose |
| :--- | :--- | :--- |
| **Web Browser** | Chrome 110+, Edge 110+, Brave, or Opera | Running the Manifest V3 Extension |
| **Node.js** *(Optional)* | Node.js 20 LTS or higher | Running unit tests and syntax checks |
| **Git** *(Optional)* | Any modern version | Cloning and syncing the codebase |
| **Microsoft PowerPoint** *(Optional)* | Office 2016+, Office 365, or LibreOffice | Viewing the academic viva presentations |

> [!NOTE]
> Node.js and Python are **NOT required** just to run the browser extension. The extension is 100% self-contained with bundled vanilla ES2022 JavaScript, HTML, CSS, and an offline Chart.js build.

---

### Step 1: Clone or Download the Repository

#### Option A: Using Git (Recommended)
Open Terminal (macOS/Linux) or PowerShell/Command Prompt (Windows):
```bash
git clone https://github.com/teamcore38-droid/Tabtime-browser-extentions.git
cd Tabtime-browser-extentions
```

#### Option B: Download ZIP
1. Visit [https://github.com/teamcore38-droid/Tabtime-browser-extentions](https://github.com/teamcore38-droid/Tabtime-browser-extentions).
2. Click **Code** -> **Download ZIP**.
3. Extract the ZIP file to any directory on your laptop (e.g. `C:\Projects\TabTime` or `~/Projects/TabTime`).

---

### Step 2: Load the Unpacked Extension in Your Browser

#### For Google Chrome / Brave / Chromium:
1. Open Google Chrome.
2. In the URL address bar, navigate to:
   ```text
   chrome://extensions
   ```
3. Look at the top-right corner of the page and turn **ON** the **Developer mode** toggle switch.
4. Click the **Load unpacked** button that appears on the top-left toolbar.
5. In the file dialog, navigate into this project folder and select the directory named:
   ```text
   tabtime-extension
   ```
   *(Select the folder itself and click "Select Folder")*.
6. You will see **Tab Time** appear in your extension list with version `1.0.0` (Manifest V3).

#### For Microsoft Edge:
1. Open Microsoft Edge.
2. In the URL address bar, navigate to:
   ```text
   edge://extensions
   ```
3. In the left sidebar (or bottom-left toggle), turn **ON** **Developer mode**.
4. Click **Load unpacked**.
5. Select the `tabtime-extension` directory.

---

### Step 3: Enable Tracking & Grant Local Consent

1. Click the **Extensions puzzle icon** (`🧩`) in your browser toolbar.
2. Find **Tab Time** and click the **Pin** icon so it stays visible on your toolbar.
3. Click the **Tab Time** icon.
4. The first time you open it, a transparent local privacy notice is displayed informing you that:
   - Only domain hostnames and active durations are tracked.
   - Zero URL paths, query parameters, passwords, or page contents are recorded.
   - All data stays strictly on your local disk.
5. Click **Enable tracking**.
6. The extension is now actively recording your browsing habits in real-time!

---

### Step 4: Explore Features

#### 1. Toolbar Popup (`popup.html`)
- Click the TabTime toolbar icon anytime to see:
  - **Today's Active Browsing Time** (HH:MM:SS)
  - **Real-Time Productivity Score** (0 to 100%)
  - **Category Breakdown** (Productive, Neutral, Unproductive)
  - **Top Visited Domains** for the day
  - Quick action buttons to pause/resume tracking or start Focus Mode.

#### 2. Full Analytics Dashboard (`dashboard.html`)
- Click the **"Dashboard"** button in the popup, or open a new browser tab and navigate to:
  ```text
  chrome-extension://<EXTENSION_ID>/dashboard.html
  ```
- Features:
  - Interactive Chart.js donut charts and weekly time allocation bar charts.
  - Detailed daily session history with exact millisecond timestamps.
  - Domain-by-domain drilldown and productivity trend tracking over 7-day and 30-day windows.
  - Zero external web assets loaded; Chart.js is bundled locally at `tabtime-extension/libs/chart.umd.js`.

#### 3. Custom Settings & Rules (`settings.html`)
- Customize which domains are classified as **Productive**, **Neutral**, or **Unproductive**.
- Add custom domains to your personal **Focus Blocklist**.
- Export your local data as JSON or perform a clean reset anytime.

#### 4. Distraction-Free Focus Mode (`blocked.html`)
- Activate Focus Mode from the popup or dashboard.
- When Focus Mode is active, any attempt to visit a blocklisted domain (e.g. social media or entertainment) is automatically redirected locally via `declarativeNetRequest` to the peaceful reminder page:
  ```text
  chrome-extension://<EXTENSION_ID>/blocked.html?blocked=<domain>
  ```

---

## Running Automated Tests & Code Verification

If you have **Node.js (>= 20)** installed on your laptop, you can run the comprehensive test suite and validation scripts from the project root:

```bash
# 1. Run the deterministic unit test suite (22 tests)
npm test

# 2. Run extension manifest, syntax, local resource, and network-leak verification
npm run check
```

### What the Tests Verify:
- `tests/tracking.test.js`: Validates hostname extraction, path/query stripping, category matching, midnight date boundary rollover, 60s idle cutoff debouncing, window focus/blur transitions, service worker recreation state hydration, and FIFO storage transactions.
- `scripts/check-extension.mjs`: Validates Manifest V3 compliance, JavaScript syntax across all files, verifies that all script/style paths exist locally, and scans code to confirm zero remote `fetch()`, `XMLHttpRequest()`, or WebSocket calls exist.

---

## Viva Presentation & Academic Deliverables

This repository includes the complete academic deliverables, reports, and animated PowerPoint presentations created for the **York St John University** Individual Research Project (IRP):

| File Path | Description |
| :--- | :--- |
| [`TabTime_IRP_Viva_Presentation_Final.pptx`](TabTime_IRP_Viva_Presentation_Final.pptx) | **Complete 20-slide Viva Voce presentation** with smooth fade slide transitions and native entrance animations for viva examination defense. |
| [`TabTime_Presentation_Final_stylized_animated.pptx`](TabTime_Presentation_Final_stylized_animated.pptx) | High-polish stylized animated presentation deck with visual cards and metric badges. |
| [`presentation_slides_preview/`](presentation_slides_preview/) | High-resolution 1920x1080 PNG image exports of every presentation slide for instant preview without PowerPoint. |
| [`documents/reports/TabTime_Final_Comprehensive_Report.docx`](documents/reports/TabTime_Final_Comprehensive_Report.docx) | Full dissertation report (~12,500 words) with complete literature review, methodology, results, and evaluation. |
| [`scripts/generate_viva_presentation.py`](scripts/generate_viva_presentation.py) | Python automation script to regenerate the animated presentation from the official university template. |

### To Re-generate the Presentation on Windows (Optional):
```bash
pip install python-pptx pillow pywin32
python scripts/generate_viva_presentation.py
```

---

## Repository Structure

```text
Tabtime-browser-extentions/
├── tabtime-extension/               # Complete unpacked browser extension
│   ├── manifest.json                # Manifest V3 configuration & permissions
│   ├── background.js                # Service worker entry point
│   ├── browser-runtime.js           # Browser event listeners, consent & focus
│   ├── tracking-core.js             # Pure tracking logic, categorization & scoring
│   ├── storage.js                   # Client-side IndexedDB persistence layer
│   ├── popup.html / .css / .js      # Toolbar popup UI
│   ├── dashboard.html / .css / .js  # Full analytics dashboard
│   ├── settings.html / .css / .js   # Rule customization & blocklist settings
│   ├── blocked.html / .css / .js    # Non-coercive focus redirect screen
│   ├── libs/chart.umd.js            # Bundled offline Chart.js library
│   └── icons/                       # High-res extension icons (16, 32, 48, 128px)
├── documents/
│   ├── reports/                     # Comprehensive Word dissertation reports
│   ├── research/                    # Original IRP research documentation
│   └── development/                 # Staged development plan & specifications
├── images/
│   ├── diagrams/                    # Architecture, data flow & testing diagrams
│   ├── charts/                      # SUS usability breakdown & empirical charts
│   ├── screenshots/                 # Extension UI & code implementation snapshots
│   └── ysj_logo.png                 # York St John University logo
├── data/
│   └── survey-responses/            # Cleaned empirical study workbooks (n=65)
├── tests/                           # 22-item automated test suite
├── scripts/                         # Verification & presentation generation scripts
├── presentation_slides_preview/     # 1920x1080 slide preview images
├── TabTime_IRP_Viva_Presentation_Final.pptx # Master animated viva presentation
├── package.json                     # Test scripts and Node.js project definition
├── .gitignore                       # Git exclusion rules
└── README.md                        # Master project and setup guide (This file)
```

---

## Privacy Guarantee & Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       Browser Runtime                       │
│  (Active Tab / Window Focus / Idle Listener / Redirects)    │
└──────────────────────────────┬──────────────────────────────┘
                               │ Local Event Triggers
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    Manifest V3 Engine                       │
│  • Domain Normalization: Strips paths & query strings       │
│  • Idle Debounce: Pauses after 60s of user inactivity       │
│  • Productivity Score: S = (T_prod - T_unprod) / T_total    │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                  Local Persistence Layer                    │
│    IndexedDB (Sessions & History) + chrome.storage.local    │
│    ★ ZERO Outbound Requests | 100% On-Device Isolation      │
└─────────────────────────────────────────────────────────────┘
```

- **Data Minimization (GDPR Art. 5)**: Never records URL query strings, search parameters, tokens, page contents, keystrokes, form inputs, or Incognito/Private browsing windows.
- **Data Protection by Design & Default (GDPR Art. 25)**: Absolutely no telemetry is transmitted over the internet. There is no remote backend, analytics tracking, or advertising pixel.
- **Resilient MV3 Lifecycle**: Employs checkpoint state hydration via `chrome.storage.local` to safely restore timer states when Chrome temporarily suspends the service worker.

---

## Troubleshooting & FAQs

### Q1: The extension says "Tracking Paused" or doesn't record time.
- **Fix**: Click the TabTime extension icon in the toolbar. Check if the button says **"Enable tracking"**. If so, click it to grant local consent. Also ensure you are browsing standard `http://` or `https://` websites (browsers restrict extensions from tracking internal `chrome://` or `about:` pages).

### Q2: How do I update the extension after making code changes?
- **Fix**: Go to `chrome://extensions`, locate **Tab Time**, and click the circular **Reload** (`🔄`) icon. If you edited `background.js` or `manifest.json`, reloading is required for the service worker to restart.

### Q3: Can I run this in Firefox?
- **Fix**: Yes. Open `about:debugging#/runtime/this-firefox`, click **Load Temporary Add-on...**, and select `tabtime-extension/manifest.json`.

### Q4: How do I export my data or transfer it to another laptop?
- **Fix**: Open the TabTime Settings page (`settings.html`) and click **Export Data as JSON**. You can copy this file to your new laptop or inspect your browsing history in any text editor.

---

## Author & Academic Information

- **Institution**: York St John University (London Campus)
- **School**: School of Science, Technology & Health
- **Module**: LDC6005M Individual Research Project
- **Degree**: BSc (Hons) Computer Science
- **Repository**: [https://github.com/teamcore38-droid/Tabtime-browser-extentions.git](https://github.com/teamcore38-droid/Tabtime-browser-extentions.git)
