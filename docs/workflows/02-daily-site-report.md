# 2. Daily Site Report Automation

## Purpose
Ensure a consistent, timestamped record of daily site progress is captured from every active project without relying on the supervisor to remember.

## Trigger
- **Scheduled:** Cron trigger at **17:00 (5 PM)**, Monday–Friday (skip weekends and company holidays, checked against a `holidays` calendar table), once per active project.

## Conditions
| # | Condition | Action if false |
|---|---|---|
| 1 | Project status = `active` | Skip project |
| 2 | Today is not in `holidays` table | Skip run entirely |
| 3 | No report already submitted today for this project | Skip (avoid duplicate prompts) |

## Actions
1. **Prompt Supervisor** — send a form link (mobile-friendly) via SMS/WhatsApp/Slack DM/Email to the assigned Site Supervisor, requesting: site photo(s), progress % complete, worker headcount, notes/blockers.
2. **Wait for Response** — wait node with timeout (e.g. 2 hours); if no response, send one reminder, then escalate to PM if still missing by 7 PM.
3. **Save Report** — write submitted data to `daily_reports` table (project database), attaching photo(s) to cloud storage `Site Reports/{date}` folder.
4. **Compute Deltas** — compare today's `progress_pct` to yesterday's to flag stalled/no-progress days.
5. **Send Summary to PM** — compiled email/Slack message to Project Manager with photo thumbnail, progress %, worker count, and delta flag.
6. **Update Project Dashboard** — update `progress_pct` field on the project record (Notion/Sheets) so overall project % rolls up.

## Data Flow
```
Cron (17:00 weekdays)
   │
   ▼
Active Projects query ──► Holidays check
   │
   ▼
Form sent to Site Supervisor (SMS/Slack/Email)
   │  (worker submits: photo, progress%, workers, notes)
   ▼
daily_reports DB  ──► Cloud Storage (photos)
   │
   ▼
Project record (progress_pct updated)
   │
   ▼
Project Manager (summary notification)
```

## n8n Node Mapping
`Cron` → `Notion/Airtable (get active projects)` → `IF (holiday check)` → `IF (already submitted?)` → `Send Message (Twilio/Slack/Email with Typeform/Google Form link)` → `Wait` → `Webhook (form submission)` → `Google Drive (upload photo)` → `Airtable/Postgres (insert daily_reports row)` → `Function (calc progress delta)` → `Send Email/Slack (summary to PM)`

## Sample Report Record
```json
{
  "report_id": "DR-2026-03-02-PRJ-2026-014",
  "project_id": "PRJ-2026-014",
  "date": "2026-03-02",
  "supervisor_id": "SUP-03",
  "progress_pct": 42,
  "progress_pct_prev": 38,
  "worker_count": 14,
  "photo_urls": ["https://drive.google.com/.../site_0302_1.jpg"],
  "notes": "Rebar delivery delayed by 1 day",
  "submitted_at": "2026-03-02T17:22:00Z"
}
```

Related template: [`docs/templates/daily-site-report-form.md`](../templates/daily-site-report-form.md)
