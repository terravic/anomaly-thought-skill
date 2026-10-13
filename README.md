# Anomaly Thought Partner Skill

A structured conversational skill for logging, triaging, and diagnosing software bugs and system anomalies.

This skill assists non-technical reporters, QA specialists, and software engineers in documenting software issues and unexpected system behaviors. It uses a three-phase **"Crawl, Walk, Run"** workflow to collect reproducible defect reports, environmental state transitions, quantitative risk scores, and root-cause classifications.

![Anomaly Thought Partner in Action](assets/skill_in_action.jpg)

---

## Key Features

* **Progressive 3-Phase Architecture**:
  * **Phase 1: Core Triage (Crawl)** - 3 sequential questions capturing the minimal reproduction pathway for quick issue reporting.
  * **Phase 2: Contextual Depth (Walk)** - 5 sequential questions capturing pre- and post-anomaly environmental state parameters.
  * **Phase 3: Thought Partner (Run)** - 4 sequential questions performing risk estimation ($$\text{Risk} = \text{Frequency} \times \text{Severity}$$) and retrospective root-cause categorization (Requirements vs. Verification vs. Other).
* **Conversational Interaction Protocol**:
  * Asks one question per conversational turn.
  * Applies **Gentle Disambiguation** when receiving brief or incomplete inputs.
  * Validates required phase parameters before generating the structured report.
* **Python Helper Module ([`scripts/anomaly_helper.py`](scripts/anomaly_helper.py))**:
  * Dynamic risk score calculation with 4-tier classification (Critical / High / Medium / Low).
  * Input schema validation ensuring all required phase fields are populated.
  * Automated Markdown report generation for each phase.
* **Automated Test Suite**:
  * Unit and scenario test suite covering risk score calculations, tier boundaries, input validation, and report generation across all three phases.

---

## Quick Navigation

* [Non-Technical User Guide](#non-technical-user-guide)
* [Directory Structure](#directory-structure)
* [Conversational Workflow Summary](#conversational-workflow-summary)
* [Technical Walkthrough Examples](#technical-walkthrough-examples)
* [Risk Score Calculation Matrix](#risk-score-calculation-matrix)
* [Python Helper CLI Reference](#python-helper-cli-reference)
* [Running Automated Tests](#running-automated-tests)

---

## Non-Technical User Guide

You do not need programming knowledge or command-line experience to use this skill in a chat interface. You interact with the assistant in plain language, and it guides you step by step to build a complete issue report.

### How to Use the Skill

1. **Start the Conversation**: Tell the assistant that you want to report a problem (for example, *"I need to report a website bug"* or *"Help me document an app issue"*).
2. **Select a Phase**: The assistant will ask which of the three phases you want to use:
   * **Phase 1 (Crawl)**: Choose this when you want to report a problem quickly in 3 simple questions (what happened, what caused it, and how to repeat it).
   * **Phase 2 (Walk)**: Choose this when you want to include extra details about the device or situation before and after the problem happened (5 questions).
   * **Phase 3 (Run)**: Choose this when you are reviewing a problem with your team to rate how often it happens, how badly it affects users, and why it occurred (4 questions).
3. **Answer One Question at a Time**: The assistant asks only one question at a time. If your answer is brief (for example, *"the page stopped working"*), the assistant will ask a simple follow-up question to help clarify what you saw on screen.
4. **Copy Your Finished Report**: After you answer the questions, the assistant generates a formatted summary report that you can copy and paste into an email, support ticket, or project tracker.

### Real-World Examples for Non-Technical Users

#### Real-World Example 1: Online Store Checkout Button Not Working (Phase 1 - Quick Report)

**Scenario**: A customer support specialist notices that customers cannot finish checking out when they apply a seasonal discount code.

* **User**: *"Help me report a checkout problem using Phase 1."*
* **Assistant**: *"What exactly does the user see or experience when this anomaly occurs?"*
* **User**: *"The 'Place Order' button turns gray and nothing happens when you click it. No error message appears on the page."*
* **Assistant**: *"What specific action, update, or system event triggered this anomaly?"*
* **User**: *"Entering the promo code SAVE20 in the discount box on the checkout page and clicking Apply."*
* **Assistant**: *"Can you reliably reproduce this? If so, what are the steps?"*
* **User**: *"Yes, it happens every time. 1. Add any item to the shopping cart. 2. Go to the checkout page. 3. Enter SAVE20 in the promo code box and click Apply. 4. Click 'Place Order' and notice the button does not respond."*

**Generated Report**:
```markdown
# Core Bug Report

| Metric | Details |
| :--- | :--- |
| **Phase** | Phase 1: Core Triage (Crawl) |
| **Status** | Ready for Triage |
| **Summary** | Checkout button stops responding after applying discount code SAVE20 |

---

## 1. Summary
> **Checkout button stops responding after applying discount code SAVE20**

## 2. Manifestation
The 'Place Order' button turns gray and nothing happens when you click it. No error message appears on the page.

## 3. Triggering Event
Entering the promo code SAVE20 in the discount box on the checkout page and clicking Apply.

## 4. Steps to Reproduce
Happens every time.
1. Add any item to the shopping cart.
2. Go to the checkout page.
3. Enter SAVE20 in the promo code box and click Apply.
4. Click 'Place Order' and notice the button does not respond.
```

---

#### Real-World Example 2: Expense App Closing When Uploading a Receipt Photo (Phase 2 - Detailed Report)

**Scenario**: An office manager is reporting an issue where the mobile expense app closes unexpectedly when employees try to attach a photo of a paper receipt while their phone battery is low.

* **User**: *"I need to log an issue with our mobile expense app using Phase 2."*
* **Assistant**: *"How was this discovered (e.g., manual testing, automated crash logs, user report)?"*
* **User**: *"Reported by three team members submitting travel expenses."*
* **Assistant**: *"What was the system state right before the anomaly occurred? (e.g., OS version, battery level, device memory load, background syncing)?"*
* **User**: *"Their phones were on low battery."*
* **Assistant** *(Gentle Disambiguation)*: *"To help narrow down the device conditions, do you know approximately what battery percentage the phones had, whether Battery Saver mode was turned on, and whether other uploads were waiting in the background?"*
* **User**: *"Phone battery was at 10% with Battery Saver turned on, and 5 previous expense drafts were still uploading in the background."*
* **Assistant**: *"What was the precise sequence of events or specific action that triggered the anomaly?"*
* **User**: *"Opening a new expense form, tapping 'Attach Receipt', and taking a high-resolution camera photo."*
* **Assistant**: *"What happened immediately after the anomaly? (e.g., app crash, automatic recovery, system freeze)?"*
* **User**: *"The app closed immediately back to the phone home screen, and when reopened, the unsaved expense draft was gone."*
* **Assistant**: *"What are the exact steps to reproduce this issue reliably?"*
* **User**: *"1. Turn on Battery Saver mode with battery around 10%. 2. Start uploading 5 expense drafts. 3. Open a new expense and take a receipt photo with the camera. 4. The app closes."*

**Generated Report**:
```markdown
# Detailed Technical Anomaly Report

| Attribute | Specification |
| :--- | :--- |
| **Phase** | Phase 2: Contextual Depth (Walk) |
| **Status** | Diagnostic Ready |
| **Summary** | Expense app closes when taking receipt photo during Battery Saver mode |
| **Discovery Method** | Reported by three team members submitting travel expenses. |

---

## 1. Executive Summary
**Expense app closes when taking receipt photo during Battery Saver mode**

---

## 2. Discovery & Reproduction
* **Discovery Method**: Reported by three team members submitting travel expenses.
* **Reproducibility**:
1. Turn on Battery Saver mode with battery around 10%.
2. Start uploading 5 expense drafts.
3. Open a new expense and take a receipt photo with the camera.
4. The app closes.

---

## 3. System State Transitions

| State Boundary | System Condition / Parameter Profile |
| :--- | :--- |
| **Pre-Anomaly State** | Phone battery was at 10% with Battery Saver turned on, and 5 previous expense drafts were still uploading in the background. |
| **Triggering Event** | Opening a new expense form, tapping 'Attach Receipt', and taking a high-resolution camera photo. |
| **Post-Anomaly State** | The app closed immediately back to the phone home screen, and when reopened, the unsaved expense draft was gone. |

---

## 4. Technical Trigger Details
Opening a new expense form, tapping 'Attach Receipt', and taking a high-resolution camera photo.
```

---

#### Real-World Example 3: Reviewing Impact of a Broken Appointment Calendar (Phase 3 - Impact & Cause Review)

**Scenario**: A clinic coordinator and product lead review an issue where patients booking appointments on the last day of the month see a blank calendar.

* **User**: *"Let's run Phase 3 for the blank appointment calendar issue."*
* **Assistant**: *"How does this anomaly manifest, and what are the exact steps/triggers to reproduce it?"*
* **User**: *"When a patient selects the 31st day of a month and clicks 'Next Available Week', the calendar grid turns completely blank instead of showing next month's time slots."*
* **Assistant**: *"What was the system state before the anomaly (OS, memory, sync state), and what was the state immediately after?"*
* **User**: *"Before: Patient is logged into the booking portal with available slots loaded for the current month. After: The calendar area is blank and the 'Confirm Appointment' button stays disabled until the page is refreshed."*
* **Assistant**: *"On a scale of 1 to 5, how would you rate the Frequency of this issue, and on a scale of 1 to 5, how would you rate its Severity? Please provide a brief rationale for both."*
* **User**: *"Frequency is 3 out of 5 because it affects anyone browsing across month-end dates. Severity is 4 out of 5 because patients cannot book appointments for the following month without refreshing and starting over."*
* **Assistant**: *"Looking at the root cause, was this a failure of Requirements (specified wrong), Verification (built wrong), or something else? Please provide any technical root-cause details."*
* **User**: *"Verification Failure (built wrong). The calendar date calculation added 7 days to the day number without rolling over into the next month, and our test cases only checked dates in the middle of the month."*

---

## Directory Structure

```text
anomaly-thought-skill/
|-- LICENSE                           # Apache License 2.0
|-- README.md                         # Project documentation and user guide
|-- SKILL.md                          # Primary Skill instruction file with YAML frontmatter
|-- prd.md                            # Product Requirements Document
|-- assets/
|   `-- skill_in_action.jpg           # Visual overview of the skill workflow
|-- examples/
|   |-- generated_reports/            # Pre-generated sample markdown reports
|   |   |-- phase1_report.md
|   |   |-- phase2_report.md
|   |   `-- phase3_report.md
|   |-- mock_inputs.json              # Mock input payloads for all 3 phases
|   |-- phase1_example.md             # Phase 1 walkthrough: UI freeze during network slowdown
|   |-- phase2_example.md             # Phase 2 walkthrough: Mobile crash during low battery & sync
|   `-- phase3_example.md             # Phase 3 walkthrough: Peripheral pairing failure & root cause
|-- references/
|   |-- disambiguation_guide.md       # Gentle disambiguation prompts and examples
|   |-- phase_specifications.md       # Phase protocols, questions, and schemas
|   |-- risk_matrix.md                # Risk formula, tier thresholds, and SLA actions
|   `-- root_cause_taxonomies.md      # Requirements vs. Verification vs. Other failure taxonomies
|-- scripts/
|   |-- __init__.py
|   |-- anomaly_helper.py             # Core Python helper library & CLI
|   `-- export_reports.py             # Batch report export utility
`-- tests/
    |-- __init__.py
    |-- test_anomaly_helper.py        # Unit tests for risk calculation, validation, & formatting
    `-- test_scenarios.py             # Scenario validation tests for Phases 1, 2, and 3
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

### Phase 3: Thought Partner (Run)
1. **The Core Issue**: *"How does this anomaly manifest, and what are the exact steps/triggers to reproduce it?"*
2. **The Environment**: *"What was the system state before the anomaly (OS, memory, sync state), and what was the state immediately after?"*
3. **Risk Estimation**: *"On a scale of 1 to 5, how would you rate the Frequency of this issue, and on a scale of 1 to 5, how would you rate its Severity? Please provide a brief rationale for both."*
4. **Retrospective & Root Cause**: *"Looking at the root cause, was this a failure of Requirements (specified wrong), Verification (built wrong), or something else? Please provide any technical root-cause details."*
* **Output**: `Comprehensive Quality Assurance Report` (with Risk Score Matrix and CAPA recommendations)

---

## Technical Walkthrough Examples

Detailed engineering transcripts and generated output reports are provided in the `examples/` directory:

* **Phase 1 Engineering Walkthrough**: [examples/phase1_example.md](examples/phase1_example.md) (Sample output: [examples/generated_reports/phase1_report.md](examples/generated_reports/phase1_report.md))
* **Phase 2 Engineering Walkthrough**: [examples/phase2_example.md](examples/phase2_example.md) (Sample output: [examples/generated_reports/phase2_report.md](examples/generated_reports/phase2_report.md))
* **Phase 3 Engineering Walkthrough**: [examples/phase3_example.md](examples/phase3_example.md) (Sample output: [examples/generated_reports/phase3_report.md](examples/generated_reports/phase3_report.md))

### Sample Phase 3 Output (`Comprehensive Quality Assurance Report`)

```markdown
# Comprehensive Quality Assurance Report

| Assessment Metric | Value |
| :--- | :--- |
| **Phase** | Phase 3: Thought Partner (Run) |
| **Overall Risk Tier** | [CRITICAL] **Critical** (Red) |
| **Calculated Risk Score** | **16 / 25** (Freq: 4 x Sev: 4) |
| **Root Cause Category** | **Verification Failure (Built Wrong)** |
| **Recommended Action** | Immediate escalation to on-call engineering; hotfix required. |

---

## 1. Executive Summary
**Hardware peripheral pairing failure caused by background thread UI violation**

---

## 2. Quantitative Risk Assessment Matrix

| Dimension | Rating (1-5) | Rationale & Behavioral Evidence |
| :--- | :---: | :--- |
| **Frequency** | `4 / 5` | Occurs on approximately 70% of initial onboarding attempts whenever high-frequency sensor streaming is concurrently active. |
| **Severity** | `4 / 5` | Completely blocks first-time device setup for end users with no automatic recovery or actionable error messaging. |
| **Risk Score** | `16 / 25` | **Critical Tier (Red)** - *Score = Frequency (4) x Severity (4)* |

> **Quality & Reliability Action Item**:
> Immediate escalation to on-call engineering; hotfix required.

---

## 3. Core Issue & Reproduction Pathway
### 3.1 Manifestation & Triggers
The peripheral pairing modal dialog fails to render on screen during accessory onboarding, leaving the user interface stuck on an infinite loading spinner. Triggered when the user taps "Pair New Peripheral" while the background telemetry worker holds the main synchronization lock.

---

## 4. Environmental & System State Context
Pre-State: Host OS version 16.5, available RAM 1.2 GB, wireless peripheral daemon active, peripheral streaming telemetry at 100Hz.
Post-State: Pairing timeout expires after 60 seconds; peripheral connection state is left stranded in "Connecting"; main UI thread watchdog logs an 8.4-second non-responsive freeze.

---

## 5. Retrospective Root-Cause Categorization

| Dimension | Classification & Engineering Analysis |
| :--- | :--- |
| **Taxonomy Category** | **Verification Failure (Built Wrong)** |
| **Technical Root Cause** | The peripheral onboarding coordinator invoked `showPairingDialog()` directly from a background dispatch callback thread instead of dispatching to the Main UI Thread. Unit tests mocked the UI dispatcher layer, and automated integration tests did not assert thread affinity during mock pairing. |

---

## 6. Corrective & Preventive Actions (CAPA)
1. **Immediate Remediation**: Address direct defect in implementation aligning with verified state constraints.
2. **Defect Prevention**: Implement automated regression test coverage specifically verifying the boundary condition.
3. **Process Improvement**: Update architectural/interface verification checklists for this failure class.
```

---

## Risk Score Calculation Matrix

$$\text{Risk Score} = \text{Frequency} \times \text{Severity} \quad (\text{Frequency}, \text{Severity} \in [1, 5])$$

| Risk Score | Tier Name | Label / Color | Engineering SLA & Recommendation |
| :---: | :--- | :---: | :--- |
| **16 - 25** | **Critical** | `[CRITICAL]` Red | **Immediate Escalation**: Page on-call engineering; hotfix required. |
| **10 - 15** | **High** | `[HIGH]` Orange | **Current Sprint Priority**: Assign to lead engineer; resolve within 24-48 hours. |
| **5 - 9** | **Medium** | `[MEDIUM]` Yellow | **Standard Triage**: Schedule for standard defect backlog in upcoming release. |
| **1 - 4** | **Low** | `[LOW]` Green | **Routine Backlog**: Address during maintenance cycles or polish sprints. |

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
  "badge": "[CRITICAL]",
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

Run the automated test suite using Python's built-in `unittest`:

```bash
python3 -B -m unittest discover -s tests -v
```

All 25 unit and scenario test cases validate:
* Risk tier boundary conditions (Critical, High, Medium, Low).
* Validation error reporting for missing or empty fields.
* Phase normalization and dispatching.
* Format generation for all 3 report types.
* End-to-end scenario workflows across Phases 1, 2, and 3.

---

## License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.
