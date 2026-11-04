import json
import logging
from pathlib import Path
from typing import Dict

import pandas as pd


def generate_report(
    total: int,
    passed: int,
    failed: int,
    failures: Dict[str, int],
) -> dict:
    report = {
        "processed_records": total,
        "passed_records": passed,
        "failed_records": failed,
        "failure_breakdown": failures,
    }
    return report


def build_failure_breakdown(invalid_df: pd.DataFrame) -> Dict[str, int]:
    if invalid_df.empty:
        return {}

    counts = invalid_df["failure_reason"].value_counts()
    return counts.to_dict()


def save_report(report: dict, output_path: str) -> dict:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        json.dump(report, f, indent=2)

    logging.info(f"Saved quality report to {output_path}")
    return report


def generate_quality_report(
    valid_df: pd.DataFrame,
    invalid_df: pd.DataFrame,
    output_path: str,
) -> dict:
    failure_breakdown = build_failure_breakdown(invalid_df)

    report = generate_report(
        total=len(valid_df) + len(invalid_df),
        passed=len(valid_df),
        failed=len(invalid_df),
        failures=failure_breakdown,
    )

    return save_report(report, output_path)
