# Quantitative Risk Matrix Reference

The Anomaly Thought Partner employs a standardized, objective two-variable risk matrix to quantify anomaly impact and guide escalation.

---

## Mathematical Formulation

$$\text{Risk Score} = \text{Frequency} \times \text{Severity}$$

Where:
* $\text{Frequency} \in \{1, 2, 3, 4, 5\}$
* $\text{Severity} \in \{1, 2, 3, 4, 5\}$
* $\text{Risk Score} \in [1, 25]$

---

## Rating Scales (1 to 5)

### Frequency Scale
* **1 (Rare)**: Edge-case occurrence (<1% of user sessions or isolated setup conditions).
* **2 (Uncommon)**: Occurs sporadically (1%–5% of sessions or under specific load conditions).
* **3 (Moderate)**: Occurs periodically (5%–20% of sessions or standard feature usage).
* **4 (Frequent)**: Occurs consistently (20%–70% of sessions under recurring conditions).
* **5 (Ubiquitous / Constant)**: Occurs in >70% of attempts or on every standard execution.

### Severity Scale
* **1 (Cosmetic / Trivial)**: Minor aesthetic flaw; no functional degradation or data impact.
* **2 (Minor)**: Slight annoyance or non-blocking workaround available; core workflow unaffected.
* **3 (Moderate)**: Degraded performance or secondary feature unavailable; workaround exists.
* **4 (Major)**: Core feature blocked or significant data inconsistency; workaround complex or nonexistent.
* **5 (Catastrophic)**: System crash, data corruption, security vulnerability, or total loss of service.

---

## Risk Tier Classification Table

| Risk Score | Tier Name | Color Code | Badge | Engineering SLA & Recommendation |
| :---: | :--- | :--- | :---: | :--- |
| **16 – 25** | **Critical** | Red | 🔴 | **Immediate Escalation**: Page on-call engineering; block release; hotfix required. |
| **10 – 15** | **High** | Orange | 🟠 | **Current Sprint Priority**: Assign to lead engineer; resolve within 24–48 hours. |
| **5 – 9** | **Medium** | Yellow | 🟡 | **Standard Triage**: Schedule for standard defect backlog; resolve in next release cycle. |
| **1 – 4** | **Low** | Green | 🟢 | **Routine Backlog**: Address during maintenance cycles, polish sprints, or minor refactoring. |

---

## Quick Reference Heatmap

| Freq \ Sev | 1 (Cosmetic) | 2 (Minor) | 3 (Moderate) | 4 (Major) | 5 (Catastrophic) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **5 (Constant)** | 🟡 5 | 🟠 10 | 🟠 15 | 🔴 20 | 🔴 25 |
| **4 (Frequent)** | 🟢 4 | 🟡 8 | 🟠 12 | 🔴 16 | 🔴 20 |
| **3 (Moderate)** | 🟢 3 | 🟡 6 | 🟡 9 | 🟠 12 | 🟠 15 |
| **2 (Uncommon)** | 🟢 2 | 🟢 4 | 🟡 6 | 🟡 8 | 🟠 10 |
| **1 (Rare)** | 🟢 1 | 🟢 2 | 🟢 3 | 🟢 4 | 🟡 5 |
