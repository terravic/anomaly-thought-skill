# Anomaly Thought Partner: Phase Specifications

This reference specifies the objectives, sequential questioning protocols, schema constraints, and output artifacts across the three operational phases of the Anomaly Thought Partner Skill.

---

## Overview

| Phase | Paradigm | Target Audience | Primary Focus | Output Report |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1** | **Crawl** | Rapid triage / First responders | Core reproduction pathway | `Core Bug Report` |
| **Phase 2** | **Walk** | QA engineers / Diagnostic devs | Environmental state transitions | `Detailed Technical Anomaly Report` |
| **Phase 3** | **Run** | Senior engineers / Staff / QAC | Root cause & quantitative risk | `Comprehensive QAC Recommendation Report` |

---

## Phase 1: Core Triage (Crawl)

### Objective
Capture the absolute minimum essential information needed to reproduce a defect immediately, minimizing developer friction.

### Question Sequence (Strictly One at a Time)
1. **Manifestation**:
   > *"What exactly does the user see or experience when this anomaly occurs?"*
2. **Triggering Event**:
   > *"What specific action, update, or system event triggered this anomaly?"*
3. **Reproducibility**:
   > *"Can you reliably reproduce this? If so, what are the steps?"*

### Required Fields
* `manifestation` (string, non-empty)
* `triggering_event` (string, non-empty)
* `reproducibility` (string, non-empty)

### Synthesized Output Structure
* **Header**: `# Core Bug Report`
* **Metadata Table**: Phase (Phase 1: Core Triage), Status (Ready for Triage), Summary
* **Sections**: Summary, Manifestation, Triggering Event, Steps to Reproduce

---

## Phase 2: Contextual Depth (Walk)

### Objective
Capture structured pre- and post-anomaly system states and execution parameters to eliminate time-consuming back-and-forth between QA and engineering.

### Question Sequence (Strictly One at a Time)
1. **Discovery Method**:
   > *"How was this discovered (e.g., manual testing, automated crash logs, user report)?"*
2. **Pre-Anomaly System State**:
   > *"What was the system state right before the anomaly occurred? (e.g., OS version, battery level, device memory load, background syncing)?"*
3. **Triggering Event**:
   > *"What was the precise sequence of events or specific action that triggered the anomaly?"*
4. **Post-Anomaly System State**:
   > *"What happened immediately after the anomaly? (e.g., app crash, automatic recovery, system freeze)?"*
5. **Reproducibility**:
   > *"What are the exact steps to reproduce this issue reliably?"*

### Required Fields
* `discovery_method` (string, non-empty)
* `pre_anomaly_state` (string, non-empty)
* `triggering_event` (string, non-empty)
* `post_anomaly_state` (string, non-empty)
* `reproducibility` (string, non-empty)

### Synthesized Output Structure
* **Header**: `# Detailed Technical Anomaly Report`
* **Metadata Table**: Phase, Status, Summary, Discovery Method
* **Sections**: Executive Summary, Discovery & Reproduction, System State Transitions Table (Pre vs. Post vs. Trigger), Technical Trigger Details

---

## Phase 3: The True "Thought Partner" (Run)

### Objective
Elevate engineering quality and reliability through quantitative risk assessment, state transition modeling, and retrospective root-cause classification.

### Question Sequence (Strictly One at a Time)
1. **The Core Issue**:
   > *"How does this anomaly manifest, and what are the exact steps/triggers to reproduce it?"*
2. **The Environment**:
   > *"What was the system state before the anomaly (OS, memory, sync state), and what was the state immediately after?"*
3. **Risk Estimation**:
   > *"On a scale of 1 to 5, how would you rate the Frequency of this issue, and on a scale of 1 to 5, how would you rate its Severity? Please provide a brief rationale for both."*
4. **Retrospective & Root Cause**:
   > *"Looking at the root cause, was this a failure of Requirements (specified wrong), Verification (built wrong), or something else? Please provide any technical root-cause details."*

### Required Fields
* `core_issue` (string, non-empty)
* `environment_state` (string, non-empty)
* `frequency` (integer, 1..5)
* `severity` (integer, 1..5)
* `root_cause_category` (string: "Requirements Failure", "Verification Failure", or "Other")
* `root_cause_details` (string, non-empty)

### Synthesized Output Structure
* **Header**: `# Comprehensive QAC Recommendation Report`
* **Metadata Table**: Phase, Overall Risk Tier (with badge/color), Calculated Risk Score (Freq x Sev), Root Cause Category, Recommended SLA Action
* **Sections**: Executive Summary, Quantitative Risk Assessment Matrix, Core Issue & Reproduction Pathway, Environmental Context, Retrospective Root-Cause Categorization, Corrective & Preventive Actions (CAPA)
