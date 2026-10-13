# Product Requirements Document: Anomaly Thought Partner Skill

## 1. Overview and Objective

The Anomaly Thought Partner Skill is an interactive conversational workflow and programmatic toolkit for documenting, triaging, and analyzing software defects and system anomalies. It structures defect collection around a three-phase progression ("Crawl, Walk, Run") so both non-technical reporters and technical engineering teams can capture reproducible issue reports, environmental state transitions, quantitative risk scores, and retrospective root-cause classifications.

---

## 2. Target Audience and Use Cases

### 2.1 Non-Technical Users
* **Roles**: Customer support specialists, operations staff, product managers, and end users reporting unexpected application behavior.
* **Primary Needs**: Step-by-step conversational guidance that asks one clear question at a time, clarifies incomplete descriptions in plain language, and generates a structured issue report ready for an issue tracker without requiring command-line usage.

### 2.2 Quality Assurance and Diagnostic Engineers
* **Roles**: QA analysts, test engineers, and support engineers reproducing field issues.
* **Primary Needs**: Structured capture of discovery methods, pre-anomaly system states, triggering events, post-anomaly states, and reproduction steps to reduce clarification cycles between QA and development teams.

### 2.3 Software Engineers and Technical Leads
* **Roles**: Application developers, systems engineers, and incident leads conducting root-cause analysis and prioritization.
* **Primary Needs**: Quantitative risk scoring ($$\text{Risk Score} = \text{Frequency} \times \text{Severity}$$), SLA-aligned severity tiers, retrospective root-cause taxonomy classification, and Corrective and Preventive Actions (CAPA).

---

## 3. Functional Requirements: Three-Phase Workflow

At the start of an interaction, the assistant presents three operational phases unless a default phase (`DEFAULT_PHASE=1|2|3`) is pre-configured in the environment.

### 3.1 Phase 1: Core Triage (Crawl)
* **Goal**: Capture the essential reproduction pathway in three questions.
* **Sequential Questions**:
  1. **Manifestation**: `"What exactly does the user see or experience when this anomaly occurs?"`
  2. **Triggering Event**: `"What specific action, update, or system event triggered this anomaly?"`
  3. **Reproducibility**: `"Can you reliably reproduce this? If so, what are the steps?"`
* **Required Schema Fields**: `manifestation`, `triggering_event`, `reproducibility`.
* **Output Document**: `Core Bug Report` containing a summary table, 1-line summary, manifestation description, triggering event, and numbered reproduction steps.

### 3.2 Phase 2: Contextual Depth (Walk)
* **Goal**: Capture environmental conditions and system state boundaries before and after the anomaly across five questions.
* **Sequential Questions**:
  1. **Discovery Method**: `"How was this discovered (e.g., manual testing, automated crash logs, user report)?"`
  2. **Pre-Anomaly System State**: `"What was the system state right before the anomaly occurred? (e.g., OS version, battery level, device memory load, background syncing)?"`
  3. **Triggering Event**: `"What was the precise sequence of events or specific action that triggered the anomaly?"`
  4. **Post-Anomaly System State**: `"What happened immediately after the anomaly? (e.g., app crash, automatic recovery, system freeze)?"`
  5. **Reproducibility**: `"What are the exact steps to reproduce this issue reliably?"`
* **Required Schema Fields**: `discovery_method`, `pre_anomaly_state`, `triggering_event`, `post_anomaly_state`, `reproducibility`.
* **Output Document**: `Detailed Technical Anomaly Report` featuring discovery metadata, reproduction steps, a Markdown state transition table comparing `Pre-Anomaly State`, `Triggering Event`, and `Post-Anomaly State`, and technical trigger details.

### 3.3 Phase 3: Thought Partner (Run)
* **Goal**: Combine issue and environmental context with quantitative risk estimation and root-cause categorization across four questions.
* **Sequential Questions**:
  1. **The Core Issue**: `"How does this anomaly manifest, and what are the exact steps/triggers to reproduce it?"`
  2. **The Environment**: `"What was the system state before the anomaly (OS, memory, sync state), and what was the state immediately after?"`
  3. **Risk Estimation**: `"On a scale of 1 to 5, how would you rate the Frequency of this issue, and on a scale of 1 to 5, how would you rate its Severity? Please provide a brief rationale for both."`
  4. **Retrospective & Root Cause**: `"Looking at the root cause, was this a failure of Requirements (specified wrong), Verification (built wrong), or something else? Please provide any technical root-cause details."`
* **Required Schema Fields**: `core_issue`, `environment_state`, `frequency` (integer 1-5), `severity` (integer 1-5), `root_cause_category`, `root_cause_details`.
* **Output Document**: `Comprehensive Quality Assurance Report` featuring risk tier classification, calculated risk score matrix, core issue and environment breakdown, root-cause taxonomy analysis, and Corrective and Preventive Actions (CAPA).

---

## 4. Interaction and Disambiguation Requirements

1. **Single-Question Turn Protocol**: The assistant must ask only one question per conversational turn and wait for the user's response before advancing to the next question.
2. **Gentle Disambiguation**: When a user supplies an incomplete or ambiguous response (such as *"it crashed"* or *"it froze"*), the assistant must acknowledge the input and ask a targeted follow-up question to clarify the missing parameter (such as error codes, OS state, battery level, or UI responsiveness) before proceeding to the next phase question. Reference patterns are defined in [references/disambiguation_guide.md](references/disambiguation_guide.md).
3. **Input Validation**: All required fields for the selected phase must be validated for presence and type constraints before generating the final Markdown report.

---

## 5. Quantitative Risk Matrix Specification

Phase 3 evaluates defect priority using a two-variable product formula defined in [references/risk_matrix.md](references/risk_matrix.md) and implemented in [scripts/anomaly_helper.py](scripts/anomaly_helper.py):

$$\text{Risk Score} = \text{Frequency} \times \text{Severity} \quad (\text{Frequency}, \text{Severity} \in \{1, 2, 3, 4, 5\})$$

| Risk Score Range | Tier Name | Color | Label | Recommended Engineering Action |
| :---: | :--- | :--- | :---: | :--- |
| **16 - 25** | **Critical** | Red | `[CRITICAL]` | Immediate escalation to on-call engineering; hotfix required. |
| **10 - 15** | **High** | Orange | `[HIGH]` | Prioritize in current sprint; assign to lead engineer within 24 hours. |
| **5 - 9** | **Medium** | Yellow | `[MEDIUM]` | Schedule for standard bug triage and fix in upcoming release cycle. |
| **1 - 4** | **Low** | Green | `[LOW]` | Log in backlog; address during routine maintenance or polish sprint. |

---

## 6. Retrospective Root-Cause Taxonomy

Phase 3 classifies root causes into four primary categories documented in [references/root_cause_taxonomies.md](references/root_cause_taxonomies.md):

1. **Requirements Failure ("Specified Wrong")**: Implementation matched specifications, but the specification was incomplete, ambiguous, or contradictory.
2. **Verification Failure ("Built Wrong")**: Requirements were defined, but the implementation introduced a logic defect, concurrency issue, or regression that escaped testing.
3. **Architecture & Interface Failure**: Defect caused by structural coupling, boundary isolation gaps, or protocol mismatches across components.
4. **Environmental & Platform Failure**: Defect triggered by external host OS constraints, hardware faults, or resource exhaustion outside runtime control.

---

## 7. System Architecture and Repository Layout

All file references across the project use relative paths originating from the project root directory:

```text
anomaly-thought-skill/
|-- LICENSE
|-- README.md
|-- SKILL.md
|-- prd.md
|-- assets/
|   `-- skill_in_action.jpg
|-- examples/
|   |-- generated_reports/
|   |   |-- phase1_report.md
|   |   |-- phase2_report.md
|   |   `-- phase3_report.md
|   |-- mock_inputs.json
|   |-- phase1_example.md
|   |-- phase2_example.md
|   `-- phase3_example.md
|-- references/
|   |-- disambiguation_guide.md
|   |-- phase_specifications.md
|   |-- risk_matrix.md
|   `-- root_cause_taxonomies.md
|-- scripts/
|   |-- __init__.py
|   |-- anomaly_helper.py
|   `-- export_reports.py
`-- tests/
    |-- __init__.py
    |-- test_anomaly_helper.py
    `-- test_scenarios.py
```

### 7.1 Programmatic Components
* **[`scripts/anomaly_helper.py`](scripts/anomaly_helper.py)**: Provides `Phase.normalize()`, `calculate_risk()`, `validate_phase_data()`, `format_phase1_report()`, `format_phase2_report()`, `format_phase3_report()`, `generate_report()`, and a CLI supporting `--phase`, `--json`, `--file`, `--demo`, `--calculate-risk`, and `--output`.
* **[`scripts/export_reports.py`](scripts/export_reports.py)**: Batch export script that generates sample reports in `examples/generated_reports/` from the mock scenario datasets.

---

## 8. Verification and Validation Requirements

The automated test suite under `tests/` validates all core functional requirements using Python's `unittest` framework:

* **[`tests/test_anomaly_helper.py`](tests/test_anomaly_helper.py)**: Unit tests verifying risk tier boundary conditions (`1` to `25`), invalid input error handling (`ValueError`, `TypeError`), phase alias normalization, required field validation across Phases 1-3, and Markdown report structure.
* **[`tests/test_scenarios.py`](tests/test_scenarios.py)**: End-to-end scenario tests validating Phase 1 (UI freeze during network slowdown), Phase 2 (mobile application crash under low battery and background synchronization), and Phase 3 (wireless peripheral pairing failure caused by background thread UI invocation).
