# AWS service selection

| Need | Good starting point | Watch-outs |
| --- | --- | --- |
| Object archive and lifecycle | Amazon S3 Lifecycle | Minimum storage duration, retrieval, early deletion, versioned objects |
| Very infrequent long-term archive | S3 Glacier Flexible Retrieval / Deep Archive | Restore delay, retrieval fees, legal hold and Object Lock design |
| Query old data without moving it back | S3 + Glue Data Catalog + Athena | Query and scan costs, schema evolution, partition quality |
| Active warehouse history | Redshift tables and partitions | Cluster/storage cost and vacuum/maintenance behavior |
| Export Redshift history | Redshift UNLOAD to S3 | Manifest, encryption, consistency, schema and count validation |
| Cluster recovery | Redshift snapshots / automated snapshots | Not a substitute for a business archive or retention policy |
| Immutable records | S3 Object Lock | Governance/compliance mode is hard to undo; validate retention mode |
| Discovery and classification | Amazon Macie and data inventory | Findings need owner action; discovery is not a retention decision |
| Audit evidence | CloudTrail, S3 data events, Redshift audit logging | Data events can add cost and must be scoped deliberately |
| Cost attribution | Cost Allocation Tags, CUR, Cost Explorer | Tags and CUR dimensions must be enabled before the pilot |

## Storage classes in plain language

- **S3 Standard:** frequent access and low latency.
- **S3 Standard-IA:** infrequent access with retrieval fees and a minimum duration.
- **S3 Glacier Instant Retrieval:** archive economics with millisecond access for suitable objects.
- **S3 Glacier Flexible Retrieval:** minutes-to-hours restore options.
- **S3 Glacier Deep Archive:** lowest storage price for data rarely retrieved; longest restore expectations.

Confirm current names, availability, minimums, and prices in the AWS documentation for the selected region.
