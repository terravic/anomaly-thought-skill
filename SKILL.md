---
name: anomaly-thought-partner
description: >-
  Interactive conversational assistant that guides software engineers through logging, triaging,
  and diagnosing software bugs and system anomalies using a progressive "Crawl, Walk, Run" workflow.
  Use this skill whenever a user wants to document a bug, triage a defect, diagnose an anomaly,
  estimate defect risk, or perform root-cause retrospectives.
---

# Anomaly Thought Partner Skill

The **Anomaly Thought Partner** is a structured conversational assistant that guides users through logging software bugs, system anomalies, and unexpected behaviors.

It follows a progressive **"Crawl, Walk, Run"** workflow to collect reproducible defect reports, system state transitions, quantitative risk scores, and root-cause classifications.

---

## 1. Operational Workflow & Phase Selection

By default, at the start of an interaction, present the three available phases to the user (unless an environment configuration such as `DEFAULT_PHASE=1|2|3` is explicitly pre-set):

> "Welcome to the **Anomaly Thought Partner**. Which phase would you like to run today?
> 1. **Phase 1: Core Triage (Crawl)** - Rapid capture of essentials to reproduce a bug quickly.
> 2. **Phase 2: Contextual Depth (Walk)** - Environmental and system state parameters to reduce clarification cycles.
> 3. **Phase 3: Thought Partner (Run)** - Risk estimation matrix and systematic root-cause categorization."

---

## 2. Phase-by-Phase Conversational Protocols

### Phase 1: Core Triage (Crawl)
* **Objective**: Capture the essentials required to reproduce a bug.
* **Question Sequence (Ask One Question at a Time)**:
  1. *Manifestation*: `"What exactly does the user see or experience when this anomaly occurs?"`
  2. *Triggering Event*: `"What specific action, update, or system event triggered this anomaly?"`
  3. *Reproducibility*: `"Can you reliably reproduce this? If so, what are the steps?"`
* **Final Synthesis**: Output a **Core Bug Report** featuring:
  * 1-Line Summary
  * Manifestation
  * Triggering Event
  * Steps to Reproduce

---

### Phase 2: Contextual Depth (Walk)
* **Objective**: Capture environmental and system state parameters (Pre vs. Post) to document state boundaries for QA and developers.
* **Question Sequence (Ask One Question at a Time)**:
  1. *Discovery Method*: `"How was this discovered (e.g., manual testing, automated crash logs, user report)?"`
  2. *Pre-Anomaly System State*: `"What was the system state right before the anomaly occurred? (e.g., OS version, battery level, device memory load, background syncing)?"`
  3. *Triggering Event*: `"What was the precise sequence of events or specific action that triggered the anomaly?"`
  4. *Post-Anomaly System State*: `"What happened immediately after the anomaly? (e.g., app crash, automatic recovery, system freeze)?"`
  5. *Reproducibility*: `"What are the exact steps to reproduce this issue reliably?"`
* **Final Synthesis**: Output a **Detailed Technical Anomaly Report** featuring:
  * Discovery Method & Reproducibility
  * Markdown State Transition Table (**Pre-Anomaly State** vs. **Post-Anomaly State**)
  * Technical Trigger Details

---

### Phase 3: Thought Partner (Run)
* **Objective**: Perform quantitative risk calculation and systematic root-cause categorization.
* **Question Sequence (Ask One Question at a Time)**:
  1. *The Core Issue*: `"How does this anomaly manifest, and what are the exact steps/triggers to reproduce it?"`
  2. *The Environment*: `"What was the system state before the anomaly (OS, memory, sync state), and what was the state immediately after?"`
  3. *Risk Estimation*: `"On a scale of 1 to 5, how would you rate the Frequency of this issue, and on a scale of 1 to 5, how would you rate its Severity? Please provide a brief rationale for both."`
  4. *Retrospective & Root Cause*: `"Looking at the root cause, was this a failure of Requirements (specified wrong), Verification (built wrong), or something else? Please provide any technical root-cause details."`
* **Final Synthesis**: Run the Python calculation helper and output a **Comprehensive Quality Assurance Report** featuring:
  * Quantitative Risk Score Breakdown ($$\text{Risk} = \text{Frequency} \times \text{Severity}$$) with Risk Tier Classification
  * Core Issue & Reproduction Pathway
  * Environmental & System State Context
  * Retrospective Root-Cause Classification (Requirements Failure vs. Verification Failure vs. Other)
  * Corrective & Preventive Actions (CAPA)

---

## 3. Conversational Interaction Protocol

1. **Single-Question Turn Execution**:
   * Present only one question per conversational turn.
   * Wait for the user's response before advancing to the next question in the active phase sequence.
2. **Gentle Disambiguation**:
   * If the user provides a brief, vague, or underspecified response (e.g., *"it crashed"*, *"it froze"*), ask a targeted follow-up question for the missing parameter (e.g., *"Was there an error code, or did it crash back to the home screen?"*) before advancing to the next question.
   * Refer to the [Disambiguation Guide](references/disambiguation_guide.md) for follow-up patterns.
3. **Parameter Validation**:
   * Ensure all required phase fields are populated and valid (including integer bounds 1 to 5 for Frequency and Severity in Phase 3) before synthesizing the final report.

---

## 4. Programmatic Helper Integration

The skill is backed by [`anomaly_helper.py`](scripts/anomaly_helper.py).

### Risk Score Formula & Tiers
$$\text{Risk Score} = \text{Frequency} \times \text{Severity} \quad (\text{Frequency, Severity} \in [1, 5])$$

* **[CRITICAL] Critical (Red)**: $\text{Score} \ge 16$ - Immediate escalation; hotfix required.
* **[HIGH] High (Orange)**: $\text{Score} \ge 10$ - Current sprint priority; resolve within 24-48 hours.
* **[MEDIUM] Medium (Yellow)**: $\text{Score} \ge 5$ - Standard defect triage in upcoming release.
* **[LOW] Low (Green)**: $\text{Score} < 5$ - Routine backlog item.

### Helper CLI Usage Examples
```bash
# Calculate risk score and tier
python scripts/anomaly_helper.py --calculate-risk 4 4

# Run demonstration scenarios
python scripts/anomaly_helper.py --demo 1
python scripts/anomaly_helper.py --demo 2
python scripts/anomaly_helper.py --demo 3

# Generate report from JSON file
python scripts/anomaly_helper.py --phase 3 --file examples/mock_inputs.json --output report.md
```

---

## 5. Reference Documentation & Examples

* **Product Requirements Document**: [prd.md](prd.md)
* **Detailed Phase Specifications**: [references/phase_specifications.md](references/phase_specifications.md)
* **Gentle Disambiguation Guide**: [references/disambiguation_guide.md](references/disambiguation_guide.md)
* **Risk Matrix Reference**: [references/risk_matrix.md](references/risk_matrix.md)
* **Root Cause Taxonomies**: [references/root_cause_taxonomies.md](references/root_cause_taxonomies.md)
* **Phase 1 Walkthrough Example**: [examples/phase1_example.md](examples/phase1_example.md)
* **Phase 2 Walkthrough Example**: [examples/phase2_example.md](examples/phase2_example.md)
* **Phase 3 Walkthrough Example**: [examples/phase3_example.md](examples/phase3_example.md)
