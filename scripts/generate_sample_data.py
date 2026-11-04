#!/usr/bin/env python3
"""
Generate sample transaction data for testing the pipeline.
"""

import csv
import os
from datetime import datetime, timedelta
from pathlib import Path
import random


def generate_sample_data(num_records=20, output_dir="data/raw"):
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    headers = [
        "transaction_id",
        "customer_id",
        "agent_id",
        "region",
        "transaction_date",
        "amount",
        "currency",
        "status",
        "payment_method",
    ]

    output_file = Path(output_dir) / "transactions_sample.csv"

    regions = ["Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret"]
    currencies = ["KES", "USD"]
    statuses = ["success", "pending", "failed", "completed"]
    payment_methods = ["Mpesa", "mobile_money", "card"]

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for i in range(num_records):
            writer.writerow({
                "transaction_id": f"TX{i + 1000:05d}",
                "customer_id": f"C{random.randint(100, 999)}",
                "agent_id": f"A{random.randint(10, 99)}",
                "region": random.choice(regions),
                "transaction_date": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d"),
                "amount": round(random.uniform(10, 10000), 2),
                "currency": "KES",
                "status": random.choice(statuses),
                "payment_method": random.choice(payment_methods),
            })

    print(f"Generated {num_records} sample records in {output_file}")


if __name__ == "__main__":
    generate_sample_data()
