# Setup & Installation Guide

## Prerequisites

- Python 3.9+
- Node.js 14+ (for n8n)
- PostgreSQL 12+ (or alternative database)
- Git
- API keys for: Slack, Gmail, Google Sheets

## Installation Steps

### 1. Clone Repository
```bash
git clone https://github.com/jsrpy01-pixel/construction-workflow.git
cd construction-workflow
```

### 2. Setup Python Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables
```bash
cp config/environment.example .env
# Edit .env with your credentials
```

### 4. Setup Database
```bash
psql -U postgres -d construction_db -f schemas/init_database.sql
```

### 5. Deploy Workflows

#### Option A: Using n8n
```bash
npm install -g n8n
n8n start
# Import workflows from workflows/ directory
```

#### Option B: Using Dify
```bash
git clone https://github.com/langgenius/dify.git
cd dify
docker-compose up -d
# Import workflows via UI
```

### 6. Configure Integrations

Edit files in `integrations/` directory:
- `slack_config.json` - Add Slack workspace token
- `email_config.json` - Gmail API credentials
- `google_sheets_config.json` - Google API key
- `database.config.json` - Database connection string

### 7. Test Deployment
```bash
python tests/test_workflows.py
python tests/test_agents.py
python tests/test_integrations.py
```

## Workflow Configuration

Each workflow requires these settings:

```json
{
  "id": "workflow_001",
  "name": "Project Initiation",
  "trigger": {
    "type": "webhook",
    "event": "project.created"
  },
  "actions": [
    {
      "type": "assign_project_id",
      "config": {}
    }
  ],
  "enabled": true
}
```

## Integration Setup

### Slack
1. Create Slack App: https://api.slack.com/apps
2. Enable Incoming Webhooks
3. Add `slack_config.json`:
```json
{
  "webhook_url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
  "bot_token": "xoxb-your-token"
}
```

### Gmail
1. Enable Gmail API in Google Cloud Console
2. Create OAuth2 credentials
3. Add to `email_config.json`:
```json
{
  "gmail_api_key": "your-key",
  "sender_email": "automation@yourcompany.com"
}
```

### Google Sheets
1. Create Google Cloud project
2. Enable Sheets API
3. Add to `google_sheets_config.json`:
```json
{
  "api_key": "your-key",
  "spreadsheet_id": "your-sheet-id"
}
```

## Running Agents

### Start Main Orchestrator Agent
```bash
python agents/construction_agent.py
```

### Start Individual Agents
```bash
# Project Agent
python agents/project_agent.py

# Compliance Agent
python agents/compliance_agent.py

# Financial Agent
python agents/financial_agent.py

# Communication Agent
python agents/communication_agent.py

# QA Agent
python agents/qa_agent.py
```

## Monitoring & Logs

Logs are stored in `logs/`:
- `workflows.log` - Workflow execution logs
- `agents.log` - Agent activity logs
- `errors.log` - Error messages

View logs:
```bash
tail -f logs/workflows.log
```

## Troubleshooting

See [docs/troubleshooting.md](docs/troubleshooting.md) for common issues.

## Next Steps

1. Review [docs/workflow_diagrams.md](docs/workflow_diagrams.md)
2. Customize templates in `templates/`
3. Configure scheduling in each workflow
4. Run full test suite
5. Deploy to production
