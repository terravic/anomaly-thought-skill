# Gentle Disambiguation Guide

When users provide brief, vague, or incomplete responses during the anomaly logging workflow, the assistant must avoid proceeding blindly. Instead, the assistant applies **Gentle Disambiguation** to solicit missing parameters while maintaining a supportive, technical tone.

---

## Core Disambiguation Principles

1. **Acknowledge and Validate**: Briefly acknowledge what the user stated.
2. **Target Specific Missing Parameters**: Ask specifically for the missing dimension (e.g., error codes, OS version, thread activity, resource constraints).
3. **Offer Concrete Examples**: Provide 2–3 illustrative examples to guide the engineer without sounding prescriptive.
4. **Never Ask Compound Questions**: Keep the follow-up focused on resolving a single ambiguity.

---

## Common Vague Responses and Gentle Follow-Ups

### Case 1: "It crashed."
* **Ambiguity**: Crash type (unhandled exception, OS termination, OOM, SIGSEGV), stack trace, or visible symptom.
* **Gentle Disambiguation**:
  > *"To help isolate the crash type, was there an unhandled exception stack trace, an error dialog, or did the process abruptly terminate back to the host operating system/home screen?"*

### Case 2: "It's slow." / "It froze."
* **Ambiguity**: Duration of freeze, main thread lock vs background latency, UI responsiveness.
* **Gentle Disambiguation**:
  > *"Did the user interface completely stop responding to input (such as an Application Not Responding / main thread freeze), or was a background network request taking an extended period to resolve?"*

### Case 3: "Doesn't work in low power mode."
* **Ambiguity**: Specific battery percentage, system background sync restrictions, CPU throttling.
* **Gentle Disambiguation**:
  > *"Could you specify the approximate battery level (e.g., below 10%) and whether OS-level background task throttling was active when this occurred?"*

### Case 4: "Hardware won't connect."
* **Ambiguity**: Protocol state, discovery vs pairing vs GATT connection, error codes.
* **Gentle Disambiguation**:
  > *"Does the peripheral fail during initial advertisement scanning, during the pairing handshake modal, or after establishing a connection during data streaming?"*

### Case 5: "Risk is 4 and 4." (Missing rationales)
* **Ambiguity**: No justification for frequency or severity ratings.
* **Gentle Disambiguation**:
  > *"Understood: Frequency = 4/5 and Severity = 4/5. Could you provide a one-sentence rationale for each (e.g., how often users encounter this in production, and how severely it blocks user workflows)?"*
