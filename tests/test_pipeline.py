import json
from pathlib import Path

import pandas as pd

from src.report import generate_report, save_report, build_failure_breakdown


def test_generate_report():
    report = generate_report(
        total=100,
        passed=80,
        failed=20,
        failures={"DUPLICATE_TRANSACTION": 10, "INVALID_AMOUNT": 10},
    )

    assert report["processed_records"] == 100
    assert report["passed_records"] == 80
    assert report["failed_records"] == 20
    assert report["failure_breakdown"]["DUPLICATE_TRANSACTION"] == 10


def test_save_report(tmp_path):
    report = generate_report(
        total=100,
        passed=80,
        failed=20,
        failures={"DUPLICATE_TRANSACTION": 20},
    )

    output_path = tmp_path / "summary_report.json"
    save_report(report, str(output_path))

    with open(output_path) as f:
        loaded = json.load(f)

    assert loaded == report


def test_build_failure_breakdown():
    invalid_df = pd.DataFrame({
        "transaction_id": ["TX001", "TX002", "TX003"],
        "failure_reason": ["DUPLICATE_TRANSACTION", "INVALID_AMOUNT", "DUPLICATE_TRANSACTION"],
    })

    breakdown = build_failure_breakdown(invalid_df)

    assert breakdown["DUPLICATE_TRANSACTION"] == 2
    assert breakdown["INVALID_AMOUNT"] == 1
