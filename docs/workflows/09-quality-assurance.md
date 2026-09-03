# 9. Quality Assurance Inspection

## Purpose
Guarantee every work phase is inspected before the project moves forward, with a clear correction loop for failed inspections.

## Trigger
- **Event:** `phases.status` updated to `work_complete` on a project (supervisor marks a work phase as physically finished).

## Conditions
| # | Condition | Action if false |
|---|---|---|
| 1 | Inspector available for the trade/phase type | Queue and notify scheduling coordinator |
| 2 | Inspection checklist result contains any "Fail"/"Issue" item | Route to "approved" path |
| 3 | Correction task previously created and resolved for this phase | Re-inspect rather than create duplicate correction task |

## Actions
1. **Auto-Schedule QA Inspection** — create inspection record in `qa_inspections` table, assign to the appropriate inspector (based on phase type: structural, electrical, plumbing, finishes), send calendar invite/notification with site + phase details.
2. **Inspector Fills Checklist** — inspector completes the [QA inspection checklist](../templates/qa-inspection-checklist.md) via mobile/web form: item-by-item pass/fail, photos, comments, overall verdict.
3. **Evaluate Verdict:**
   - **If issues found:** create a `correction_task` (assigned to site supervisor/subcontractor) detailing exact deficiencies, due date, and required re-inspection; set `phases.status = correction_needed`; notify responsible parties.
   - **If approved:** set `phases.status = complete`; unlock/trigger the next phase's start conditions (e.g. notify next trade crew, update project schedule); trigger the [Client Communication & Invoicing](08-client-communication-invoicing.md) workflow if this phase maps to a billing milestone.
4. **Log & Report** — append inspection outcome to `qa_inspections` history for compliance/audit trail; roll up pass rate per project/inspector for quality metrics dashboard.

## Data Flow
```
Site Supervisor marks phase "work_complete"
   │
   ▼
qa_inspections DB (create, assign inspector) ──► Inspector notified (calendar/app)
   │
   ▼ (inspector submits checklist)
Evaluate verdict
   │
   ├─► FAIL ──► correction_task created ──► Supervisor/Subcontractor notified ──► re-inspect loop
   │
   └─► PASS ──► phases.status = complete ──► Next phase triggered
                                          └──► Billing milestone triggered (if applicable)
```

## n8n Node Mapping
`Postgres Trigger (phase status = work_complete)` → `Function (select inspector by phase type)` → `Google Calendar/Send Email (schedule inspection)` → `Webhook (inspector submits checklist)` → `IF (verdict = fail)` → `Postgres (create correction_task)` + `Send Email/Slack (notify supervisor)` ; `IF (verdict = pass)` → `Postgres (update phase = complete)` → `Execute Workflow (next phase / invoicing workflow)`

## Sample Records
```json
// qa_inspections
{
  "inspection_id": "QA-2026-0119",
  "project_id": "PRJ-2026-014",
  "phase": "Electrical Rough-In",
  "inspector_id": "INS-05",
  "scheduled_at": "2026-04-18T09:00:00Z",
  "verdict": "fail",
  "checklist": { "conduit_routing": "pass", "grounding": "fail", "panel_labeling": "pass" },
  "notes": "Grounding wire not bonded at panel 2"
}
```
```json
// correction_task
{
  "task_id": "CT-2026-0031",
  "inspection_id": "QA-2026-0119",
  "assigned_to": "SUP-03",
  "description": "Bond grounding wire at panel 2",
  "due_date": "2026-04-20",
  "status": "open"
}
```

Related template: [`docs/templates/qa-inspection-checklist.md`](../templates/qa-inspection-checklist.md)
