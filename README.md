# Anomaly Thought Partner Skill

An intelligent, interactive, and generic **"Anomaly Thought Partner" Skill** designed for Gemini Enterprise and skill-compliant conversational AI environments.

This skill assists software engineers, QA specialists, and technical leads in logging, triaging, and diagnosing software bugs and system anomalies. It utilizes a progressive **"Crawl, Walk, Run"** workflow to minimize developer friction while ensuring complete, high-quality, reproducible defect reports with quantitative risk evaluation and root-cause classification.

![Anomaly Thought Partner in Action](assets/skill_in_action.jpg)

---

## Key Features

* **Progressive 3-Phase Architecture**:
  * **Phase 1: Core Triage (Crawl)** — 3 rapid questions capturing the minimal reproduction pathway for quick bug reporting.
  * **Phase 2: Contextual Depth (Walk)** — 5 structured questions capturing pre- and post-anomaly environmental state parameters.
  * **Phase 3: The True "Thought Partner" (Run)** — 4 elevated questions performing risk estimation ($$\text{Risk} = \text{Frequency} \times \text{Severity}$$) and retrospective root-cause categorization (Requirements vs. Verification vs. Other).
* **Strict Conversational Protocol**:
  * Enforces **strictly one question per conversational turn**.
  * Employs **Gentle Disambiguation** when receiving brief or underspecified inputs.
  * Maintains an objective, technical tone free of proprietary brand names.
* **Robust Python Helper (`scripts/anomaly_helper.py`)**:
  * Dynamic risk score calculation with 4-tier classification (Critical / High / Medium / Low).
  * Input schema validation ensuring all required phase fields are populated.
  * Automated Markdown report generation tailored to each phase.
* **Automated Test Suite**:
  * Comprehensive `unittest` test suite covering risk calculations, tier boundaries, input validation, report generation, and all 3 specification scenarios.

---

## Quick Navigation

* 💬 [**How to Use in Chat Harnesses (Non-Technical Guide & Examples)**](#using-this-skill-in-chat-agent-harnesses-gemini-enterprise-antigravity-etc)
* 📋 [**Conversational Workflow Summary**](#conversational-workflow-summary)
* 🧮 [**Risk Score Calculation Matrix**](#risk-score-calculation-matrix)
* 💻 [**Python Helper CLI Reference**](#python-helper-cli-reference)
* 🧪 [**Running Automated Tests**](#running-automated-tests)

---

## Directory Structure

```text
anomaly-thought-skill/
├── SKILL.md                          # Primary Skill instruction file with YAML frontmatter
├── README.md                         # Project documentation and developer guide
├── LICENSE                           # Apache License 2.0
├── assets/
│   └── skill_in_action.jpg           # Skill in action visual overview
├── scripts/
│   ├── __init__.py
│   ├── anomaly_helper.py             # Core Python helper library & CLI
│   └── export_reports.py             # Batch report export utility
├── tests/
│   ├── __init__.py
│   ├── test_anomaly_helper.py        # Unit tests for risk calculation, validation, & formatting
│   └── test_scenarios.py             # Scenario-specific validation tests for Phases 1, 2, and 3
├── examples/
│   ├── phase1_example.md             # Scenario 1: UI freeze during network slowdown
│   ├── phase2_example.md             # Scenario 2: Mobile crash during low battery & sync
│   ├── phase3_example.md             # Scenario 3: Hardware pairing failure & verification root cause
│   ├── mock_inputs.json              # Mock input payloads for all 3 scenarios
│   └── generated_reports/            # Pre-generated sample markdown reports
│       ├── phase1_report.md
│       ├── phase2_report.md
│       └── phase3_report.md
└── references/
    ├── phase_specifications.md       # Deep dive into phase protocols, questions, and schemas
    ├── disambiguation_guide.md       # Gentle disambiguation prompts and examples
    ├── risk_matrix.md                # Risk formula, tier thresholds, and SLA actions
    └── root_cause_taxonomies.md      # Requirements vs. Verification vs. Other failure taxonomies
```

---

## Conversational Workflow Summary

### Phase 1: Core Triage (Crawl)
1. **Manifestation**: *"What exactly does the user see or experience when this anomaly occurs?"*
2. **Triggering Event**: *"What specific action, update, or system event triggered this anomaly?"*
3. **Reproducibility**: *"Can you reliably reproduce this? If so, what are the steps?"*
* **Output**: `Core Bug Report`

### Phase 2: Contextual Depth (Walk)
1. **Discovery Method**: *"How was this discovered (e.g., manual testing, automated crash logs, user report)?"*
2. **Pre-Anomaly System State**: *"What was the system state right before the anomaly occurred? (e.g., OS version, battery level, device memory load, background syncing)?"*
3. **Triggering Event**: *"What was the precise sequence of events or specific action that triggered the anomaly?"*
4. **Post-Anomaly System State**: *"What happened immediately after the anomaly? (e.g., app crash, automatic recovery, system freeze)?"*
5. **Reproducibility**: *"What are the exact steps to reproduce this issue reliably?"*
* **Output**: `Detailed Technical Anomaly Report` (with Pre vs. Post State Table)

### Phase 3: The True "Thought Partner" (Run)
1. **The Core Issue**: *"How does this anomaly manifest, and what are the exact steps/triggers to reproduce it?"*
2. **The Environment**: *"What was the system state before the anomaly (OS, memory, sync state), and what was the state immediately after?"*
3. **Risk Estimation**: *"On a scale of 1 to 5, how would you rate the Frequency of this issue, and on a scale of 1 to 5, how would you rate its Severity? Please provide a brief rationale for both."*
4. **Retrospective & Root Cause**: *"Looking at the root cause, was this a failure of Requirements (specified wrong), Verification (built wrong), or something else? Please provide any technical root-cause details."*
* **Output**: `Comprehensive QAC Recommendation Report` (with Risk Score Matrix and CAPA recommendations)

---

## Using This Skill in Chat Agent Harnesses (Gemini Enterprise, Antigravity, etc.)

If you are using this skill in a conversational environment (such as **Gemini Enterprise App**, **Antigravity**, or any skill-enabled chat UI), **no coding or terminal commands are required**. You simply converse with the AI in natural language.

### How It Works for Non-Technical Users

1. **Start the Chat**: Type a simple sentence indicating you want to log or triage an issue (e.g., *"I need to log an anomaly"* or *"Help me report a bug"*).
2. **Choose a Phase**: The assistant will present the 3 phases. Choose the one that matches your current goal:
   * **Phase 1 (Crawl)**: When you just need to get reproduction steps logged quickly (3 questions).
   * **Phase 2 (Walk)**: When QA and developers need detailed device/system parameters (5 questions).
   * **Phase 3 (Run)**: When you need severity/frequency risk ratings and root-cause analysis (4 questions).
3. **Answer One Question at a Time**: The assistant will guide you step-by-step. If an answer is vague (e.g., *"it froze"*), the assistant will politely ask for a bit more detail before moving forward.
4. **Get Your Finished Report**: Once all questions are answered, the assistant automatically formats and prints a clean, structured Markdown report that you can copy and paste directly into your team's issue tracker or ticketing system.

---

### Step-by-Step Chat Examples & Outputs

#### Example 1: Phase 1 — Core Triage (Crawl)

**User Prompt to Start:**
> *"Help me log a bug using Phase 1."*

**Interactive Conversation:**
* **Assistant**: *"What exactly does the user see or experience when this anomaly occurs?"*
* **User**: *"The search filter dropdown freezes in place for over 15 seconds without throwing an error dialog."*
* **Assistant**: *"What specific action, update, or system event triggered this anomaly?"*
* **User**: *"Typing a search query into the live filter while network bandwidth is throttled to 50 kbps."*
* **Assistant**: *"Can you reliably reproduce this? If so, what are the steps?"*
* **User**: *"Yes, 100% reproducible. 1. Go to Catalog. 2. Set network throttle to 50 kbps. 3. Type 5 characters in search box. 4. UI freezes."*

**Final Output Generated by the Skill:**
```markdown
# Core Bug Report

| Metric | Details |
| :--- | :--- |
| **Phase** | Phase 1: Core Triage (Crawl) |
| **Status** | Ready for Triage |
| **Summary** | UI freeze during network slowdown in catalog search filter |

---

## 1. Summary
> **UI freeze during network slowdown in catalog search filter**

## 2. Manifestation
The search filter dropdown freezes in place for over 15 seconds without throwing an error dialog.

## 3. Triggering Event
Typing a search query into the live filter while network bandwidth is throttled to 50 kbps.

## 4. Steps to Reproduce
100% reproducible.
1. Go to Catalog.
2. Set network throttle to 50 kbps.
3. Type 5 characters in search box.
4. UI freezes.
```

---

#### Example 2: Phase 2 — Contextual Depth (Walk)

**User Prompt to Start:**
> *"I want to log a mobile crash using Phase 2."*

**Interactive Conversation:**
* **Assistant**: *"How was this discovered (e.g., manual testing, automated crash logs, user report)?"*
* **User**: *"Automated crash telemetry alert in the staging build."*
* **Assistant**: *"What was the system state right before the anomaly occurred? (e.g., OS version, battery level, device memory load, background syncing)?"*
* **User**: *"Low battery and syncing."*
* **Assistant** *(Gentle Disambiguation)*: *"To help engineering isolate resource limits, could you provide the approximate battery level percentage, device OS version, and whether background sync queue items were pending?"*
* **User**: *"OS version 14.2, memory usage at 88%, battery at 9% with Low-Power Mode active, and background sync worker active with 45 pending items."*
* **Assistant**: *"What was the precise sequence of events or specific action that triggered the anomaly?"*
* **User**: *"The background worker attempted to batch-deserialize an uncompressed 25MB sync payload while the OS aggressively throttled CPU under low-battery mode."*
* **Assistant**: *"What happened immediately after the anomaly? (e.g., app crash, automatic recovery, system freeze)?"*
* **User**: *"The application process abruptly terminated to the home screen, killing the background thread and leaving a 0-byte lock file."*
* **Assistant**: *"What are the exact steps to reproduce this issue reliably?"*
* **User**: *"Set device battery to 8%, queue 45 sync items, and trigger the sync worker."*

**Final Output Generated by the Skill:**
```markdown
# Detailed Technical Anomaly Report

| Attribute | Specification |
| :--- | :--- |
| **Phase** | Phase 2: Contextual Depth (Walk) |
| **Status** | Diagnostic Ready |
| **Summary** | Mobile application crash during low-battery mode and active background synchronization |
| **Discovery Method** | Automated crash telemetry alert in the staging build. |

---

## 1. Executive Summary
**Mobile application crash during low-battery mode and active background synchronization**

---

## 2. Discovery & Reproduction
* **Discovery Method**: Automated crash telemetry alert in the staging build.
* **Reproducibility**: Set device battery to 8%, queue 45 sync items, and trigger the sync worker.

---

## 3. System State Transitions

| State Boundary | System Condition / Parameter Profile |
| :--- | :--- |
| **Pre-Anomaly State** | OS version 14.2, memory usage at 88%, battery at 9% with Low-Power Mode active, and background sync worker active with 45 pending items. |
| **Triggering Event** | The background worker attempted to batch-deserialize an uncompressed 25MB sync payload while the OS aggressively throttled CPU under low-battery mode. |
| **Post-Anomaly State** | The application process abruptly terminated to the home screen, killing the background thread and leaving a 0-byte lock file. |

---

## 4. Technical Trigger Details
The background worker attempted to batch-deserialize an uncompressed 25MB sync payload while the OS aggressively throttled CPU under low-battery mode.
```

---

#### Example 3: Phase 3 — The True "Thought Partner" (Run)

**User Prompt to Start:**
> *"Let's do a Phase 3 analysis for a peripheral pairing failure."*

**Interactive Conversation:**
* **Assistant**: *"How does this anomaly manifest, and what are the exact steps/triggers to reproduce it?"*
* **User**: *"The peripheral pairing dialog fails to render on screen, leaving an infinite loading spinner when the user taps 'Pair New Peripheral' while background telemetry is streaming."*
* **Assistant**: *"What was the system state before the anomaly (OS, memory, sync state), and what was the state immediately after?"*
* **User**: *"Pre-State: OS 16.5, 1.2 GB RAM available, Bluetooth active, telemetry streaming at 100Hz. Post-State: Pairing timed out after 60s, Bluetooth stayed in 'Connecting', and UI thread watchdog logged an 8.4s freeze."*
* **Assistant**: *"On a scale of 1 to 5, how would you rate the Frequency of this issue, and on a scale of 1 to 5, how would you rate its Severity? Please provide a brief rationale for both."*
* **User**: *"Frequency: 4/5 (occurs in ~70% of initial onboarding attempts). Severity: 4/5 (completely blocks device setup for new users with no workaround)."*
* **Assistant**: *"Looking at the root cause, was this a failure of Requirements (specified wrong), Verification (built wrong), or something else? Please provide any technical root-cause details."*
* **User**: *"Verification Failure (built wrong). The onboarding manager invoked the pairing UI dialog directly from a background thread instead of dispatching to the Main UI Thread."*

**Final Output Generated by the Skill:**
```markdown
# Comprehensive QAC Recommendation Report

| Assessment Metric | Value |
| :--- | :--- |
| **Phase** | Phase 3: The True "Thought Partner" (Run) |
| **Overall Risk Tier** | 🔴 **Critical** (Red) |
| **Calculated Risk Score** | **16 / 25** (Freq: 4 × Sev: 4) |
| **Root Cause Category** | **Verification Failure (Built Wrong)** |
| **Recommended Action** | Immediate escalation to on-call engineering; hotfix required. |

---

## 1. Executive Summary
**Peripheral pairing failure caused by background thread UI violation**

---

## 2. Quantitative Risk Assessment Matrix

| Dimension | Rating (1–5) | Rationale & Behavioral Evidence |
| :--- | :---: | :--- |
| **Frequency** | `4 / 5` | Occurs in ~70% of initial onboarding attempts. |
| **Severity** | `4 / 5` | Completely blocks device setup for new users with no workaround. |
| **Risk Score** | `16 / 25` | **Critical Tier (Red)** — *Score = Frequency (4) × Severity (4)* |

> **Quality & Reliability Action Item**:
> Immediate escalation to on-call engineering; hotfix required.

---

## 3. Core Issue & Reproduction Pathway
### 3.1 Manifestation & Triggers
The peripheral pairing dialog fails to render on screen, leaving an infinite loading spinner when the user taps 'Pair New Peripheral' while background telemetry is streaming.

---

## 4. Environmental & System State Context
Pre-State: OS 16.5, 1.2 GB RAM available, Bluetooth active, telemetry streaming at 100Hz.
Post-State: Pairing timed out after 60s, Bluetooth stayed in 'Connecting', and UI thread watchdog logged an 8.4s freeze.

---

## 5. Retrospective Root-Cause Categorization

| Dimension | Classification & Engineering Analysis |
| :--- | :--- |
| **Taxonomy Category** | **Verification Failure (Built Wrong)** |
| **Technical Root Cause** | The onboarding manager invoked the pairing UI dialog directly from a background thread instead of dispatching to the Main UI Thread. |

---

## 6. Corrective & Preventive Actions (CAPA)
1. **Immediate Remediation**: Address direct defect in implementation aligning with verified state constraints.
2. **Defect Prevention**: Implement automated regression test coverage specifically verifying the boundary condition.
3. **Process Improvement**: Update architectural/interface verification checklists for this failure class.
```

---

## Risk Score Calculation Matrix

$$\text{Risk Score} = \text{Frequency} \times \text{Severity} \quad (\text{Frequency}, \text{Severity} \in [1, 5])$$

| Risk Score | Tier Name | Badge / Color | Engineering SLA & Recommendation |
| :---: | :--- | :---: | :--- |
| **16 – 25** | **Critical** | 🔴 Red | **Immediate Escalation**: Page on-call engineering; hotfix required. |
| **10 – 15** | **High** | 🟠 Orange | **Current Sprint Priority**: Assign to lead engineer; resolve within 24–48 hours. |
| **5 – 9** | **Medium** | 🟡 Yellow | **Standard Triage**: Schedule for standard defect backlog in upcoming release. |
| **1 – 4** | **Low** | 🟢 Green | **Routine Backlog**: Address during maintenance cycles or polish sprints. |

---

## Python Helper CLI Reference

### 1. Calculate Risk Score
```bash
python scripts/anomaly_helper.py --calculate-risk 4 4
```
**Output:**
```json
{
  "frequency": 4,
  "severity": 4,
  "score": 16,
  "tier_name": "Critical",
  "color": "Red",
  "badge": "🔴",
  "recommendation": "Immediate escalation to on-call engineering; hotfix required."
}
```

### 2. Run Built-In Demonstration Scenarios
```bash
# Phase 1: Simple UI Freeze during network slowdown
python scripts/anomaly_helper.py --demo 1

# Phase 2: Mobile crash during low-battery & background sync
python scripts/anomaly_helper.py --demo 2

# Phase 3: Hardware pairing thread violation & verification root cause
python scripts/anomaly_helper.py --demo 3
```

### 3. Generate Report from JSON Payload
```bash
python scripts/anomaly_helper.py --phase 3 --file examples/mock_inputs.json --output report.md
```

---

## Running Automated Tests

Run the full automated test suite using Python's built-in `unittest`:

```bash
python3 -m unittest discover -s tests -v
```

All 25 unit and scenario test cases will execute and validate:
* Risk tier boundary conditions (Critical, High, Medium, Low).
* Validation error reporting for missing/empty fields.
* Phase normalization and dispatching.
* Format generation for all 3 report types.
* Realistic mock scenarios matching all technical specifications.

---

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.

