# Construction Workflow Automation System

A comprehensive workflow automation system for a construction company, covering project initiation, daily site reporting, procurement, safety compliance, payroll, budget tracking, equipment maintenance, client communication/invoicing, quality assurance, and change order management.

> **Status:** Internal draft for review. No pull request has been opened — all files live directly on `main` for private review.

## Contents

| Area | Location |
|---|---|
| Workflow definitions (triggers, conditions, actions, data flow) | [`docs/workflows/`](docs/workflows) |
| Database / data structure definitions | [`docs/schemas/`](docs/schemas) |
| Integration points (Slack, Email, Google Sheets, Notion, Accounting) | [`docs/integrations.md`](docs/integrations.md) |
| n8n implementation & setup guide | [`docs/setup-guide.md`](docs/setup-guide.md) |
| Sample forms / checklists / templates | [`docs/templates/`](docs/templates) |
| Example n8n workflow exports (importable JSON) | [`n8n-workflows/`](n8n-workflows) |

## The 10 Core Workflows

1. [Project Initiation & Job Tracking](docs/workflows/01-project-initiation.md)
2. [Daily Site Report Automation](docs/workflows/02-daily-site-report.md)
3. [Material Purchase & Inventory](docs/workflows/03-material-purchase-inventory.md)
4. [Safety Compliance Check](docs/workflows/04-safety-compliance.md)
5. [Worker Time Tracking & Payroll](docs/workflows/05-time-tracking-payroll.md)
6. [Budget Tracking & Cost Alerts](docs/workflows/06-budget-tracking.md)
7. [Equipment Maintenance Schedule](docs/workflows/07-equipment-maintenance.md)
8. [Client Communication & Invoicing](docs/workflows/08-client-communication-invoicing.md)
9. [Quality Assurance Inspection](docs/workflows/09-quality-assurance.md)
10. [Change Order Management](docs/workflows/10-change-order-management.md)

## High-Level Architecture

```
                        ┌───────────────────────────┐
                        │   Automation Platform      │
                        │   (n8n / equivalent)       │
                        └─────────────┬──────────────┘
                                      │ triggers / webhooks / schedules
        ┌───────────────┬────────────┼────────────┬───────────────┬──────────────┐
        ▼               ▼            ▼            ▼               ▼              ▼
 ┌─────────────┐ ┌──────────────┐ ┌─────────┐ ┌───────────┐ ┌────────────┐ ┌────────────┐
 │  Project    │ │  Inventory / │ │ Accounting│ │ Communication│ │ Field Apps │ │  Storage   │
 │  Management │ │  Procurement │ │ / Payroll │ │ (Slack/Email)│ │ (mobile)   │ │ (Sheets/DB)│
 │  (Notion/DB)│ │  system      │ │  system   │ │              │ │            │ │            │
 └─────────────┘ └──────────────┘ └─────────┘ └───────────┘ └────────────┘ └────────────┘
```

Each workflow document describes: **Trigger → Conditions → Actions**, the systems it reads from/writes to, and the data contract exchanged between systems.

## Quick Start

See [`docs/setup-guide.md`](docs/setup-guide.md) for step-by-step instructions to stand this system up in n8n (self-hosted or cloud), including credentials, environment variables, and how to import the sample workflows in [`n8n-workflows/`](n8n-workflows).

