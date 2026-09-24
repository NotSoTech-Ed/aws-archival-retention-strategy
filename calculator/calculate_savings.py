#!/usr/bin/env python3
"""Estimate monthly and horizon savings for an S3/Redshift archive design.

The pricing catalog is deliberately external and versioned. This keeps the
calculation reproducible while making regional price updates explicit.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as handle:
            value = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Could not read JSON file {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def number(data: dict[str, Any], key: str, *, minimum: float = 0.0) -> float:
    value = data.get(key)
    if not isinstance(value, (int, float)) or isinstance(value, bool) or value < minimum:
        raise ValueError(f"{key} must be a number >= {minimum}")
    return float(value)


def calculate(scenario: dict[str, Any], catalog: dict[str, Any]) -> dict[str, Any]:
    horizon = int(number(scenario, "horizon_months", minimum=1))
    current = scenario.get("current")
    archive = scenario.get("archive")
    rates = catalog.get("rates")
    if not all(isinstance(section, dict) for section in (current, archive, rates)):
        raise ValueError("scenario.current, scenario.archive, and catalog.rates are required objects")

    required_rates = (
        "redshift_storage_per_gb_month",
        "s3_standard_per_gb_month",
        "s3_glacier_flexible_per_gb_month",
        "s3_put_per_1000_requests",
        "s3_get_per_1000_requests",
        "s3_retrieval_per_gb",
        "redshift_unload_compute_per_hour",
    )
    prices = {key: number(rates, key) for key in required_rates}
    current_gb = number(current, "redshift_gb") + number(current, "s3_standard_gb")
    growth = number(current, "monthly_growth_gb")
    unload_gb = number(archive, "redshift_gb_to_unload")
    if unload_gb > number(current, "redshift_gb"):
        raise ValueError("archive.redshift_gb_to_unload cannot exceed current.redshift_gb")
    active_redshift_gb = number(current, "redshift_gb") - unload_gb
    archive_gb = number(archive, "s3_archive_gb")
    archive_growth = number(archive, "monthly_new_archive_gb")
    active_growth = max(growth - archive_growth, 0.0)

    current_monthly = current_gb * prices["redshift_storage_per_gb_month"]
    archive_monthly = (
        (active_redshift_gb + number(current, "s3_standard_gb")) * prices["redshift_storage_per_gb_month"]
        + archive_gb * prices["s3_glacier_flexible_per_gb_month"]
        + number(archive, "s3_put_requests") / 1000 * prices["s3_put_per_1000_requests"]
        + number(archive, "s3_get_requests") / 1000 * prices["s3_get_per_1000_requests"]
        + number(archive, "monthly_retrieval_gb") * prices["s3_retrieval_per_gb"]
        + number(archive, "unload_compute_hours") * prices["redshift_unload_compute_per_hour"]
    )
    monthly_migration = (
        number(archive, "one_time_migration_usd") / horizon
        + (archive_growth * prices["s3_glacier_flexible_per_gb_month"])
    )
    current_horizon = sum(
        (current_gb + month * growth) * prices["redshift_storage_per_gb_month"]
        for month in range(horizon)
    )
    archive_horizon = sum(
        (active_redshift_gb + number(current, "s3_standard_gb") + month * active_growth)
        * prices["redshift_storage_per_gb_month"]
        + (archive_gb + month * archive_growth) * prices["s3_glacier_flexible_per_gb_month"]
        + number(archive, "s3_put_requests") / 1000 * prices["s3_put_per_1000_requests"]
        + number(archive, "s3_get_requests") / 1000 * prices["s3_get_per_1000_requests"]
        + number(archive, "monthly_retrieval_gb") * prices["s3_retrieval_per_gb"]
        + number(archive, "unload_compute_hours") * prices["redshift_unload_compute_per_hour"]
        for month in range(horizon)
    ) + number(archive, "one_time_migration_usd")
    savings = current_horizon - archive_horizon
    return {
        "catalog_version": catalog.get("catalog_version", "unspecified"),
        "horizon_months": horizon,
        "current_monthly_usd": round(current_monthly, 2),
        "archive_monthly_usd_before_migration": round(archive_monthly + monthly_migration, 2),
        "archive_monthly_retrieval_exposure_usd": round(
            number(archive, "monthly_retrieval_gb") * prices["s3_retrieval_per_gb"], 2
        ),
        "current_horizon_usd": round(current_horizon, 2),
        "archive_horizon_usd": round(archive_horizon, 2),
        "estimated_horizon_savings_usd": round(savings, 2),
        "estimated_horizon_savings_percent": round((savings / current_horizon * 100) if current_horizon else 0, 2),
        "assumptions": [
            "Decimal GB and USD rates from the supplied catalog.",
            "Archive growth is charged for each month in the horizon.",
            "Excluded services and discounts are listed in calculator/README.md.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", type=Path, required=True)
    parser.add_argument("--catalog", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = calculate(load_json(args.scenario), load_json(args.catalog))
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
