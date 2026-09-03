# Integration Points

This system is designed to be automation-platform-agnostic (n8n is the reference implementation), but connects to the following categories of tools. Swap any specific product for an equivalent as long as it exposes a webhook, REST API, or supported n8n node.

## Project Management / Data Store
| Tool | Role | Notes |
|---|---|---|
| **Notion** | Project workspace, phase tracking, milestones | Use Notion API + n8n Notion node for reads/writes; database templates duplicated per project |
| **Airtable** | Alternative structured DB for all tables in [`data-model.md`](schemas/data-model.md) | Good fit if the team prefers a spreadsheet-like UI with relational linking |
| **Google Sheets** | Lightweight option for small teams, or as an export/reporting layer | Use for `payroll_reports`, `monthly cost report` outputs |
| **Postgres/MySQL** | Production-grade relational store for high-volume tables (`time_entries`, `expenses`, `equipment_usage`) | Recommended once volume outgrows Airtable/Sheets rate limits |

## Communication
| Tool | Role |
|---|---|
| **Slack** | Team channel notifications (`#new-projects`, `#procurement`, `#safety-alerts`), DMs for approval prompts |
| **Email (SMTP / Gmail / Outlook)** | Client communications, invoices, formal reports, escalations |
| **SMS/WhatsApp (Twilio)** | Time-sensitive prompts to field staff (daily report, safety checklist) where Slack/email may be missed |

## Field Data Collection
| Tool | Role |
|---|---|
| **Mobile app (custom or Glide/Softr/Typeform-based)** | Clock in/out, daily site report submission, safety checklist, QA inspection checklist, equipment service form |
| **Google Forms / Typeform / JotForm** | Low-code alternative for all field forms; webhook on submission triggers the automation |

## Inventory / Procurement
| Tool | Role |
|---|---|
| **Inventory DB (Airtable/Postgres)** | `inventory` table with reorder thresholds |
| **Supplier email/EDI/API** | PO delivery to suppliers |

## Accounting / Payroll
| Tool | Role |
|---|---|
| **QuickBooks / Xero** | Invoice generation, expense sync, payment tracking |
| **Gusto / ADP / Paychex** | Payroll disbursement after approval |
| **Stripe / ACH processor** | Client payment links, payment-received webhooks |

## Equipment / Maintenance
| Tool | Role |
|---|---|
| **Telematics/IoT (e.g. Samsara, equipment OEM APIs)** | Usage-hour logging (optional; manual logging via mobile app is a valid fallback) |
| **Google Calendar** | Maintenance appointment scheduling |

## Document / File Storage
| Tool | Role |
|---|---|
| **Google Drive / SharePoint** | Project folders, photos, generated PDFs (invoices, reports, change orders) |
| **DocuSign / HelloSign** | Change order and contract e-signatures |

## Automation Platform
| Tool | Role |
|---|---|
| **n8n** (reference) | Orchestrates all triggers, conditions, and actions described in [`docs/workflows/`](workflows) |
| Alternatives: **Zapier, Make (Integromat), Activepieces** | Same workflow logic can be re-implemented; node names differ but trigger/condition/action structure is portable |

## Data Flow Summary Across Systems
```
Field Apps (mobile) ──┐
Google Forms/Typeform ─┼──► n8n (Automation Platform) ──► Project DB (Notion/Airtable/Postgres)
IoT/Telematics ────────┘             │                              │
                                      ├──► Slack / Email / SMS       │
                                      ├──► Accounting (QuickBooks/Xero/Payroll)
                                      ├──► Cloud Storage (Drive/SharePoint)
                                      └──► Calendar / E-signature (Calendar, DocuSign)
```

## Credential & Secret Management
- Store all API keys/tokens as n8n **Credentials** (encrypted at rest), never hard-coded in workflow JSON.
- Use environment-specific credentials for staging vs. production instances.
- Rotate Slack/email/accounting API tokens on a regular schedule; audit access via the `audit_log` table.
