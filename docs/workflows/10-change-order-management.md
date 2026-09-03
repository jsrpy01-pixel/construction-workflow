# 10. Change Order Management

## Purpose
Give clients a structured, transparent way to request scope changes, and ensure cost/time impacts are reviewed and approved before the project scope or budget changes.

## Trigger
- **Event:** Client submits a change request (via client portal form, email parsed into a form, or PM manually logs a verbal request).

## Conditions
| # | Condition | Action if false |
|---|---|---|
| 1 | Required fields present (`description`, `requested_by`, `project_id`) | Return to client for more detail |
| 2 | PM has completed cost/time estimate within SLA (e.g. 3 business days) | Send reminder to PM |
| 3 | Client responds to approval request within SLA (e.g. 5 business days) | Send reminder; mark `expired` after 2 reminders |

## Actions
1. **Create Change Order Form** — generate a `change_orders` record: `co_id` (`CO-{YYYY}-{sequence}`), linked `project_id`, description, requested_by, date requested, `status = submitted`.
2. **PM Review & Estimate** — notify Project Manager to review; PM fills in estimated `cost_impact`, `schedule_impact_days`, `justification`; sets `status = estimated`.
3. **Send to Client for Approval** — generate a formal Change Order document (PDF) with cost/time impact and send to client with an approve/reject e-signature link (DocuSign/HelloSign or simple approve-button webhook).
4. **On Approval:**
   - Update project `scope` (append change description to scope document).
   - Update project `budget` (add `cost_impact` to `approved_budget`).
   - Update project `schedule` (extend `end_date` by `schedule_impact_days` if applicable).
   - Set `status = approved`.
   - **Notify Relevant Teams** — procurement (if new materials needed), site supervisor (if new scope of work), accounting (budget change), client (confirmation).
5. **On Rejection** — set `status = rejected`, notify PM and client, archive with reason.
6. **On Expiry** — set `status = expired` after SLA reminders exhausted, notify PM to follow up manually.

## Data Flow
```
Client submits change request
   │
   ▼
change_orders DB (status = submitted) ──► PM notified
   │
   ▼ (PM estimates cost/time)
status = estimated ──► Change Order PDF ──► Client (approve/reject link)
   │
   ├─► Approved ──► Update: scope, budget, schedule ──► Notify: procurement, supervisor, accounting, client
   │
   ├─► Rejected ──► Notify PM + Client, archive
   │
   └─► Expired (no response) ──► Notify PM to follow up
```

## n8n Node Mapping
`Webhook/Form (client change request)` → `Postgres (insert change_order, status=submitted)` → `Send Email (notify PM)` → `Webhook (PM submits estimate)` → `Postgres (update status=estimated)` → `Function (generate CO PDF)` → `Send Email/DocuSign (client approval request)` → `Webhook (client decision)` → `IF (approved)` → `Postgres (update project scope/budget/schedule)` → `Slack/Email (notify procurement, supervisor, accounting, client)`; `IF (rejected)` → `Send Email (notify PM + client)`; `Cron (SLA reminder check)` → `IF (overdue)` → `Send Email (reminder/escalate)`

## Sample Records
```json
{
  "co_id": "CO-2026-0012",
  "project_id": "PRJ-2026-014",
  "requested_by": "client_contact@acme.com",
  "description": "Add rooftop solar panel conduit runs",
  "date_requested": "2026-04-01",
  "cost_impact": 18500.00,
  "schedule_impact_days": 4,
  "status": "approved",
  "approved_at": "2026-04-09"
}
```

Related template: [`docs/templates/change-order-form.md`](../templates/change-order-form.md)
