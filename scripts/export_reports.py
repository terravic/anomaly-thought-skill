#!/usr/bin/env python3
"""
Batch export utility to generate Markdown reports from mock scenarios or custom JSON.
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.anomaly_helper import Phase, generate_report, MOCK_SCENARIOS


def export_all(output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    for p in [Phase.PHASE_1, Phase.PHASE_2, Phase.PHASE_3]:
        out_file = os.path.join(output_dir, f"{p.value}_report.md")
        content = generate_report(p, MOCK_SCENARIOS[p])
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(content + "\n")
        print(f"Exported {p.value} report to {out_file}")


def main():
    parser = argparse.ArgumentParser(description="Export anomaly reports.")
    parser.add_argument("--output-dir", default="examples/generated_reports", help="Directory to save reports.")
    args = parser.parse_args()
    export_all(args.output_dir)


if __name__ == "__main__":
    main()
