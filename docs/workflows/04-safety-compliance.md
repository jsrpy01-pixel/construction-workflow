# 4. Safety Compliance Check

## Purpose
Enforce a daily pre-work safety checklist on every active site, escalate issues immediately, and roll up compliance into a weekly report for management.

## Trigger
- **Scheduled:** Cron trigger every morning (e.g. **06:30**, before the typical 07:00 work start), Monday–Saturday, per active project.

## Conditions
| # | Condition | Action if false |
|---|---|---|
| 1 | Project status = `active` | Skip project |
| 2 | Checklist not already submitted today | Skip re-send |

## Actions
1. **Send Checklist** — push the [safety checklist form](../templates/safety-checklist-form.md) to the Site Supervisor (mobile app / SMS link / Slack).
2. **Collect Responses** — capture: PPE availability (hard hats, harnesses, gloves, eyewear), scaffolding/ladder condition, fire extinguisher access, first-aid kit stocked, site hazards (weather, excavation, electrical), free-text notes.
3. **Evaluate Responses** — if any item marked "Fail"/"Issue" → flag as `non_compliant`.
4. **Escalate on Issues** — if `non_compliant`, immediately notify Safety Manager (SMS + email + Slack `#safety-alerts`) with the specific failed items and site; optionally block work-start confirmation until resolved.
5. **Log Result** — write to `safety_checklists` table regardless of outcome.
6. **Weekly Report** — every Friday at 18:00 (or Sunday night), aggregate the week's checklists per project: compliance rate %, list of issues raised, resolution status, trend vs. prior week → send PDF/summary to management distribution list.

## Data Flow
```
Cron (06:30 daily)
   │
   ▼
Active Projects ──► Send checklist to Supervisor (mobile/SMS/Slack)
   │                          │
   │                          ▼ (submits)
   │                 safety_checklists DB
   │                          │
   │                 IF any "Fail" item
   │                          │
   │                          ▼
   │                 Safety Manager escalation (SMS/Email/Slack)
   │
   ▼ (Fridays)
Aggregate weekly compliance ──► Weekly Safety Report (PDF/email) ──► Management
```

## n8n Node Mapping
`Cron` → `Airtable/Postgres (active projects)` → `Send SMS/Slack (checklist link)` → `Webhook (form response)` → `Function (evaluate pass/fail)` → `IF (non_compliant)` → `Twilio + Send Email + Slack (escalate to Safety Manager)` → `Postgres (insert safety_checklists row)`
Weekly branch: `Cron (Fri 18:00)` → `Postgres (aggregate query)` → `Function (build report)` → `Generate PDF (HTML→PDF)` → `Send Email (management list)`

## Sample Checklist Record
```json
{
  "checklist_id": "SC-2026-03-02-PRJ-2026-014",
  "project_id": "PRJ-2026-014",
  "date": "2026-03-02",
  "supervisor_id": "SUP-03",
  "items": {
    "ppe_available": "pass",
    "scaffolding_condition": "pass",
    "fire_extinguisher": "fail",
    "first_aid_kit": "pass",
    "site_hazards": "pass"
  },
  "compliant": false,
  "notes": "Fire extinguisher near Tower A missing, needs replacement",
  "submitted_at": "2026-03-02T06:41:00Z"
}
```

Related templates: [`docs/templates/safety-checklist-form.md`](../templates/safety-checklist-form.md), [`docs/templates/weekly-safety-report.md`](../templates/weekly-safety-report.md)
