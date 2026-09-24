# Archival savings calculator

This offline calculator compares a current monthly storage estimate with an archived S3 plus Redshift export estimate. It also reports retrieval exposure so a lower storage line item is not mistaken for guaranteed savings.

## Inputs

The scenario contains:

- region and source sizes;
- current Redshift storage price and S3 storage price;
- archive storage class price;
- monthly growth and archive age;
- request counts, retrieval volume, and Redshift UNLOAD compute hours;
- one-time migration cost.

All prices are **USD per GB-month**, **USD per 1,000 requests**, **USD per GB retrieved**, or **USD per compute hour**, as labelled. Decimal GB is used. The catalog is illustrative and must be replaced with current AWS prices.

```bash
python3 calculator/calculate_savings.py \
  --scenario calculator/example-scenario.json \
  --catalog calculator/pricing_catalog.json
```

The command exits non-zero for invalid inputs and prints JSON suitable for a ticket or spreadsheet import.

## Model boundaries

Included: storage, S3 requests, retrieval, export compute, and one-time migration amortised over the requested horizon.

Not included by default: taxes, negotiated discounts, NAT Gateway/data-transfer charges, KMS request charges, Glue/Athena query charges, Redshift Serverless/RPU differences, backup/snapshot charges, support, and staff time. Add these separately when they are material.

The result is an estimate and not a commitment. Use the AWS Pricing Calculator and account Cost and Usage Report for a decision.
