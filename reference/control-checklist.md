# Readiness checklist

## Discovery

- [ ] Dataset register exists and has a business purpose.
- [ ] Source, region, account, data class, size, growth, and access pattern are known.
- [ ] Redshift partitions and S3 prefixes are deterministic.

## Governance

- [ ] Named accountable owner or time-boxed interim owner exists.
- [ ] Retention basis is recorded.
- [ ] Legal hold and exception process exists.
- [ ] Deletion authority and evidence are defined.

## Security

- [ ] Block Public Access is enabled.
- [ ] Encryption and KMS key ownership are documented.
- [ ] Roles use least privilege and access is reviewed.
- [ ] Sensitive-data findings have an owner and remediation path.
- [ ] Audit logging is scoped and retained.

## Reliability

- [ ] Archive manifest, counts, schema, and checksums are validated.
- [ ] Restore runbook exists and has been tested.
- [ ] RPO/RTO are measurable.
- [ ] Key, account, region, and service failure paths are documented.

## Cost

- [ ] Pricing catalog region and date are recorded.
- [ ] Storage, requests, retrieval, restore, and early deletion costs are included.
- [ ] Cost allocation tags and CUR are enabled.
- [ ] Pilot estimate is compared with actual spend.

## Operations

- [ ] Policy is versioned and reviewed as code.
- [ ] Lifecycle changes have a dry run or preview.
- [ ] Metrics and alerts exist for transition, expiry, restore, and tagging failures.
- [ ] Review cadence and policy owner are assigned.
