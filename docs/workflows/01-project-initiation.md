# 1. Project Initiation & Job Tracking

## Purpose
Automatically bootstrap a new construction project the moment it is created in the Project Management system, eliminating manual folder creation, ID assignment, and kickoff notifications.

## Trigger
- **Event:** New record created in `projects` table (Project Management system — e.g. Notion database, Airtable, or internal PM tool) **or** webhook fired by the PM system's "New Project" form.

## Conditions
| # | Condition | Action if false |
|---|---|---|
| 1 | Required fields present (`project_name`, `client_id`, `site_address`, `start_date`, `estimated_budget`) | Notify admin, halt workflow |
| 2 | `manager_id` not already set | Skip auto-assignment step |

## Actions
1. **Generate Project ID** — format `PRJ-{YYYY}-{sequence}` (e.g. `PRJ-2026-014`), written back to the `projects` record.
2. **Assign Project Manager** — round-robin or workload-based lookup against the `managers` table; write `manager_id` + `manager_name` back to the project record.
3. **Create Project Folder** — create a folder in cloud storage (Google Drive / SharePoint) named `{project_id} - {project_name}` with standard subfolders: `Contracts`, `Site Reports`, `Photos`, `Invoices`, `Change Orders`, `QA`.
4. **Create Project Workspace** — create a linked Notion page / Sheets tab for the project using a template, pre-populated with `project_id`, `manager`, `budget`, `milestones`.
5. **Send Kickoff Email** — email project team (manager, site supervisor, procurement contact, client contact) with project details: ID, address, budget, start date, folder link, workspace link.
6. **Post to Slack** — message to `#new-projects` channel summarizing the new project.
7. **Log Event** — append row to `audit_log` table.

## Data Flow
```
PM System (new project webhook)
   │
   ▼
Automation Platform
   ├─► Managers DB  (read: availability)          ─► write manager_id back to Project
   ├─► Cloud Storage API (create folder tree)      ─► write folder_url back to Project
   ├─► Notion/Sheets API (clone project template)  ─► write workspace_url back to Project
   ├─► Email/SMTP (send kickoff email)
   ├─► Slack API (post message)
   └─► Audit Log DB (append record)
```

## n8n Node Mapping
`Webhook / Notion Trigger` → `IF (validate fields)` → `Function (generate Project ID)` → `Notion/Airtable (query available managers)` → `HTTP Request (Google Drive: create folder)` → `Notion (create workspace page)` → `Send Email` → `Slack` → `Google Sheets (append audit log)`

## Sample Payload
```json
{
  "event": "project.created",
  "project_id": "PRJ-2026-014",
  "project_name": "Riverside Apartments Phase 2",
  "client_id": "CL-0091",
  "site_address": "142 Riverside Dr, Springfield",
  "estimated_budget": 1250000,
  "start_date": "2026-03-01",
  "manager_id": "MGR-07",
  "folder_url": "https://drive.google.com/.../PRJ-2026-014",
  "workspace_url": "https://notion.so/.../PRJ-2026-014"
}
```

Related template: [`docs/templates/project-kickoff-email.md`](../templates/project-kickoff-email.md)
