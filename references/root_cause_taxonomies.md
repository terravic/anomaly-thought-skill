# Root Cause Taxonomy Reference

In **Phase 3 (Thought Partner)**, anomalies are categorized systematically to facilitate defect prevention and Corrective and Preventive Actions (CAPA).

---

## Primary Root Cause Taxonomies

### 1. Requirements Failure (*"Specified Wrong"*)
* **Definition**: The implementation faithfully adhered to specifications, but the specification itself was incomplete, ambiguous, contradictory, or architecturally flawed.
* **Common Examples**:
  * Undefined behavior for network timeouts or edge-case input values.
  * Omission of low-power mode memory quotas.
  * Incompatible state transition assumptions between subsystem contracts.
* **Target Prevention**: Formal requirement reviews, contract testing, and product requirement edge-case matrices.

---

### 2. Verification Failure (*"Built Wrong"*)
* **Definition**: The requirement was well-defined and understood, but the implementation contained a logic flaw, concurrency defect, thread violation, or regression that escaped verification.
* **Common Examples**:
  * Invoking UI operations from a background thread or dispatch queue.
  * Unhandled null/nil pointers or out-of-bounds array accesses.
  * Inadequate unit/integration test assertions (e.g., mocking out the bug-inducing subsystem).
* **Target Prevention**: Unit test thread-affinity assertions, static analysis linters, integration test suites on physical/virtual targets.

---

### 3. Architecture & Interface Failure
* **Definition**: Defect stemming from structural coupling, improper boundary isolation, or protocol mismatch across boundaries.
* **Common Examples**:
  * Synchronous blocking RPCs on reactive event loops.
  * Deadlocks caused by inconsistent mutex acquisition orders across services.
* **Target Prevention**: Architectural design reviews, async-first boundary enforcement, threat modeling.

---

### 4. Environmental & Platform Failure
* **Definition**: Defect triggered exclusively by external host platform anomalies, hardware faults, or OS-level resource starvation beyond standard runtime control.
* **Common Examples**:
  * Host OS kernel panic or hardware peripheral firmware crash.
  * File system read-only mount during flash degradation.
* **Target Prevention**: Defensive fault isolation, graceful degradation wrappers, circuit breakers.
