# Construction Company Workflow Automation System

A comprehensive automation platform designed to streamline construction company operations through intelligent workflow management.

## Overview

This system automates 10 critical business processes:
1. Project Initiation & Job Tracking
2. Daily Site Report Automation
3. Material Purchase & Inventory
4. Safety Compliance Check
5. Worker Time Tracking & Payroll
6. Budget Tracking & Cost Alerts
7. Equipment Maintenance Schedule
8. Client Communication & Invoicing
9. Quality Assurance Inspection
10. Change Order Management

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│      Construction Workflow Orchestrator Agent                │
│  (Coordinates all 10 automation workflows)                   │
└──────────────┬──────────────────────────────────────────────┘
               │
      ┌────────┴─────────┬──────────────┬──────────────┐
      │                  │              │              │
   Project        Daily Reports    Material Mgmt    Safety Checks
   Tracking       & Alerts         & Inventory      & Compliance
      │                  │              │              │
      └────────┬─────────┴──────────────┴──────────────┘
               │
      ┌────────┴─────────┬──────────────┬──────────────┐
      │                  │              │              │
   Payroll         Budget Tracking   Equipment      Client Comms
   & Time          & Cost Alerts     Maintenance    & Invoicing
      │                  │              │              │
      └────────┬─────────┴──────────────┴──────────────┘
               │
      ┌────────┴─────────────────────────────┐
      │                                       │
   QA Inspection              Change Order Management
```

## Tech Stack

- **Orchestration Engine**: n8n / Dify / Activepieces
- **Backend**: Python 3.9+
- **Database**: PostgreSQL
- **Communication**: Slack, Email, SMS
- **Cloud Storage**: Google Drive, AWS S3
- **Authentication**: OAuth2 / JWT

## Directory Structure

```
construction-workflow/
├── README.md                    # This file
├── SETUP.md                     # Installation guide
├── workflows/                   # Workflow definitions
│   ├── 1_project_initiation.json
│   ├── 2_daily_reports.json
│   ├── 3_material_inventory.json
│   ├── 4_safety_compliance.json
│   ├── 5_payroll_tracking.json
│   ├── 6_budget_alerts.json
│   ├── 7_equipment_maintenance.json
│   ├── 8_client_invoicing.json
│   ├── 9_qa_inspection.json
│   └── 10_change_orders.json
├── agents/                      # AI Agents
│   ├── construction_agent.py    # Main orchestrator
│   ├── project_agent.py
│   ├── compliance_agent.py
│   └── financial_agent.py
├── schemas/                     # Database schemas
├── templates/                   # Forms & templates
├── integrations/                # Integration configs
├── tests/                       # Test suite
├── docs/                        # Documentation
└── config/                      # Configuration
```

## Quick Start

1. Clone the repository
2. Follow [SETUP.md](./SETUP.md) for installation
3. Configure integrations in `integrations/`
4. Deploy workflows to automation platform
5. Run test suite: `python -m pytest tests/`

## Features

✅ Fully automated project tracking
✅ Real-time notifications and alerts
✅ AI-powered decision making
✅ Budget monitoring with cost alerts
✅ Safety compliance tracking
✅ Automated payroll processing
✅ Client communication automation
✅ Quality assurance workflows
✅ Equipment maintenance scheduling
✅ Change order management

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific workflow tests
python -m pytest tests/test_workflows.py

# Run with coverage
python -m pytest tests/ --cov=agents/
```

## Support & Documentation

- [Setup Guide](./SETUP.md)
- [Workflow Diagrams](./docs/workflow_diagrams.md)
- [API Reference](./docs/api_reference.md)
- [Troubleshooting](./docs/troubleshooting.md)

## License

Private & Confidential - Construction Company Internal Use Only
