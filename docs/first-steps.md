# First steps: a safe archival journey

## Days 1–5: establish facts

Create a dataset register with one row per logical dataset or Redshift table:

| Field | Example |
| --- | --- |
| Dataset and source | `orders`, Redshift `analytics` cluster |
| Business purpose | Financial reporting |
| Data class | Confidential / regulated / public |
| Time grain | Daily partition by `order_date` |
| Current size and growth | 18 TB, 250 GB/month |
| Reads in last 90 days | 4 ad-hoc restores |
| RPO / RTO | RPO 24h, RTO 8h |
| Required retention | 7 years |
| Deletion trigger | 7 years after fiscal close |
| Account, region, residency | Production, `eu-west-1`, EU |
| Business owner / technical steward | Named person or `UNASSIGNED` |

Do not begin by choosing Glacier. A storage class is the result of the data and recovery assessment.

## Days 6–10: classify and decide

Assign each dataset a retention class such as `hot-90d`, `warm-12m`, `compliance-7y`, or `ephemeral-30d`. For each class, record:

- active and archive transition points;
- minimum storage duration and expected retrieval pattern;
- encryption and access boundary;
- legal hold behavior;
- deletion approval and evidence;
- restore test frequency.

Use the example policy as a contract between platform, security, legal, finance, and the data owner.

## Days 11–20: run a bounded pilot

Choose one partitioned, non-critical dataset with a measurable read pattern. The pilot should:

1. export or inventory the source;
2. apply tags and ownership metadata;
3. write an S3 lifecycle rule in a non-production bucket;
4. unload an old Redshift partition to an immutable, encrypted S3 prefix;
5. verify checksums, row counts, partition metadata, and permissions;
6. perform a restore into an isolated location;
7. measure elapsed time, retrieval bytes, requests, and actual spend;
8. exercise an exception or legal hold;
9. approve or reject expiration.

## Days 21–30: decide whether to scale

Scale only if the pilot has evidence for:

- successful restore within the agreed RTO;
- no unauthorised access;
- policy and owner metadata present;
- lifecycle rule behavior understood;
- deletion and legal hold behavior tested;
- forecast savings remain positive after retrieval and operations;
- an on-call team knows how to recover the data.

## The first decision record

Capture the outcome in a short decision record:

- decision and scope;
- options considered;
- assumptions and pricing catalog version;
- risks and mitigations;
- approvers;
- review date;
- rollback and restore procedure.

This record is more valuable than a large one-time migration plan because retention policies change.
