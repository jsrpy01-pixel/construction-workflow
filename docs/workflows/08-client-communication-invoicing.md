# 8. Client Communication & Invoicing

## Purpose
Automatically keep clients informed at each project milestone and generate/send the corresponding invoice, tightening the cash-flow loop.

## Trigger
- **Event:** `milestones.status` updated to `completed` on a project (e.g. "Foundation Complete", "Framing Complete", "Phase 1 Complete").

## Conditions
| # | Condition | Action if false |
|---|---|---|
| 1 | Milestone has an associated billing phase in the contract/payment schedule | Send progress update only, skip invoicing |
| 2 | Milestone photos have been uploaded (from daily site reports or a dedicated milestone photo capture step) | Prompt supervisor for milestone photos before proceeding |
| 3 | No invoice already generated for this milestone | Skip duplicate invoice |

## Actions
1. **Capture Photos & Generate Progress Report** — pull recent site photos (or request new ones), compile a milestone completion report (photos, description, completion date, cumulative % complete).
2. **Send Progress Update to Client** — email/branded client portal notification with the report attached; optionally post to a shared client Slack/Teams channel.
3. **Generate Invoice** — using the contract's payment schedule (e.g. % of contract value per milestone), create an invoice via accounting system (QuickBooks/Xero API) with line items, due date (Net 15/30).
4. **Send Invoice to Client** — email invoice (PDF) with payment link (Stripe/ACH/etc.).
5. **Request Payment / Track** — set reminder follow-ups at day 7 and day 14 if unpaid; on payment received (webhook from accounting/payment processor), mark invoice `paid`, notify PM and Finance.

## Data Flow
```
Site/QA confirms milestone complete
   │
   ▼
milestones.status = completed
   │
   ├─► Photos/Report compiled ──► Client (progress update email/portal)
   │
   └─► Payment Schedule (contract) ──► Accounting System (generate invoice)
                                              │
                                              ▼
                                     Client (invoice + payment link)
                                              │
                              ┌───────────────┴───────────────┐
                              ▼ paid                          ▼ unpaid after 7/14 days
                    PM + Finance notified                Reminder sent to client
```

## n8n Node Mapping
`Postgres/Airtable Trigger (milestone status = completed)` → `IF (photos present)` → `Function (compile report)` → `Send Email (client progress update)` → `HTTP Request (QuickBooks/Xero: create invoice)` → `Send Email (invoice + payment link)` → `Wait/Cron (7/14 day reminder check)` → `Webhook (payment received from Stripe/accounting)` → `IF (paid)` → `Slack/Email (notify PM + Finance)`

## Sample Records
```json
// milestone
{ "milestone_id": "MS-014-03", "project_id": "PRJ-2026-014", "name": "Framing Complete", "status": "completed", "completed_at": "2026-04-15", "billing_pct": 20 }
```
```json
// invoice
{
  "invoice_id": "INV-2026-0231",
  "project_id": "PRJ-2026-014",
  "milestone_id": "MS-014-03",
  "amount": 250000.00,
  "due_date": "2026-04-30",
  "status": "sent",
  "payment_link": "https://pay.example.com/inv/2026-0231"
}
```

Related template: [`docs/templates/client-progress-update.md`](../templates/client-progress-update.md)
