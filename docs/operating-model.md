# Enterprise operating model

## Required controls

### Preventive

- Policy changes are pull requests with peer review and owner approval.
- Lifecycle selectors require `dataset-id`, `retention-class`, `owner-id`, `classification`, and `legal-hold` metadata.
- Production archive writes use encryption, private networking where required, least-privilege roles, and blocked public access.
- Expiry is disabled for `owner-status: unassigned`, `legal-hold: true`, and active exceptions.

### Detective

- Inventory and lifecycle reports are reviewed monthly.
- CloudTrail data events, S3 access logs, KMS events, and Redshift audit logs are retained according to the evidence policy.
- Cost and Usage Reports are compared with the estimate and tagged to a cost center.
- Restore tests record object counts, checksums, elapsed time, bytes retrieved, and outcome.

### Corrective

- A failed restore opens an incident and blocks the affected policy class from expansion.
- A selector or tagging defect pauses lifecycle changes and identifies affected objects.
- A legal hold is applied immediately and expiry candidates are re-evaluated.
- KMS, account, or region failures use a documented alternate recovery path.

## Lifecycle review cadence

| Cadence | Review |
| --- | --- |
| Per change | Scope, owner, classification, selector, tests, rollback |
| Monthly | Cost, access, failed transitions, unassigned datasets |
| Quarterly | Restore test, retention exceptions, key/access review |
| Annually | Legal/policy basis, storage class assumptions, architecture and RTO |

## Metrics

- percentage of archive bytes with an accountable owner;
- percentage of objects with required tags;
- lifecycle transition and expiration success rate;
- restore success rate and p95 restore duration;
- archive read frequency and retrieval bytes;
- forecast versus realised monthly cost;
- age and count of retention exceptions;
- deletion evidence completeness.

## Evidence package

For each policy class, retain:

- approved policy version and effective date;
- inventory snapshot and matching rule;
- lifecycle configuration;
- owner and legal-hold decision;
- archive manifest and validation output;
- restore test result;
- deletion approval and completion evidence.
