#!/usr/bin/env python3
"""
Unit and integration tests for scripts/anomaly_helper.py.
"""

import json
import os
import sys
import unittest

# Ensure scripts directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.anomaly_helper import (
    Phase,
    RiskTier,
    RiskEvaluation,
    calculate_risk,
    validate_phase_data,
    format_phase1_report,
    format_phase2_report,
    format_phase3_report,
    generate_report,
    MOCK_SCENARIOS,
)


class TestRiskCalculation(unittest.TestCase):
    """Tests for Risk Score Calculation and Tier Classifications."""

    def test_critical_tier_boundaries(self):
        # 5 x 5 = 25 -> Critical
        res = calculate_risk(5, 5)
        self.assertEqual(res.score, 25)
        self.assertEqual(res.tier, RiskTier.CRITICAL)
        self.assertEqual(res.tier_name, "Critical")
        self.assertEqual(res.color, "Red")
        self.assertEqual(res.badge, "[CRITICAL]")

        # 4 x 4 = 16 -> Critical (Lower boundary for Critical)
        res16 = calculate_risk(4, 4)
        self.assertEqual(res16.score, 16)
        self.assertEqual(res16.tier, RiskTier.CRITICAL)

    def test_high_tier_boundaries(self):
        # 3 x 5 = 15 -> High (Upper boundary for High)
        res15 = calculate_risk(3, 5)
        self.assertEqual(res15.score, 15)
        self.assertEqual(res15.tier, RiskTier.HIGH)
        self.assertEqual(res15.tier_name, "High")
        self.assertEqual(res15.color, "Orange")
        self.assertEqual(res15.badge, "[HIGH]")

        # 2 x 5 = 10 -> High (Lower boundary for High)
        res10 = calculate_risk(2, 5)
        self.assertEqual(res10.score, 10)
        self.assertEqual(res10.tier, RiskTier.HIGH)

    def test_medium_tier_boundaries(self):
        # 3 x 3 = 9 -> Medium (Upper boundary for Medium)
        res9 = calculate_risk(3, 3)
        self.assertEqual(res9.score, 9)
        self.assertEqual(res9.tier, RiskTier.MEDIUM)
        self.assertEqual(res9.tier_name, "Medium")
        self.assertEqual(res9.color, "Yellow")
        self.assertEqual(res9.badge, "[MEDIUM]")

        # 1 x 5 = 5 -> Medium (Lower boundary for Medium)
        res5 = calculate_risk(1, 5)
        self.assertEqual(res5.score, 5)
        self.assertEqual(res5.tier, RiskTier.MEDIUM)

    def test_low_tier_boundaries(self):
        # 2 x 2 = 4 -> Low (Upper boundary for Low)
        res4 = calculate_risk(2, 2)
        self.assertEqual(res4.score, 4)
        self.assertEqual(res4.tier, RiskTier.LOW)
        self.assertEqual(res4.tier_name, "Low")
        self.assertEqual(res4.color, "Green")
        self.assertEqual(res4.badge, "[LOW]")

        # 1 x 1 = 1 -> Low (Minimum possible)
        res1 = calculate_risk(1, 1)
        self.assertEqual(res1.score, 1)
        self.assertEqual(res1.tier, RiskTier.LOW)

    def test_invalid_range_raises_value_error(self):
        with self.assertRaises(ValueError):
            calculate_risk(0, 5)
        with self.assertRaises(ValueError):
            calculate_risk(6, 3)
        with self.assertRaises(ValueError):
            calculate_risk(3, -1)
        with self.assertRaises(ValueError):
            calculate_risk(3, 6)

    def test_invalid_type_raises_type_error(self):
        with self.assertRaises(TypeError):
            calculate_risk("high", 4)
        with self.assertRaises(TypeError):
            calculate_risk(None, 4)

    def test_string_integer_conversion(self):
        res = calculate_risk("4", "4")
        self.assertEqual(res.score, 16)
        self.assertEqual(res.tier, RiskTier.CRITICAL)


class TestPhaseNormalization(unittest.TestCase):
    """Tests for phase normalization."""

    def test_phase_1_aliases(self):
        self.assertEqual(Phase.normalize(1), Phase.PHASE_1)
        self.assertEqual(Phase.normalize("1"), Phase.PHASE_1)
        self.assertEqual(Phase.normalize("crawl"), Phase.PHASE_1)
        self.assertEqual(Phase.normalize("Phase 1"), Phase.PHASE_1)
        self.assertEqual(Phase.normalize("core_triage"), Phase.PHASE_1)

    def test_phase_2_aliases(self):
        self.assertEqual(Phase.normalize(2), Phase.PHASE_2)
        self.assertEqual(Phase.normalize("2"), Phase.PHASE_2)
        self.assertEqual(Phase.normalize("walk"), Phase.PHASE_2)
        self.assertEqual(Phase.normalize("Phase 2"), Phase.PHASE_2)
        self.assertEqual(Phase.normalize("contextual"), Phase.PHASE_2)

    def test_phase_3_aliases(self):
        self.assertEqual(Phase.normalize(3), Phase.PHASE_3)
        self.assertEqual(Phase.normalize("3"), Phase.PHASE_3)
        self.assertEqual(Phase.normalize("run"), Phase.PHASE_3)
        self.assertEqual(Phase.normalize("Phase 3"), Phase.PHASE_3)
        self.assertEqual(Phase.normalize("thought_partner"), Phase.PHASE_3)

    def test_invalid_phase(self):
        with self.assertRaises(ValueError):
            Phase.normalize("invalid_phase")
        with self.assertRaises(ValueError):
            Phase.normalize(4)


class TestDataValidation(unittest.TestCase):
    """Tests for Input Validation across Phases."""

    def test_phase1_valid(self):
        data = {
            "manifestation": "App displays blank white screen on startup",
            "triggering_event": "User taps launch button while offline",
            "reproducibility": "100% reproducible",
        }
        is_valid, errors = validate_phase_data(Phase.PHASE_1, data)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_phase1_missing_and_empty_fields(self):
        # Missing fields
        is_valid, errors = validate_phase_data(Phase.PHASE_1, {})
        self.assertFalse(is_valid)
        self.assertEqual(len(errors), 3)

        # Empty string field
        data = {
            "manifestation": "   ",
            "triggering_event": "Launch",
            "reproducibility": "Always",
        }
        is_valid, errors = validate_phase_data(Phase.PHASE_1, data)
        self.assertFalse(is_valid)
        self.assertTrue(any("manifestation" in err for err in errors))

    def test_phase2_valid(self):
        data = {
            "discovery_method": "Automated regression test suite",
            "pre_anomaly_state": "Memory 500MB, OS 12.0",
            "triggering_event": "Concurrent sync request sent",
            "post_anomaly_state": "Worker thread deadlocks",
            "reproducibility": "Reproducible in 9/10 runs",
        }
        is_valid, errors = validate_phase_data(Phase.PHASE_2, data)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_phase2_missing_field(self):
        data = {
            "discovery_method": "Manual QA",
            "pre_anomaly_state": "Normal",
            # missing triggering_event
            "post_anomaly_state": "Crash",
            "reproducibility": "Always",
        }
        is_valid, errors = validate_phase_data(Phase.PHASE_2, data)
        self.assertFalse(is_valid)
        self.assertTrue(any("triggering_event" in err for err in errors))

    def test_phase3_valid(self):
        data = {
            "core_issue": "Database migration failure on table lock timeout",
            "environment_state": "Pre: 200 open connections. Post: 504 Gateway Timeouts.",
            "frequency": 3,
            "severity": 4,
            "root_cause_category": "Verification Failure",
            "root_cause_details": "Lock timeout was configured to 0 instead of 30s in config file.",
        }
        is_valid, errors = validate_phase_data(Phase.PHASE_3, data)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)

    def test_phase3_invalid_frequency_severity(self):
        data = {
            "core_issue": "Issue",
            "environment_state": "State",
            "frequency": 6,  # Out of range
            "severity": "high",  # Non-integer
            "root_cause_category": "Requirements",
            "root_cause_details": "Details",
        }
        is_valid, errors = validate_phase_data(Phase.PHASE_3, data)
        self.assertFalse(is_valid)
        self.assertTrue(any("frequency" in err for err in errors))
        self.assertTrue(any("severity" in err for err in errors))


class TestReportFormatting(unittest.TestCase):
    """Tests for Markdown Report Generation."""

    def test_phase1_report_structure(self):
        data = MOCK_SCENARIOS[Phase.PHASE_1]
        report = format_phase1_report(data)
        self.assertIn("# Core Bug Report", report)
        self.assertIn("Phase 1: Core Triage (Crawl)", report)
        self.assertIn("## 1. Summary", report)
        self.assertIn("## 2. Manifestation", report)
        self.assertIn("## 3. Triggering Event", report)
        self.assertIn("## 4. Steps to Reproduce", report)
        self.assertIn(data["manifestation"], report)

    def test_phase2_report_structure(self):
        data = MOCK_SCENARIOS[Phase.PHASE_2]
        report = format_phase2_report(data)
        self.assertIn("# Detailed Technical Anomaly Report", report)
        self.assertIn("Phase 2: Contextual Depth (Walk)", report)
        self.assertIn("## 1. Executive Summary", report)
        self.assertIn("## 2. Discovery & Reproduction", report)
        self.assertIn("## 3. System State Transitions", report)
        self.assertIn("Pre-Anomaly State", report)
        self.assertIn("Post-Anomaly State", report)
        self.assertIn(data["discovery_method"], report)

    def test_phase3_report_structure(self):
        data = MOCK_SCENARIOS[Phase.PHASE_3]
        report = format_phase3_report(data)
        self.assertIn("# Comprehensive Quality Assurance Report", report)
        self.assertIn("Phase 3: Thought Partner (Run)", report)
        self.assertIn("[CRITICAL] **Critical** (Red)", report)
        self.assertIn("16 / 25", report)
        self.assertIn("## 2. Quantitative Risk Assessment Matrix", report)
        self.assertIn("## 5. Retrospective Root-Cause Categorization", report)
        self.assertIn("Verification Failure (Built Wrong)", report)
        self.assertIn("## 6. Corrective & Preventive Actions (CAPA)", report)

    def test_generate_report_dispatcher(self):
        report1 = generate_report("1", MOCK_SCENARIOS[Phase.PHASE_1])
        self.assertIn("# Core Bug Report", report1)

        report2 = generate_report(2, MOCK_SCENARIOS[Phase.PHASE_2])
        self.assertIn("# Detailed Technical Anomaly Report", report2)

        report3 = generate_report("run", MOCK_SCENARIOS[Phase.PHASE_3])
        self.assertIn("# Comprehensive Quality Assurance Report", report3)

    def test_generate_report_validation_failure(self):
        with self.assertRaises(ValueError) as ctx:
            generate_report(1, {})
        self.assertIn("Validation failed", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
