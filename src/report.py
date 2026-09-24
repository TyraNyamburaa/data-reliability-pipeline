import json
from pathlib import Path
from collections import Counter


def generate_report(total, passed, failed, failures):

    report = {
        "processed_records": total,
        "passed_records": passed,
        "failed_records": failed,
        "failure_breakdown": failures
    }

    return report


def save_report(report, output_path):
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w") as f:
        json.dump(report, f, indent=2)

    return report


def build_failure_breakdown(invalid_df):
    if invalid_df.empty:
        return {}

    counts = invalid_df["failure_reason"].value_counts()

    return counts.to_dict()
