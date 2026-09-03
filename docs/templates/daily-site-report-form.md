# Template: Daily Site Report Form

**Sent to:** Site Supervisor, daily at 5 PM (workdays)

| Field | Type | Required |
|---|---|---|
| Project | dropdown (auto-filled) | Yes |
| Date | date (auto-filled, today) | Yes |
| Site photo(s) | file upload (1–5 images) | Yes |
| Progress complete (%) | number (0–100) | Yes |
| Workers on site (count) | number | Yes |
| Weather conditions | dropdown (Clear/Rain/Snow/Extreme Heat/Wind) | No |
| Blockers / issues | text area | No |
| Materials received today | text area | No |
| Notes | text area | No |

**Confirmation message after submit:**
> ✅ Thanks {{supervisor_name}}! Your report for {{project_name}} on {{date}} has been recorded. Progress: {{progress_pct}}%.

**Escalation if not submitted by 7 PM:**
> ⚠️ Daily report for {{project_name}} has not been submitted. Please submit ASAP or contact your Project Manager.
