# TAB TIME: A Privacy-Preserving Browser Extension for Real-Time Time Awareness, Visual Productivity Analytics, and Focus Management

**Institution:** York St John University (London Campus)  
**School:** School of Science, Technology & Health  
**Module:** LDC6005M Individual Research Project  
**Assessment:** Component 2 – Final Comprehensive Dissertation & Research Project Report  
**Target Platform:** Google Chrome & Mozilla Firefox (Manifest V3 Architecture)  
**Academic Year:** 2025/2026 | **Submission Date:** June 2026  

---

## **Project Declarations & Compliance Confirmation**

| Declaration Item | Status / Confirmation |
| :--- | :--- |
| **Academic Misconduct Statement Read & Understood** | Confirmed ✔ |
| **Generative AI Usage Declaration & Policy Compliance** | Confirmed ✔ |
| **Meeting All Prescribed Module Learning Outcomes** | Met ✔ (Verified Against Assessment Brief) |
| **Ethical Clearance & GDPR Data Protection Compliance** | Approved ✔ (Fully Local Client-Side Execution) |

---

## **Acronyms & Abbreviations**

| Acronym / Abbreviation | Full Expanded Definition | Contextual Domain |
| :--- | :--- | :--- |
| **API** | Application Programming Interface | Software Engineering |
| **BCS** | British Computer Society | Professional & Ethical Standards |
| **CSP** | Content Security Policy | Web Application Security |
| **DOM** | Document Object Model | Web Browser Architecture |
| **DSR** | Design Science Research | Information Systems Methodology |
| **FIFO** | First-In, First-Out (Queue Processing) | Asynchronous Concurrency |
| **FQDN** | Fully Qualified Domain Name | Networking & Domain Normalization |
| **GDPR** | General Data Protection Regulation (EU 2016/679) | Legal & Privacy Compliance |
| **HCI** | Human-Computer Interaction | Academic Discipline |
| **IDB** | IndexedDB (Indexed Database API) | Client-Side Persistent Storage |
| **JSON** | JavaScript Object Notation | Data Serialization & Export |
| **MV2** | Manifest Version 2 (Legacy WebExtensions Specification) | Browser Extension Architecture |
| **MV3** | Manifest Version 3 (Modern WebExtensions Specification) | Browser Extension Architecture |
| **NLP** | Natural Language Processing | Machine Learning & Future Roadmap |
| **RAM** | Random Access Memory | System Resource Consumption |
| **SUS** | System Usability Scale (Brooke, 1996) | Psychometric Usability Evaluation |
| **UAT** | User Acceptance Testing | Empirical Evaluation & User Studies |
| **UI / UX** | User Interface / User Experience | Frontend Design System |
| **W3C** | World Wide Web Consortium | Web Standards & Specifications |
| **WBS** | Work Breakdown Structure | Project Management & Milestones |

---

## **Abstract & Executive Summary**

Modern digital knowledge work and academic study are overwhelmingly conducted within web browser environments. While web browsers provide seamless access to critical educational, research, and collaborative resources, their friction-free design enables single-click transitions to algorithmic entertainment and social media platforms. This phenomenon leads to continuous attention fragmentation, high cognitive switching costs, and widespread loss of temporal awareness. Commercial time-tracking utilities consistently suffer from two fundamental flaws: (1) an over-reliance on centralized cloud data harvesting that creates grave privacy and surveillance vulnerabilities; and (2) a functional dichotomy offering passive logging without intervention, or enforcing rigid blocking without behavioral reflection.

This project presents Tab Time, an open, privacy-preserving, client-side browser extension engineered under the modern Manifest V3 specification for Google Chrome and Mozilla Firefox. Tab Time unifies millisecond-accurate automated tracking, rule-based semantic categorization, mathematical productivity scoring, interactive Chart.js visual analytics, and a configurable, non-coercive Focus Mode powered by dynamic network redirection (declarativeNetRequest). Crucially, Tab Time operates under a strict Privacy-by-Design paradigm: 100% of telemetry, domain logs, and user preferences are stored and processed locally within the browser's native IndexedDB and chrome.storage.local facilities, completely eliminating external server dependencies.

The system was evaluated through an empirical strategy combining automated stopwatch accuracy benchmarking, extended system stress testing, and a human-centered User Acceptance Testing study (n = 65 participants) instrumented via Google Forms. Tab Time achieved a mean System Usability Scale (SUS) score of 89.04 / 100 (Grade A: Top 10% usability tier), tracking accuracy within ±1.8 seconds of ground truth, an ultra-low memory footprint of 14–22 MB, and statistically significant self-reported improvements in digital habit awareness (95.4%) and distraction reduction (93.8%). This report details the theoretical foundation, system requirements, methodology, code implementation, empirical results, and future roadmap.

> **Key Research Finding:** A fully local, client-side browser extension combining real-time visual feedback with configurable declarative blocking successfully enhances user time awareness (95.4%) and reduces digital interruptions (93.8%) without compromising personal data privacy.

---

## **Contents Page**

- [Acronyms & Abbreviations](#acronyms--abbreviations)
- [Abstract & Executive Summary](#abstract--executive-summary)
- [Contents Page](#contents-page)
- [List of Tables](#list-of-tables)
- [List of Figures](#list-of-figures)
- [Chapter 1: Introduction & Contextual Framework](#chapter-1-introduction-and-contextual-framework)
  - [1.1 Background to the Study & Digital Wellbeing Landscape](#11-background-to-the-study--digital-wellbeing-landscape)
  - [1.2 Problem Statement & Motives for Research](#12-problem-statement--motives-for-research)
  - [1.3 Project Aim and Core Objectives](#13-project-aim-and-core-objectives)
  - [1.4 Central Research Question and Hypotheses](#14-central-research-question-and-hypotheses)
  - [1.5 Scope, Boundaries, and Constraints](#15-scope-boundaries-and-constraints)
  - [1.6 Definition of Key Technical & HCI Terms](#16-definition-of-key-technical--hci-terms)
  - [1.7 Report Structure & Organization](#17-report-structure--organization)
- [Chapter 2: Literature Review](#chapter-2-literature-review)
  - [2.1 Attention Fragmentation and Cognitive Interruption Costs](#21-attention-fragmentation-and-cognitive-interruption-costs)
  - [2.2 WebExtensions Architecture: Manifest V2 vs Manifest V3](#22-webextensions-architecture-manifest-v2-vs-manifest-v3)
  - [2.3 Automated Time Tracking & Activity Monitoring Techniques](#23-automated-time-tracking--activity-monitoring-techniques)
  - [2.4 Focus Management, Distraction Blocking & Behavioral Nudges](#24-focus-management-distraction-blocking--behavioral-nudges)
  - [2.5 Productivity Analytics & Information Visualization](#25-productivity-analytics--information-visualization)
  - [2.6 Privacy, Data Minimization & Surveillance Capitalism](#26-privacy-data-minimization--surveillance-capitalism)
  - [2.7 Comparative Analysis Matrix of Existing Solutions](#27-comparative-analysis-matrix-of-existing-solutions)
  - [2.8 Identified Research Gap and Project Justification](#28-identified-research-gap-and-project-justification)
- [Chapter 3: Project Specification / Requirements](#chapter-3-project-specification--requirements)
  - [3.1 Functional Requirements Specification (FR-01 to FR-09)](#31-functional-requirements-specification)
  - [3.2 Non-Functional Requirements & Performance Specification](#32-non-functional-requirements--performance-specification)
  - [3.3 Target Platform Support](#33-target-platform-support)
  - [3.4 System Performance Criteria & Resource Benchmarks](#34-system-performance-criteria--resource-benchmarks)
  - [3.5 Use Case Specifications and Interaction Flows](#35-use-case-specifications-and-interaction-flows)
- [Chapter 4: Methodology](#chapter-4-methodology)
  - [4.1 Design Science Research (DSR) Framework & Process Model](#41-design-science-research-dsr-framework--process-model)
  - [4.2 Data Collection Methods & Analysis Strategy (n = 65 Survey)](#42-data-collection-methods--analysis-strategy-n--65-survey)
  - [4.3 Multi-Tier Testing & Implementation Verification Strategy](#43-multi-tier-testing--implementation-verification-strategy)
  - [4.4 Project Risk Assessment & Mitigation Matrix](#44-project-risk-assessment--mitigation-matrix)
  - [4.5 Professional, Legal, and Ethical Issues (GDPR & BCS Compliance)](#45-professional-legal-and-ethical-issues-gdpr--bcs-compliance)
- [Chapter 5: Design & Implementation](#chapter-5-design--implementation)
  - [5.1 Three-Layer Architectural Design](#51-three-layer-architectural-design)
  - [5.2 Mathematical Formulations & Tracking Algorithms](#52-mathematical-formulations--tracking-algorithms)
  - [5.3 Concrete Module Implementation & Source Code Analysis](#53-concrete-module-implementation--source-code-analysis)
  - [5.4 Technical Challenges Encountered & Problem Resolutions](#54-technical-challenges-encountered--problem-resolutions)
- [Chapter 6: Results & Evaluation](#chapter-6-results--evaluation)
  - [6.1 Evidence: Google Forms Empirical Survey Results (n = 65)](#61-evidence-google-forms-empirical-survey-results-n--65)
  - [6.2 System Telemetry & Automated Testing Results](#62-system-telemetry--automated-testing-results)
  - [6.3 Achievement of Project Objectives Matrix](#63-achievement-of-project-objectives-matrix)
  - [6.4 Critical Discussion & Verification of Hypotheses](#64-critical-discussion--verification-of-hypotheses)
- [Chapter 7: Conclusions & Evaluation of Process and Products](#chapter-7-conclusions--evaluation-of-process-and-products)
  - [7.1 Evaluation of Developed Products (Artefact & Documentation)](#71-evaluation-of-developed-products-artefact--documentation)
  - [7.2 Evaluation of the Research & Development Process](#72-evaluation-of-the-research--development-process)
  - [7.3 Concluding Resolution of the Central Research Question](#73-concluding-resolution-of-the-central-research-question)
  - [7.4 Theoretical HCI & Practical Industrial Significance](#74-theoretical-hci--practical-industrial-significance)
  - [7.5 Personal Reflection & Professional Development](#75-personal-reflection--professional-development)
- [Chapter 8: Recommendations for Further Work](#chapter-8-recommendations-for-further-work)
- [References List](#references-list)
- [Bibliography List](#bibliography-list)
- [Appendices](#appendices)

---

## **List of Tables**

- [Table 0.1: Project Declarations and Compliance Confirmation](#project-declarations--compliance-confirmation)
- [Table 0.2: Comprehensive Table of Acronyms and Technical Abbreviations](#acronyms--abbreviations)
- [Table 2.1: Comparative Feature Matrix of Existing Productivity Solutions](#27-comparative-analysis-matrix-of-existing-solutions)
- [Table 3.1: System Requirements Specification Matrix (Functional & Non-Functional)](#32-non-functional-requirements--performance-specification)
- [Table 4.1: Project Risk Assessment and Proactive Mitigation Matrix](#44-project-risk-assessment--mitigation-matrix)
- [Table 6.1: Standardized System Usability Scale (SUS) Item-by-Item Breakdown (n = 65)](#612-standardized-system-usability-scale-sus-results-composite-score--8904--100)
- [Table 6.2: Ground-Truth Stopwatch Tracking Accuracy Validation Benchmark](#621-ground-truth-stopwatch-accuracy-validation)
- [Table 6.3: Formal Project Objectives Achievement Verification Matrix](#63-achievement-of-project-objectives-matrix)
- [Table B.1: Google Forms Evaluation Survey Question Inventory](#appendix-b-google-forms-user-evaluation-survey-instrument--questionnaire-screenshots)
- [Table C.1: Complete System Test Case Execution Matrix (TC-01 to TC-12)](#appendix-c-complete-system-test-case-execution-matrix)
- [Table E.1: Project Timeline, Milestones, and Work Breakdown Structure](#appendix-e-project-timeline-milestones-and-work-breakdown-structure)

---

## **List of Figures**

- [Figure 1.1: Conceptual Overview of Tab Time: Mindful Digital Engagement Pipeline](#11-background-to-the-study--digital-wellbeing-landscape)
- [Figure 1.2: Project Main Aim and Core Research Objectives Framework](#13-project-aim-and-core-objectives)
- [Figure 3.1: Hierarchical Functional and System Requirements Decomposition](#31-functional-requirements-specification)
- [Figure 5.1: Three-Layer System Architecture: Presentation, Logic Engine, and Local Storage](#51-three-layer-architectural-design)
- [Figure 5.2: End-to-End Data Flow and Real-Time Event Processing Pipeline](#52-mathematical-formulations--tracking-algorithms)
- [Figure 5.3: Analytics Data Transformation and Rollup Pipeline](#52-mathematical-formulations--tracking-algorithms)
- [Figure 5.4: Code Implementation: Manifest V3 Specification in manifest.json](#531-manifest-v3-configuration--security-architecture-manifestjson)
- [Figure 5.5: Code Implementation: Real-Time Tab Lifecycle Event Listeners in background.js](#532-tab-lifecycle-event-listeners--idle-debouncing-backgroundjs)
- [Figure 5.6: Code Implementation: DeclarativeNetRequest Focus Engine in background.js](#533-declarativenetrequest-dynamic-rules--focus-engine-backgroundjs)
- [Figure 5.7: Code Implementation: Client-Side IndexedDB Storage Layer in storage.js](#534-client-side-indexeddb-storage-schema--data-layer-storagejs)
- [Figure 5.8: Code Implementation: Mathematical Productivity Scoring in popup.js](#535-ui-component-engineering--productivity-scoring-popupjs)
- [Figure 6.1: Google Forms Evaluation: Participant Demographic and Browser Usage Profile (n = 65)](#611-participant-demographics--usage-profiles)
- [Figure 6.2: System Usability Scale (SUS) 10-Item Evaluation Breakdown (n = 65)](#612-standardized-system-usability-scale-sus-results-composite-score--8904--100)
- [Figure 6.3: Feature Utility & Satisfaction Ratings from Google Forms Evaluation (n = 65)](#613-feature-specific-utility--performance-ratings)
- [Figure 6.4: Self-Reported Behavioral Impact on Time Awareness and Distraction Reduction (n = 65)](#614-self-reported-behavioral-changes--distraction-reduction)
- [Figure 6.5a: Google Forms Live Evaluation Responses Spreadsheet (Part 1 - Profiles & SUS)](#616-live-responses-spreadsheet-evidence)
- [Figure 6.5b: Google Forms Live Evaluation Responses Spreadsheet (Part 2 - Ratings & Feedback)](#616-live-responses-spreadsheet-evidence)
- [Figure 7.1: Full Interactive Analytics Dashboard Interface](#71-evaluation-of-developed-products-artefact--documentation)
- [Figure A.1: Toolbar Extension Popup UI](#appendix-a-complete-system-interface-screenshots)
- [Figure A.2: Full-Page Interactive Analytics Dashboard](#appendix-a-complete-system-interface-screenshots)
- [Figure A.3: Extension Settings Interface](#appendix-a-complete-system-interface-screenshots)
- [Figure B.1: Google Forms Evaluation Survey (Form Title & Demographics)](#appendix-b-google-forms-user-evaluation-survey-instrument--questionnaire-screenshots)
- [Figure B.2: Google Forms Evaluation Survey (SUS Items 1 to 5)](#appendix-b-google-forms-user-evaluation-survey-instrument--questionnaire-screenshots)
- [Figure B.3: Google Forms Evaluation Survey (SUS Items 6 to 10)](#appendix-b-google-forms-user-evaluation-survey-instrument--questionnaire-screenshots)
- [Figure B.4: Google Forms Evaluation Survey (Feature Utility Ratings)](#appendix-b-google-forms-user-evaluation-survey-instrument--questionnaire-screenshots)
- [Figure B.5: Google Forms Evaluation Survey (Behavioral Impact & Qualitative Feedback)](#appendix-b-google-forms-user-evaluation-survey-instrument--questionnaire-screenshots)

---

*(The full detailed content of Chapters 1 to 8, References List, Bibliography List, and Appendices A to F follows in exact alignment with the Master Word report).*
