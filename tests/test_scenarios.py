#!/usr/bin/env python3
"""
Scenario-specific automated tests for Phase 1, Phase 2, and Phase 3 workflows.
"""

import json
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.anomaly_helper import (
    Phase,
    RiskTier,
    calculate_risk,
    validate_phase_data,
    generate_report,
    MOCK_SCENARIOS,
)


class TestMockScenarios(unittest.TestCase):
    """Automated tests for Phase 1, Phase 2, and Phase 3 scenario workflows."""

    def test_phase1_network_slowdown_scenario(self):
        """Phase 1 Scenario: A simple UI freeze issue during a network slowdown."""
        data = MOCK_SCENARIOS[Phase.PHASE_1]
        
        # 1. Validate data conforms to Phase 1 schema
        is_valid, errors = validate_phase_data(Phase.PHASE_1, data)
        self.assertTrue(is_valid, f"Phase 1 validation failed: {errors}")
        
        # 2. Check essential scenario parameters
        self.assertIn("UI freeze", data["summary"])
        self.assertIn("throttled to 50 kbps", data["triggering_event"])
        self.assertIn("100% reproducible", data["reproducibility"])

        # 3. Generate and verify report structure
        report = generate_report(Phase.PHASE_1, data)
        self.assertIn("# Core Bug Report", report)
        self.assertIn("Phase 1: Core Triage (Crawl)", report)
        self.assertIn("## 1. Summary", report)
        self.assertIn("## 2. Manifestation", report)
        self.assertIn("## 3. Triggering Event", report)
        self.assertIn("## 4. Steps to Reproduce", report)

    def test_phase2_low_battery_sync_crash_scenario(self):
        """Phase 2 Scenario: Mobile application crash during low-battery mode and active background sync."""
        data = MOCK_SCENARIOS[Phase.PHASE_2]

        # 1. Validate data conforms to Phase 2 schema
        is_valid, errors = validate_phase_data(Phase.PHASE_2, data)
        self.assertTrue(is_valid, f"Phase 2 validation failed: {errors}")

        # 2. Check essential scenario parameters
        self.assertIn("crash", data["summary"].lower())
        self.assertIn("Low-Power Mode", data["pre_anomaly_state"])
        self.assertIn("9%", data["pre_anomaly_state"])
        self.assertIn("25MB sync payload", data["triggering_event"])
        self.assertIn("terminated to the home screen", data["post_anomaly_state"])

        # 3. Generate and verify report structure
        report = generate_report(Phase.PHASE_2, data)
        self.assertIn("# Detailed Technical Anomaly Report", report)
        self.assertIn("Phase 2: Contextual Depth (Walk)", report)
        self.assertIn("## 2. Discovery & Reproduction", report)
        self.assertIn("## 3. System State Transitions", report)
        self.assertIn("Pre-Anomaly State", report)
        self.assertIn("Post-Anomaly State", report)

    def test_phase3_hardware_pairing_thread_violation_scenario(self):
        """
        Phase 3 Scenario: Hardware pairing failure where pairing dialog is blocked
        due to a background thread violation, resulting in a high risk estimation
        (Score >= 16 / Critical Red) and a "Verification Failure" root-cause categorization.
        """
        data = MOCK_SCENARIOS[Phase.PHASE_3]

        # 1. Validate data conforms to Phase 3 schema
        is_valid, errors = validate_phase_data(Phase.PHASE_3, data)
        self.assertTrue(is_valid, f"Phase 3 validation failed: {errors}")

        # 2. Verify Risk Matrix Calculation (4 x 4 = 16 -> Critical Red)
        risk_eval = calculate_risk(data["frequency"], data["severity"])
        self.assertEqual(data["frequency"], 4)
        self.assertEqual(data["severity"], 4)
        self.assertEqual(risk_eval.score, 16)
        self.assertEqual(risk_eval.tier, RiskTier.CRITICAL)
        self.assertEqual(risk_eval.color, "Red")
        self.assertEqual(risk_eval.badge, "[CRITICAL]")

        # 3. Verify Root Cause Categorization
        self.assertIn("Verification Failure", data["root_cause_category"])
        self.assertIn("Main UI Thread", data["root_cause_details"])

        # 4. Generate and verify report structure
        report = generate_report(Phase.PHASE_3, data)
        self.assertIn("# Comprehensive Quality Assurance Report", report)
        self.assertIn("Phase 3: Thought Partner (Run)", report)
        self.assertIn("[CRITICAL] **Critical** (Red)", report)
        self.assertIn("16 / 25", report)
        self.assertIn("## 2. Quantitative Risk Assessment Matrix", report)
        self.assertIn("Verification Failure (Built Wrong)", report)
        self.assertIn("## 6. Corrective & Preventive Actions (CAPA)", report)


if __name__ == "__main__":
    unittest.main()
