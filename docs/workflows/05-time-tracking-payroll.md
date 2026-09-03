# 5. Worker Time Tracking & Payroll

## Purpose
Capture accurate clock-in/out data per worker per project via a mobile app, and automatically produce a weekly payroll report routed for approval.

## Trigger
- **Event-based:** Worker taps "Clock In"/"Clock Out" in mobile app → webhook fired with `worker_id`, `project_id`, `timestamp`, `gps_location` (optional geofence validation).
- **Scheduled:** Cron every **Friday 18:00** (or Monday 06:00 for prior week) to run payroll calculation.

## Conditions
| # | Condition | Action if false |
|---|---|---|
| 1 | (Clock event) Worker is assigned to the project they're clocking into | Reject event, notify worker |
| 2 | (Clock event) GPS within geofence radius of site (if enabled) | Flag entry for manual review |
| 3 | (Payroll run) All active workers have paired clock-in/out for the week | Flag missing pairs for supervisor confirmation before finalizing |

## Actions — Clock Events
1. **Record Time Entry** — append row to `time_entries` table: `worker_id`, `project_id`, `type` (in/out), `timestamp`, `location`.
2. **Real-time Validation** — if clock-out without matching clock-in (or vice versa), flag `anomaly = true` for supervisor review.

## Actions — Weekly Payroll Run
1. **Calculate Hours per Project** — sum paired in/out intervals per worker per project for the week (Mon–Sun), including overtime rules (>40 hrs/week = 1.5x).
2. **Apply Pay Rates** — join with `workers` table (`hourly_rate`, `role`) to compute `regular_pay`, `overtime_pay`, `total_pay`.
3. **Generate Payroll Report** — compile per-project and per-worker breakdown into a spreadsheet/PDF.
4. **Send for Approval** — route report to Project Manager / Payroll Admin for sign-off (approve/reject with comments) via email or Slack approval workflow.
5. **On Approval** — push finalized payroll to accounting/payroll system (e.g. Gusto, QuickBooks, ADP) for disbursement; archive report.
6. **On Rejection** — return to payroll admin with comments for correction, re-run calculation.

## Data Flow
```
Mobile App (clock in/out)
   │
   ▼
time_entries DB  ◄── geofence/assignment validation
   │
   ▼ (Fri 18:00 cron)
Payroll Calculation (Function/Code node)
   │
   ▼
Payroll Report (per project/worker) ──► PM/Payroll Admin (approval request)
                                              │
                       ┌──────────────────────┴─────────────────────┐
                       ▼ approved                                    ▼ rejected
              Accounting/Payroll System (push)              Back to Payroll Admin (revise)
```

## n8n Node Mapping
`Webhook (mobile clock event)` → `IF (assignment/geofence check)` → `Postgres (insert time_entries)`
Weekly: `Cron (Fri 18:00)` → `Postgres (query week's entries)` → `Function (pair in/out, compute hours & OT)` → `Postgres/Airtable (join worker rates)` → `Function (build report)` → `Google Sheets (write report)` → `Send Email/Slack (approval request with Approve/Reject buttons or form)` → `Webhook (approval response)` → `IF (approved)` → `HTTP Request (push to payroll API)`

## Sample Records
```json
// time_entries
{ "entry_id": "TE-88231", "worker_id": "W-014", "project_id": "PRJ-2026-014", "type": "in", "timestamp": "2026-03-02T06:58:00Z", "location": {"lat": 39.79, "lng": -89.65} }
```
```json
// payroll_reports (line item)
{
  "worker_id": "W-014",
  "project_id": "PRJ-2026-014",
  "week_ending": "2026-03-08",
  "regular_hours": 40,
  "overtime_hours": 4.5,
  "hourly_rate": 28.00,
  "regular_pay": 1120.00,
  "overtime_pay": 189.00,
  "total_pay": 1309.00
}
```

Related template: [`docs/templates/payroll-approval-request.md`](../templates/payroll-approval-request.md)
