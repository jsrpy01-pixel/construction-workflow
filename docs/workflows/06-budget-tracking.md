# 6. Budget Tracking & Cost Alerts

## Purpose
Continuously track actual spend against budget across materials, labor, and equipment rental, alerting the Project Manager before overruns happen, and producing a monthly cost report.

## Trigger
- **Event-based:** New expense recorded (`expenses` table insert) — sourced from approved POs (materials), payroll runs (labor), and equipment rental invoices.
- **Scheduled:** Cron on the **1st of every month at 08:00** for the monthly report.

## Conditions
| # | Condition | Action if false |
|---|---|---|
| 1 | `total_spent / budget >= 0.80` for a project (after new expense) | No alert |
| 2 | Alert not already sent for this threshold band this month (avoid alert spam) | Skip duplicate alert |
| 3 | `total_spent / budget >= 1.00` (over budget) | Send elevated/critical alert instead of standard |

## Actions — Real-time Expense Tracking
1. **Record Expense** — insert into `expenses` table with `category` (materials/labor/equipment), `amount`, `project_id`, `source_ref` (PO ID / payroll ID / rental invoice ID).
2. **Recalculate Spend** — update `projects.total_spent` (sum of all expense categories) and `budget_utilization_pct`.
3. **Threshold Check** — if utilization crosses 80% → send alert to Project Manager (email + Slack) with category breakdown and remaining budget; if crosses 100% → escalate to PM + Finance Director as critical.

## Actions — Monthly Cost Report
1. **Aggregate Expenses** — group by project and category for the prior calendar month.
2. **Compute Variance** — actual vs. planned budget burn rate (based on % project complete vs. % budget spent).
3. **Generate Report** — spreadsheet/PDF with per-project summary, top cost drivers, forecast to completion.
4. **Distribute** — email to Finance, Project Managers, and Executive team; archive to `Reports/Monthly Cost/{YYYY-MM}` folder.

## Data Flow
```
PO delivered (materials) ──┐
Payroll finalized (labor) ─┼──► expenses DB ──► Recalculate project.total_spent
Equipment rental invoice ──┘                            │
                                                          ▼
                                           IF utilization >= 80% ──► PM Alert (email/Slack)
                                           IF utilization >= 100% ──► Critical Alert (PM + Finance)

Cron (1st of month) ──► Aggregate expenses DB ──► Monthly Cost Report ──► Finance/PM/Exec + Archive
```

## n8n Node Mapping
`Postgres Trigger (expenses insert)` → `Function (recalc total_spent & pct)` → `Postgres (update project)` → `IF (>=80% and not yet alerted)` → `Send Email/Slack (PM alert)` → `IF (>=100%)` → `Send Email/Slack (critical, Finance Director)`
Monthly: `Cron` → `Postgres (aggregate GROUP BY project, category)` → `Function (variance calc)` → `Google Sheets/PDF (report)` → `Send Email (distribution list)` → `Google Drive (archive)`

## Sample Records
```json
// expenses
{ "expense_id": "EXP-33921", "project_id": "PRJ-2026-014", "category": "materials", "amount": 4375.00, "source_ref": "PO-2026-0087", "date": "2026-03-06" }
```
```json
// budget alert payload
{
  "project_id": "PRJ-2026-014",
  "budget": 1250000,
  "total_spent": 1005000,
  "utilization_pct": 80.4,
  "breakdown": { "materials": 512000, "labor": 410000, "equipment": 83000 },
  "alert_level": "warning"
}
```

Related template: [`docs/templates/monthly-cost-report.md`](../templates/monthly-cost-report.md)
