import unittest

from calculator.calculate_savings import calculate


class CalculatorTests(unittest.TestCase):
    def test_archive_scenario_reports_savings(self):
        scenario = {
            "horizon_months": 12,
            "current": {"redshift_gb": 1000, "s3_standard_gb": 0, "monthly_growth_gb": 0},
            "archive": {
                "redshift_gb_to_unload": 1000,
                "s3_archive_gb": 1000,
                "monthly_new_archive_gb": 0,
                "s3_put_requests": 0,
                "s3_get_requests": 0,
                "monthly_retrieval_gb": 0,
                "unload_compute_hours": 0,
                "one_time_migration_usd": 0,
            },
        }
        catalog = {
            "catalog_version": "test",
            "rates": {
                "redshift_storage_per_gb_month": 0.02,
                "s3_standard_per_gb_month": 0.02,
                "s3_glacier_flexible_per_gb_month": 0.004,
                "s3_put_per_1000_requests": 0,
                "s3_get_per_1000_requests": 0,
                "s3_retrieval_per_gb": 0,
                "redshift_unload_compute_per_hour": 0,
            },
        }
        result = calculate(scenario, catalog)
        self.assertEqual(result["current_horizon_usd"], 240.0)
        self.assertEqual(result["archive_horizon_usd"], 48.0)
        self.assertEqual(result["estimated_horizon_savings_usd"], 192.0)

    def test_missing_rate_is_explicit(self):
        with self.assertRaisesRegex(ValueError, "redshift_storage_per_gb_month"):
            calculate({"horizon_months": 1, "current": {}, "archive": {}}, {"rates": {}})


if __name__ == "__main__":
    unittest.main()
