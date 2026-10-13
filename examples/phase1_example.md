# Phase 1 Example: Core Triage (Crawl)

This example illustrates a complete **Phase 1 (Core Triage)** interaction for logging a simple UI freeze anomaly during network slowdown.

---

## Scenario Overview
* **Anomaly**: UI freeze in the catalog search filter.
* **Component**: Web/Mobile Client Interface.
* **Goal**: Capture the minimal reproduction pathway in 3 rapid questions.

---

## Conversational Transcript

### Step 0: Phase Selection
**Assistant**:
> Welcome to the Anomaly Thought Partner. Which phase would you like to run today?
> 1. **Phase 1: Core Triage (Crawl)** - Rapid capture of essentials for quick reproduction.
> 2. **Phase 2: Contextual Depth (Walk)** - Deep environmental and system state parameters.
> 3. **Phase 3: Thought Partner (Run)** - Root cause analysis and quantitative risk estimation.

**User**:
> Let's do Phase 1.

---

### Step 1: Manifestation
**Assistant**:
> What exactly does the user see or experience when this anomaly occurs?

**User**:
> The search filter dropdown becomes unresponsive, with the loading spinner frozen in place for over 15 seconds without throwing an explicit crash alert or error dialog.

---

### Step 2: Triggering Event
**Assistant**:
> What specific action, update, or system event triggered this anomaly?

**User**:
> The user enters a search query into the live filter input field while the network connection bandwidth is throttled to 50 kbps (simulated 2G/edge conditions).

---

### Step 3: Reproducibility
**Assistant**:
> Can you reliably reproduce this? If so, what are the steps?

**User**:
> Yes, it's 100% reproducible on throttled or high-latency connections.
> 1. Launch the application.
> 2. Navigate to the Catalog view.
> 3. Throttle network link to 50 kbps.
> 4. Rapidly type 5 characters into the filter input box.
> 5. Observe UI freeze.

---

## Synthesized Final Output

**Assistant**:
> Thank you. Here is your synthesized **Core Bug Report**:

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
The search filter dropdown becomes unresponsive, with the loading spinner frozen in place for over 15 seconds without throwing an explicit crash alert or error dialog.

## 3. Triggering Event
The user enters a search query into the live filter input field while the network connection bandwidth is throttled to 50 kbps (simulated 2G/edge conditions).

## 4. Steps to Reproduce
100% reproducible on throttled or high-latency connections.
1. Launch the application.
2. Navigate to the Catalog view.
3. Throttle network link to 50 kbps.
4. Rapidly type 5 characters into the filter input box.
5. Observe UI freeze.

---
*Report generated via Anomaly Thought Partner (Phase 1: Core Triage).*
