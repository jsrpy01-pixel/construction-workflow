# Setup Guide — Implementing in n8n

This guide walks through standing up the construction workflow automation system using **n8n** (self-hosted or n8n Cloud). The same concepts apply to Zapier/Make/Activepieces with equivalent nodes.

## 1. Prerequisites
- An n8n instance (Docker self-hosted, or n8n Cloud account).
- A data store: Airtable/Notion (fastest to start) or a Postgres database (recommended at scale). Create the tables described in [`docs/schemas/data-model.md`](schemas/data-model.md).
- Accounts/API access for: Slack, email/SMTP provider, Twilio (optional, SMS), Google Drive or SharePoint, QuickBooks/Xero, Google Calendar, DocuSign (optional).
- A form tool for field data collection (Google Forms, Typeform, or a custom mobile app posting to n8n webhooks).

## 2. Install / Start n8n
```bash
# Self-hosted via Docker
docker volume create n8n_data
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n
```
Or sign up at n8n.cloud for a managed instance.

## 3. Configure Credentials
In n8n, go to **Credentials → New** and add:
- Slack (OAuth or Bot Token)
- SMTP / Gmail / Outlook (email)
- Twilio (Account SID + Auth Token) — optional, for SMS
- Notion API / Airtable Personal Access Token / Postgres connection
- Google Drive / Google Calendar (OAuth2)
- QuickBooks/Xero (OAuth2)
- DocuSign (optional)

## 4. Create the Data Store
- **Option A (fast start): Airtable/Notion** — create one base/database per table in `data-model.md`; link related tables via linked-record fields.
- **Option B (production): Postgres** — run the DDL translated from `data-model.md` (one `CREATE TABLE` per entity), then add the **Postgres** credential in n8n.

## 5. Import the Sample Workflows
Sample importable workflow JSON files are provided in [`n8n-workflows/`](../n8n-workflows):
- `01-project-initiation.json`
- `02-daily-site-report.json`
- `03-material-purchase-inventory.json`

To import: n8n UI → **Workflows → Import from File** → select the JSON → update each node's credentials to point at your accounts → **Activate**.

Use these as templates: duplicate and adapt the same trigger/condition/action pattern for workflows 4–10 using the definitions in [`docs/workflows/`](workflows).

## 6. Wire Up Field Data Collection
1. Create a **Webhook** trigger node in n8n for each form (daily report, safety checklist, QA checklist, clock in/out, change order request).
2. Point your form tool's "on submit" webhook/integration at the n8n Webhook URL (Typeform → Webhooks; Google Forms → Apps Script `UrlFetchApp.fetch`; custom mobile app → HTTP POST).
3. Confirm payload field names match what the workflow's `Function`/`Set` nodes expect (see the "Sample Payload"/"Sample Record" JSON in each workflow doc).

## 7. Configure Schedules
Set **Cron** node schedules to match your business hours/timezone:
| Workflow | Suggested schedule |
|---|---|
| Daily Site Report | 17:00 Mon–Fri |
| Safety Compliance (daily) | 06:30 Mon–Sat |
| Safety Compliance (weekly report) | Fri 18:00 |
| Payroll | Fri 18:00 |
| Budget monthly report | 1st of month, 08:00 |
| Equipment maintenance check | Daily 06:00 |

Remember to set the n8n instance timezone (**Settings → General**) to the project site's local timezone.

## 8. Test Each Workflow
1. Use n8n's **Execute Workflow** (manual trigger) with sample data from each workflow doc's "Sample Payload"/"Sample Record" section.
2. Verify each downstream action (DB write, Slack message, email) fires correctly in a staging Slack channel/test inbox before pointing at production channels.
3. Check **Executions** tab for errors; add **Error Trigger** workflows to alert an admin channel on failures.

## 9. Go Live Checklist
- [ ] All credentials configured and tested
- [ ] All 10 workflows imported/built and activated
- [ ] Field forms wired to webhooks and tested end-to-end
- [ ] Schedules confirmed in correct timezone
- [ ] Error-handling workflow active (alerts on failed executions)
- [ ] Access control reviewed (who can edit workflows/credentials in n8n)
- [ ] Backups configured for the underlying database

## 10. Maintenance
- Review `audit_log` weekly for anomalies.
- Revisit thresholds (safety escalation, budget 80%, equipment maintenance interval, reorder threshold) quarterly as the business scales.
- Version-control workflow JSON exports in this repository (`n8n-workflows/`) whenever a workflow is materially changed.
