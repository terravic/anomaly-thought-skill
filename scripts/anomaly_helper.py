#!/usr/bin/env python3
"""
Anomaly Helper Module for the Anomaly Thought Partner Skill.

This module provides:
1. Risk score calculation and tier classification (Frequency x Severity matrix).
2. Phase-specific data validation for Crawl (Phase 1), Walk (Phase 2), and Run (Phase 3).
3. Professional Markdown report generation tailored to each phase.
4. CLI and interactive modes for standalone and automated execution.
"""

import argparse
import json
import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union


class Phase(str, Enum):
    PHASE_1 = "phase_1"
    PHASE_2 = "phase_2"
    PHASE_3 = "phase_3"

    @classmethod
    def normalize(cls, phase_input: Union[str, int, "Phase"]) -> "Phase":
        """Normalize various phase input representations to a Phase enum."""
        if isinstance(phase_input, Phase):
            return phase_input
        
        str_val = str(phase_input).strip().lower()
        if str_val in ("1", "phase_1", "phase 1", "phase1", "crawl", "core", "core_triage"):
            return cls.PHASE_1
        elif str_val in ("2", "phase_2", "phase 2", "phase2", "walk", "contextual", "contextual_depth"):
            return cls.PHASE_2
        elif str_val in ("3", "phase_3", "phase 3", "phase3", "run", "thought_partner", "qac"):
            return cls.PHASE_3
        else:
            raise ValueError(
                f"Unknown phase: {phase_input}. Expected 1 (Crawl), 2 (Walk), or 3 (Run)."
            )


class RiskTier(Enum):
    CRITICAL = ("Critical", "Red", "🔴", 16, 25, "Immediate escalation to on-call engineering; hotfix required.")
    HIGH = ("High", "Orange", "🟠", 10, 15, "Prioritize in current sprint; assign to lead engineer within 24 hours.")
    MEDIUM = ("Medium", "Yellow", "🟡", 5, 9, "Schedule for standard bug triage and fix in upcoming release cycle.")
    LOW = ("Low", "Green", "🟢", 1, 4, "Log in backlog; address during routine maintenance or polish sprint.")

    def __init__(self, tier_name: str, color: str, badge: str, min_score: int, max_score: int, recommendation: str):
        self.tier_name = tier_name
        self.color = color
        self.badge = badge
        self.min_score = min_score
        self.max_score = max_score
        self.recommendation = recommendation


@dataclass
class RiskEvaluation:
    frequency: int
    severity: int
    score: int
    tier: RiskTier
    tier_name: str
    color: str
    badge: str
    recommendation: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "frequency": self.frequency,
            "severity": self.severity,
            "score": self.score,
            "tier_name": self.tier_name,
            "color": self.color,
            "badge": self.badge,
            "recommendation": self.recommendation,
        }


def calculate_risk(frequency: int, severity: int) -> RiskEvaluation:
    """
    Calculate dynamic risk score and determine risk tier.
    
    Formula: Risk = Frequency * Severity
    Inputs:
        frequency: Integer between 1 and 5 (inclusive)
        severity: Integer between 1 and 5 (inclusive)
        
    Tiers:
        Score >= 16 -> Critical (Red)
        Score >= 10 -> High (Orange)
        Score >= 5  -> Medium (Yellow)
        Score < 5   -> Low (Green)
    """
    try:
        freq_int = int(frequency)
        sev_int = int(severity)
    except (ValueError, TypeError) as e:
        raise TypeError(f"Frequency and Severity must be integers. Received frequency={frequency}, severity={severity}") from e

    if not (1 <= freq_int <= 5):
        raise ValueError(f"Frequency must be between 1 and 5 (inclusive). Received: {freq_int}")
    if not (1 <= sev_int <= 5):
        raise ValueError(f"Severity must be between 1 and 5 (inclusive). Received: {sev_int}")

    score = freq_int * sev_int

    if score >= 16:
        tier = RiskTier.CRITICAL
    elif score >= 10:
        tier = RiskTier.HIGH
    elif score >= 5:
        tier = RiskTier.MEDIUM
    else:
        tier = RiskTier.LOW

    return RiskEvaluation(
        frequency=freq_int,
        severity=sev_int,
        score=score,
        tier=tier,
        tier_name=tier.tier_name,
        color=tier.color,
        badge=tier.badge,
        recommendation=tier.recommendation,
    )


# Required fields per phase
REQUIRED_FIELDS = {
    Phase.PHASE_1: [
        "manifestation",
        "triggering_event",
        "reproducibility",
    ],
    Phase.PHASE_2: [
        "discovery_method",
        "pre_anomaly_state",
        "triggering_event",
        "post_anomaly_state",
        "reproducibility",
    ],
    Phase.PHASE_3: [
        "core_issue",
        "environment_state",
        "frequency",
        "severity",
        "root_cause_category",
        "root_cause_details",
    ],
}


def _clean_str(val: Any) -> str:
    if val is None:
        return ""
    return str(val).strip()


def validate_phase_data(phase_input: Union[str, int, Phase], data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate that all required fields for the active phase are populated and valid.
    
    Returns:
        (is_valid: bool, errors: List[str])
    """
    try:
        phase = Phase.normalize(phase_input)
    except ValueError as e:
        return False, [str(e)]

    if not isinstance(data, dict):
        return False, ["Input data must be a dictionary/JSON object."]

    errors: List[str] = []
    required = REQUIRED_FIELDS[phase]

    for field_name in required:
        if field_name not in data:
            errors.append(f"Missing required field: '{field_name}'")
            continue

        val = data[field_name]

        if field_name in ("frequency", "severity"):
            try:
                num_val = int(val)
                if not (1 <= num_val <= 5):
                    errors.append(f"Field '{field_name}' must be an integer between 1 and 5. Received: {num_val}")
            except (ValueError, TypeError):
                errors.append(f"Field '{field_name}' must be an integer between 1 and 5. Received: '{val}'")
        else:
            cleaned = _clean_str(val)
            if not cleaned:
                errors.append(f"Field '{field_name}' cannot be empty.")

    # Phase 3 specific checks
    if phase == Phase.PHASE_3 and "root_cause_category" in data:
        cat = _clean_str(data["root_cause_category"]).lower()
        if not any(v in cat for v in ["requirement", "verification", "other", "architecture", "environment", "implementation"]):
            errors.append(
                f"Field 'root_cause_category' should classify into Requirements Failure, Verification Failure, or Other. Received: '{data['root_cause_category']}'"
            )

    return len(errors) == 0, errors


def _extract_summary(data: Dict[str, Any], default: str) -> str:
    if "summary" in data and _clean_str(data["summary"]):
        return _clean_str(data["summary"])
    if "manifestation" in data and _clean_str(data["manifestation"]):
        man = _clean_str(data["manifestation"]).split(".")[0].strip()
        return man[:120] if len(man) > 120 else man
    if "core_issue" in data and _clean_str(data["core_issue"]):
        core = _clean_str(data["core_issue"]).split(".")[0].strip()
        return core[:120] if len(core) > 120 else core
    return default


def format_phase1_report(data: Dict[str, Any]) -> str:
    """Format Phase 1 (Core Triage / Crawl) Bug Report in clean Markdown."""
    summary = _extract_summary(data, "Core Anomaly Report")
    manifestation = _clean_str(data.get("manifestation", "N/A"))
    trigger = _clean_str(data.get("triggering_event", "N/A"))
    reproducibility = _clean_str(data.get("reproducibility", "N/A"))

    report = f"""# Core Bug Report

| Metric | Details |
| :--- | :--- |
| **Phase** | Phase 1: Core Triage (Crawl) |
| **Status** | Ready for Triage |
| **Summary** | {summary} |

---

## 1. Summary
> **{summary}**

## 2. Manifestation
{manifestation}

## 3. Triggering Event
{trigger}

## 4. Steps to Reproduce
{reproducibility}

---
*Report generated via Anomaly Thought Partner (Phase 1: Core Triage).*
"""
    return report.strip()


def format_phase2_report(data: Dict[str, Any]) -> str:
    """Format Phase 2 (Contextual Depth / Walk) Detailed Technical Report in clean Markdown."""
    summary = _extract_summary(data, "Detailed Technical Anomaly Report")
    discovery = _clean_str(data.get("discovery_method", "N/A"))
    pre_state = _clean_str(data.get("pre_anomaly_state", "N/A"))
    trigger = _clean_str(data.get("triggering_event", "N/A"))
    post_state = _clean_str(data.get("post_anomaly_state", "N/A"))
    reproducibility = _clean_str(data.get("reproducibility", "N/A"))

    report = f"""# Detailed Technical Anomaly Report

| Attribute | Specification |
| :--- | :--- |
| **Phase** | Phase 2: Contextual Depth (Walk) |
| **Status** | Diagnostic Ready |
| **Summary** | {summary} |
| **Discovery Method** | {discovery} |

---

## 1. Executive Summary
**{summary}**

---

## 2. Discovery & Reproduction
* **Discovery Method**: {discovery}
* **Reproducibility**:
{reproducibility}

---

## 3. System State Transitions

| State Boundary | System Condition / Parameter Profile |
| :--- | :--- |
| **Pre-Anomaly State** | {pre_state} |
| **Triggering Event** | {trigger} |
| **Post-Anomaly State** | {post_state} |

---

## 4. Technical Trigger Details
{trigger}

---
*Report generated via Anomaly Thought Partner (Phase 2: Contextual Depth).*
"""
    return report.strip()


def format_phase3_report(data: Dict[str, Any]) -> str:
    """Format Phase 3 (The True Thought Partner / Run) Comprehensive QAC Report."""
    freq = int(data.get("frequency", 1))
    sev = int(data.get("severity", 1))
    risk_eval = calculate_risk(freq, sev)

    summary = _extract_summary(data, "Comprehensive QAC Recommendation Report")
    core_issue = _clean_str(data.get("core_issue", "N/A"))
    env_state = _clean_str(data.get("environment_state", "N/A"))
    freq_rationale = _clean_str(data.get("frequency_rationale", "Standard observation frequency."))
    sev_rationale = _clean_str(data.get("severity_rationale", "Standard severity assessment."))
    root_cause_cat = _clean_str(data.get("root_cause_category", "N/A"))
    root_cause_details = _clean_str(data.get("root_cause_details", "N/A"))

    report = f"""# Comprehensive QAC Recommendation Report

| Assessment Metric | Value |
| :--- | :--- |
| **Phase** | Phase 3: The True \"Thought Partner\" (Run) |
| **Overall Risk Tier** | {risk_eval.badge} **{risk_eval.tier_name}** ({risk_eval.color}) |
| **Calculated Risk Score** | **{risk_eval.score} / 25** (Freq: {freq} × Sev: {sev}) |
| **Root Cause Category** | **{root_cause_cat}** |
| **Recommended Action** | {risk_eval.recommendation} |

---

## 1. Executive Summary
**{summary}**

---

## 2. Quantitative Risk Assessment Matrix

| Dimension | Rating (1–5) | Rationale & Behavioral Evidence |
| :--- | :---: | :--- |
| **Frequency** | `{freq} / 5` | {freq_rationale} |
| **Severity** | `{sev} / 5` | {sev_rationale} |
| **Risk Score** | `{risk_eval.score} / 25` | **{risk_eval.tier_name} Tier ({risk_eval.color})** — *Score = Frequency ({freq}) × Severity ({sev})* |

> **Quality & Reliability Action Item**:
> {risk_eval.recommendation}

---

## 3. Core Issue & Reproduction Pathway
### 3.1 Manifestation & Triggers
{core_issue}

---

## 4. Environmental & System State Context
{env_state}

---

## 5. Retrospective Root-Cause Categorization

| Dimension | Classification & Engineering Analysis |
| :--- | :--- |
| **Taxonomy Category** | **{root_cause_cat}** |
| **Technical Root Cause** | {root_cause_details} |

---

## 6. Corrective & Preventive Actions (CAPA)
1. **Immediate Remediation**: Address direct defect in implementation aligning with verified state constraints.
2. **Defect Prevention**: Implement automated regression test coverage specifically verifying the boundary condition.
3. **Process Improvement**: Update architectural/interface verification checklists for this failure class.

---
*Report generated via Anomaly Thought Partner (Phase 3: The True \"Thought Partner\").*
"""
    return report.strip()


def generate_report(phase_input: Union[str, int, Phase], data: Dict[str, Any]) -> str:
    """
    Validate input data and generate the phase-specific Markdown report.
    Raises ValueError if validation fails.
    """
    phase = Phase.normalize(phase_input)
    is_valid, errors = validate_phase_data(phase, data)
    if not is_valid:
        raise ValueError(f"Validation failed for {phase.value}: " + "; ".join(errors))

    if phase == Phase.PHASE_1:
        return format_phase1_report(data)
    elif phase == Phase.PHASE_2:
        return format_phase2_report(data)
    elif phase == Phase.PHASE_3:
        return format_phase3_report(data)
    else:
        raise ValueError(f"Unsupported phase: {phase}")


# Mock datasets for testing, demonstrations, and CLI samples
MOCK_SCENARIOS = {
    Phase.PHASE_1: {
        "summary": "UI freeze during network slowdown in catalog search filter",
        "manifestation": "The search filter dropdown becomes unresponsive, with the loading spinner frozen in place for over 15 seconds without throwing an explicit crash alert or error dialog.",
        "triggering_event": "The user enters a search query into the live filter input field while the network connection bandwidth is throttled to 50 kbps (simulated 2G/edge conditions).",
        "reproducibility": "100% reproducible on throttled or high-latency connections.\n1. Launch the application.\n2. Navigate to the Catalog view.\n3. Throttle network link to 50 kbps.\n4. Rapidly type 5 characters into the filter input box.\n5. Observe UI freeze.",
    },
    Phase.PHASE_2: {
        "summary": "Mobile application crash during low-battery mode and active background synchronization",
        "discovery_method": "Automated crash telemetry alert (SIGSEGV / OOM termination recorded in staging telemetry).",
        "pre_anomaly_state": "Device OS version 14.2, device memory utilization at 88% (constrained), battery level at 9% with system Low-Power Mode active, and background data synchronization worker active with 45 pending payloads.",
        "triggering_event": "Background synchronization worker attempts to batch-deserialize and allocate an uncompressed 25MB sync payload while the host OS aggressively limits CPU execution quotas and background memory under low-battery throttling.",
        "post_anomaly_state": "Application process is abruptly terminated to the home screen; background worker thread is killed; sync checkpoint file is left in a partially written 0-byte lock state.",
        "reproducibility": "Consistently reproducible (4 out of 5 attempts) under low power and high queue volume.\n1. Configure device battery level to 8% (Low-Power Mode triggered).\n2. Enqueue 45 uncompressed synchronization items.\n3. Trigger background sync worker.\n4. Observe process termination.",
    },
    Phase.PHASE_3: {
        "summary": "Hardware peripheral pairing failure caused by background thread UI violation",
        "core_issue": "The peripheral pairing modal dialog fails to render on screen during accessory onboarding, leaving the user interface stuck on an infinite loading spinner. Triggered when the user taps \"Pair New Peripheral\" while the background telemetry worker holds the main synchronization lock.",
        "environment_state": "Pre-State: Host OS version 16.5, available RAM 1.2 GB, Bluetooth daemon active, peripheral streaming telemetry at 100Hz.\nPost-State: Pairing timeout expires after 60 seconds; peripheral connection state is left stranded in \"Connecting\"; main UI thread watchdog logs an 8.4-second non-responsive freeze.",
        "frequency": 4,
        "frequency_rationale": "Occurs on approximately 70% of initial onboarding attempts whenever high-frequency sensor streaming is concurrently active.",
        "severity": 4,
        "severity_rationale": "Completely blocks first-time device setup for end users with no automatic recovery or actionable error messaging.",
        "root_cause_category": "Verification Failure (Built Wrong)",
        "root_cause_details": "The peripheral onboarding coordinator invoked `showPairingDialog()` directly from a background dispatch callback thread instead of dispatching to the Main UI Thread. Unit tests mocked the UI dispatcher layer, and automated integration tests did not assert thread affinity during mock pairing.",
    },
}


def main():
    parser = argparse.ArgumentParser(
        description="Anomaly Thought Partner helper script for bug logging, risk assessment, and report generation."
    )
    parser.add_argument(
        "--phase",
        choices=["1", "2", "3", "phase_1", "phase_2", "phase_3", "crawl", "walk", "run"],
        default="1",
        help="Active phase (1: Crawl, 2: Walk, 3: Run). Default is 1.",
    )
    parser.add_argument(
        "--json",
        type=str,
        help="JSON string containing the gathered data parameters.",
    )
    parser.add_argument(
        "--file",
        type=str,
        help="Path to a JSON file containing the gathered data parameters.",
    )
    parser.add_argument(
        "--demo",
        choices=["1", "2", "3"],
        help="Run a built-in demonstration scenario for the given phase.",
    )
    parser.add_argument(
        "--calculate-risk",
        nargs=2,
        type=int,
        metavar=("FREQ", "SEV"),
        help="Calculate risk score and tier for FREQUENCY (1-5) and SEVERITY (1-5).",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Optional path to write generated markdown report to file.",
    )

    args = parser.parse_args()

    # Standalone risk calculation mode
    if args.calculate_risk:
        freq, sev = args.calculate_risk
        try:
            res = calculate_risk(freq, sev)
            print(json.dumps(res.to_dict(), indent=2))
            return 0
        except Exception as e:
            print(f"Error calculating risk: {e}", file=sys.stderr)
            return 1

    # Demonstration mode
    if args.demo:
        phase = Phase.normalize(args.demo)
        data = MOCK_SCENARIOS[phase]
        report = generate_report(phase, data)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"Demo report written to {args.output}")
        else:
            print(report)
        return 0

    # Data loading
    data = None
    if args.json:
        try:
            data = json.loads(args.json)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON string: {e}", file=sys.stderr)
            return 1
    elif args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading JSON file {args.file}: {e}", file=sys.stderr)
            return 1

    if data is not None:
        try:
            phase = Phase.normalize(args.phase)
            report = generate_report(phase, data)
            if args.output:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(report)
                print(f"Report written to {args.output}")
            else:
                print(report)
            return 0
        except Exception as e:
            print(f"Error generating report: {e}", file=sys.stderr)
            return 1

    # If no data is supplied, print help
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
