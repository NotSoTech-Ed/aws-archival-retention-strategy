# Ownership when no data owner is defined

An absent owner is a governance finding, not permission to archive or delete. Until accountability is assigned, use a conservative default:

1. **Quarantine the decision.** Mark the dataset `owner-status: unassigned` and exclude it from automated expiration.
2. **Name an accountable interim role.** The platform or service owner may approve access and a pilot, but must not silently invent the business retention requirement.
3. **Triangulate evidence.** Ask the application team, finance, privacy/legal, security, and records-management teams who relies on the data and why it exists.
4. **Open an ownership ticket.** Include the dataset, source system, classification, usage, risk, proposed interim retention, and a due date.
5. **Escalate by risk.** Regulated, sensitive, or business-critical data goes to the data governance council or risk owner; low-risk data can use a time-boxed interim class.
6. **Set an expiry on the exception, not the data.** Re-review the ownership exception in 30–90 days.
7. **Record the decision.** A named role, not a team alias, must accept retention and deletion accountability.

## Minimum decision record

```yaml
dataset: finance/orders
owner_status: unassigned
interim_accountable_role: data-platform-service-owner
business_representatives:
  - finance-controls
  - privacy-office
classification: confidential
proposed_interim_retention_days: 365
automatic_expiry_allowed: false
exception_expires_on: 2026-12-31
decision_ticket: GOV-0000
```

## RACI starter

| Activity | Accountable | Responsible | Consulted |
| --- | --- | --- | --- |
| Define business retention | Data owner | Records manager | Legal, privacy |
| Implement lifecycle | Platform owner | Cloud engineering | Security, data owner |
| Approve deletion | Data owner / records authority | Platform owner | Legal, privacy |
| Restore archive | Data owner | Platform/on-call | Security |
| Review cost | FinOps owner | Platform owner | Data owner |
