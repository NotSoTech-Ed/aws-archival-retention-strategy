# AWS Archival & Retention Strategy

An opinionated, vendor-aware starting point for designing **data archival, retention, and deletion** on AWS for Amazon S3 and Amazon Redshift.

This repository is written for two audiences:

- a decision-maker who needs a safe first conversation about retention;
- an engineer who needs patterns, policy examples, controls, and a cost estimate to start a proof of concept.

It is a reference implementation, not a production deployment. AWS prices, service capabilities, legal obligations, and organisational policies must be validated before rollout.

## The short version

1. **Inventory data before moving it.** Record the source, business purpose, owner, classification, residency, legal hold status, and recovery objective.
2. **Assign a retention class.** Do not use “keep everything” as a policy. Define when data becomes inactive, when it may be archived, and when it must be deleted.
3. **Choose the lowest operationally safe tier.** S3 lifecycle transitions are usually the simplest archive mechanism. Redshift data that is still queried should remain queryable; unload historical partitions to S3 before considering deletion.
4. **Make deletion as deliberate as archival.** Expiry, legal holds, approvals, evidence, and restore testing belong in the same design.
5. **Prove recovery and cost.** A cheaper tier is not a saving if retrieval latency, retrieval fees, or rehydration time breaks the business process.

## What is in this repository?

| Path | Purpose |
| --- | --- |
| [`docs/architecture.md`](docs/architecture.md) | Reference architecture and end-to-end flow |
| [`docs/first-steps.md`](docs/first-steps.md) | A practical 30-day discovery and pilot plan |
| [`docs/ownership-and-governance.md`](docs/ownership-and-governance.md) | How to proceed when a data owner is missing |
| [`docs/operating-model.md`](docs/operating-model.md) | Controls, evidence, exceptions, and operating cadence |
| [`diagrams/archival-flow.mmd`](diagrams/archival-flow.mmd) | Mermaid flow diagram for workshops |
| [`policies/retention-policy.example.yml`](policies/retention-policy.example.yml) | Plug-and-play organisation policy shape |
| [`policies/retention-policy.schema.json`](policies/retention-policy.schema.json) | JSON Schema for validating policy files |
| [`calculator/`](calculator/) | Offline S3 + Redshift monthly savings estimator |
| [`reference/aws-services.md`](reference/aws-services.md) | Service selection and limitations |
| [`reference/control-checklist.md`](reference/control-checklist.md) | Design and readiness checklist |
| [`reference/glossary.md`](reference/glossary.md) | Plain-language terminology |

## Run the savings calculator

The calculator uses no third-party packages. It reads a JSON scenario, uses the rates in a versioned catalog, and prints a cost comparison plus retrieval exposure:

```bash
python3 calculator/calculate_savings.py \
  --scenario calculator/example-scenario.json \
  --catalog calculator/pricing_catalog.json
```

The output is an estimate, not an AWS bill. Update the catalog from the AWS Pricing pages for the account's region, storage class, redundancy choice, and commercial agreement. See [`calculator/README.md`](calculator/README.md) for assumptions and interpretation.

## Suggested workshop order

Use these questions in order:

1. What data do we have, and which workloads actually read it?
2. What is the consequence of losing, exposing, or deleting it?
3. Who is accountable for the business purpose and deletion decision?
4. What retention period is required by policy, contract, or law?
5. How quickly must archived data be recoverable, and how often will it be retrieved?
6. What evidence proves that lifecycle rules, legal holds, and deletion controls worked?
7. What is the measured cost before and after the pilot?

Start with one bounded dataset and one retention class. Expand only after restore, deletion, security, and cost evidence are accepted.

## Important guardrails

- Never apply a lifecycle rule to a production bucket without a dry-run inventory and an owner-approved change.
- S3 lifecycle expiration and Redshift deletion can be irreversible. Versioning, Object Lock, snapshots, backups, and legal holds solve different problems; they are not interchangeable.
- Glacier and Deep Archive are not “free S3.” Retrieval cost, minimum storage duration, early deletion charges, request costs, and restore time matter.
- Retention is not a security control by itself. Use least privilege, encryption, logging, sensitive-data discovery, and access reviews as separate controls.
- Keep customer-managed pricing inputs and policy exceptions under change control.

## License and use

The material is intended as an internal design accelerator. Validate it with your security, privacy, legal, finance, data-platform, and AWS account teams before use.
