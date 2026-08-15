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
