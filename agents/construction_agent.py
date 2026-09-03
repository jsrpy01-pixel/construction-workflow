#!/usr/bin/env python3
"""
Construction Company Workflow Automation - Main Orchestrator Agent
Manages and coordinates all 10 automation workflows
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any
from dataclasses import dataclass
import os
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/construction_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class WorkflowEvent:
    """Represents an event that triggers a workflow"""
    workflow_id: str
    event_type: str
    data: Dict[str, Any]
    timestamp: datetime


class ConstructionAutomationAgent:
    """Main orchestrator agent for construction workflow automation"""

    def __init__(self, config_path: str = 'config/workflow.config.json'):
        """Initialize the construction automation agent"""
        self.config = self._load_config(config_path)
        self.workflows = {}
        self.active_workflows = {}
        self.event_queue = []
        self.execution_history = []
        logger.info("Construction Automation Agent initialized")

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {config_path}. Using defaults.")
            return self._get_default_config()

    def _get_default_config(self) -> Dict:
        """Get default configuration"""
        return {
            "agent_name": "Construction Automation Agent",
            "version": "1.0.0",
            "workflows_enabled": 10,
            "max_concurrent_workflows": 5,
            "retry_attempts": 3,
            "timeout_seconds": 300
        }

    def load_workflows(self) -> None:
        """Load all workflow definitions from workflows/ directory"""
        workflows_dir = Path('workflows')
        if not workflows_dir.exists():
            logger.error("Workflows directory not found")
            return

        workflow_files = sorted(workflows_dir.glob('*.json'))
        logger.info(f"Found {len(workflow_files)} workflow files")

        for workflow_file in workflow_files:
            try:
                with open(workflow_file, 'r') as f:
                    workflow = json.load(f)
                    self.workflows[workflow['id']] = workflow
                    logger.info(f"Loaded workflow: {workflow['name']} ({workflow['id']})")
            except Exception as e:
                logger.error(f"Error loading workflow {workflow_file}: {e}")

    def process_event(self, event: WorkflowEvent) -> bool:
        """Process an incoming event and trigger appropriate workflows"""
        logger.info(f"Processing event: {event.event_type} for workflow {event.workflow_id}")
        
        try:
            # Find matching workflow
            workflow = self.workflows.get(event.workflow_id)
            if not workflow:
                logger.warning(f"Workflow not found: {event.workflow_id}")
                return False

            # Check if workflow is enabled
            if not workflow.get('enabled', True):
                logger.info(f"Workflow {event.workflow_id} is disabled")
                return False

            # Check trigger condition
            if not self._check_trigger_condition(workflow, event):
                logger.info(f"Trigger condition not met for {event.workflow_id}")
                return False

            # Execute workflow
            return self._execute_workflow(workflow, event)

        except Exception as e:
            logger.error(f"Error processing event: {e}")
            return False

    def _check_trigger_condition(self, workflow: Dict, event: WorkflowEvent) -> bool:
        """Check if workflow trigger conditions are met"""
        trigger = workflow.get('trigger', {})
        trigger_type = trigger.get('type')
        trigger_event = trigger.get('event')

        if trigger_type == 'webhook' and trigger_event == event.event_type:
            return True
        elif trigger_type == 'schedule':
            return self._check_schedule_trigger(trigger)
        elif trigger_type == 'manual':
            return True

        return False

    def _check_schedule_trigger(self, trigger: Dict) -> bool:
        """Check if scheduled trigger should fire"""
        # TODO: Implement cron/schedule checking
        return True

    def _execute_workflow(self, workflow: Dict, event: WorkflowEvent) -> bool:
        """Execute a workflow with given event data"""
        workflow_id = workflow['id']
        
        try:
            logger.info(f"Executing workflow: {workflow['name']} ({workflow_id})")
            
            # Mark workflow as active
            self.active_workflows[workflow_id] = {
                'started_at': datetime.now(),
                'status': 'running'
            }

            # Execute actions
            execution_result = {
                'workflow_id': workflow_id,
                'workflow_name': workflow['name'],
                'event': event.event_type,
                'timestamp': datetime.now().isoformat(),
                'status': 'success',
                'actions_executed': 0,
                'errors': []
            }

            actions = workflow.get('actions', [])
            for action in actions:
                try:
                    self._execute_action(action, event.data)
                    execution_result['actions_executed'] += 1
                except Exception as e:
                    logger.error(f"Action failed: {e}")
                    execution_result['errors'].append(str(e))
                    execution_result['status'] = 'partial_failure'

            # Store execution history
            self.execution_history.append(execution_result)
            self.active_workflows[workflow_id]['status'] = 'completed'
            
            logger.info(f"Workflow {workflow_id} completed: {execution_result['status']}")
            return execution_result['status'] in ['success', 'partial_failure']

        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            self.active_workflows[workflow_id]['status'] = 'failed'
            return False

    def _execute_action(self, action: Dict, data: Dict) -> None:
        """Execute a single action within a workflow"""
        action_type = action.get('type')
        action_config = action.get('config', {})

        logger.debug(f"Executing action: {action_type}")

        if action_type == 'send_notification':
            self._send_notification(action_config, data)
        elif action_type == 'create_record':
            self._create_record(action_config, data)
        elif action_type == 'update_record':
            self._update_record(action_config, data)
        elif action_type == 'send_email':
            self._send_email(action_config, data)
        elif action_type == 'assign_id':
            self._assign_id(action_config, data)
        else:
            logger.warning(f"Unknown action type: {action_type}")

    def _send_notification(self, config: Dict, data: Dict) -> None:
        """Send notification (Slack, email, etc.)"""
        channels = config.get('channels', [])
        message = config.get('message', '')
        logger.info(f"Sending notification to {channels}: {message}")

    def _create_record(self, config: Dict, data: Dict) -> None:
        """Create a new record in database"""
        table = config.get('table')
        logger.info(f"Creating record in table: {table}")

    def _update_record(self, config: Dict, data: Dict) -> None:
        """Update an existing record in database"""
        table = config.get('table')
        logger.info(f"Updating record in table: {table}")

    def _send_email(self, config: Dict, data: Dict) -> None:
        """Send an email"""
        recipient = config.get('recipient')
        subject = config.get('subject')
        logger.info(f"Sending email to {recipient}: {subject}")

    def _assign_id(self, config: Dict, data: Dict) -> None:
        """Assign a unique ID to a resource"""
        resource_type = config.get('resource_type')
        logger.info(f"Assigning ID for resource type: {resource_type}")

    def get_status(self) -> Dict:
        """Get current status of all workflows"""
        return {
            'agent_status': 'running',
            'timestamp': datetime.now().isoformat(),
            'total_workflows': len(self.workflows),
            'active_workflows': len(self.active_workflows),
            'total_executions': len(self.execution_history),
            'workflows': [
                {
                    'id': wf_id,
                    'name': wf.get('name'),
                    'enabled': wf.get('enabled', True),
                    'status': self.active_workflows.get(wf_id, {}).get('status', 'idle')
                }
                for wf_id, wf in self.workflows.items()
            ]
        }

    def get_execution_history(self, workflow_id: str = None, limit: int = 10) -> List[Dict]:
        """Get execution history for workflows"""
        history = self.execution_history[-limit:]
        if workflow_id:
            history = [h for h in history if h['workflow_id'] == workflow_id]
        return history

    def health_check(self) -> bool:
        """Check if agent is healthy and all workflows are loaded"""
        return len(self.workflows) > 0


def main():
    """Main entry point"""
    logger.info("Starting Construction Automation Agent")
    
    # Create agent instance
    agent = ConstructionAutomationAgent()
    
    # Load all workflows
    agent.load_workflows()
    
    # Check health
    if agent.health_check():
        logger.info("Agent is healthy and ready")
        logger.info(f"Loaded {len(agent.workflows)} workflows")
    else:
        logger.error("Agent health check failed")
        return
    
    # Print status
    status = agent.get_status()
    print(json.dumps(status, indent=2))
    
    logger.info("Construction Automation Agent ready to accept events")


if __name__ == '__main__':
    main()
