# Database / Data Structure Definitions

These tables can be implemented in any relational database (Postgres, MySQL), or mirrored as Airtable/Notion databases / Google Sheets tabs for a no-code setup. Primary keys are `id` columns (or the human-readable `*_id` shown); foreign keys reference those IDs.

## `projects`
| Column | Type | Notes |
|---|---|---|
| project_id | string (PK) | `PRJ-{YYYY}-{seq}` |
| project_name | string | |
| client_id | string (FK → clients) | |
| site_address | string | |
| manager_id | string (FK → managers) | |
| status | enum | `active`, `on_hold`, `complete`, `cancelled` |
| estimated_budget | decimal | |
| approved_budget | decimal | updated by change orders |
| total_spent | decimal | rolled up from `expenses` |
| budget_utilization_pct | decimal | computed |
| progress_pct | decimal | rolled up from `daily_reports` |
| start_date | date | |
| end_date | date | updated by change orders |
| folder_url | string | cloud storage link |
| workspace_url | string | Notion/Sheets link |
| created_at | timestamp | |

## `clients`
| Column | Type | Notes |
|---|---|---|
| client_id | string (PK) | |
| name | string | |
| primary_contact_email | string | |
| primary_contact_phone | string | |

## `managers` / `workers` (personnel)
| Column | Type | Notes |
|---|---|---|
| id | string (PK) | `MGR-##` / `W-###` |
| name | string | |
| role | enum | `project_manager`, `site_supervisor`, `laborer`, `foreman`, `inspector`, etc. |
| email | string | |
| phone | string | |
| hourly_rate | decimal | workers only |
| active | boolean | |

## `daily_reports`
| Column | Type | Notes |
|---|---|---|
| report_id | string (PK) | `DR-{date}-{project_id}` |
| project_id | string (FK) | |
| supervisor_id | string (FK) | |
| date | date | |
| progress_pct | decimal | |
| worker_count | integer | |
| photo_urls | array<string> | |
| notes | text | |
| submitted_at | timestamp | |

## `inventory`
| Column | Type | Notes |
|---|---|---|
| material_id | string (PK) | |
| project_id | string (FK, nullable) | null = shared/warehouse stock |
| name | string | |
| quantity_on_hand | decimal | |
| unit | string | |
| reorder_threshold | decimal | |
| reorder_quantity | decimal | |
| preferred_supplier_id | string (FK → suppliers) | |

## `suppliers`
| Column | Type | Notes |
|---|---|---|
| supplier_id | string (PK) | |
| name | string | |
| email | string | |
| unit_costs | json | material_id → unit_cost map |
| active | boolean | |

## `purchase_orders`
| Column | Type | Notes |
|---|---|---|
| po_id | string (PK) | `PO-{YYYY}-{seq}` |
| project_id | string (FK) | |
| material_id | string (FK) | |
| quantity | decimal | |
| unit_cost | decimal | |
| total_cost | decimal | |
| supplier_id | string (FK) | |
| status | enum | `pending`, `shipped`, `delivered`, `delayed`, `cancelled` |
| expected_delivery_date | date | |
| created_at | timestamp | |

## `safety_checklists`
| Column | Type | Notes |
|---|---|---|
| checklist_id | string (PK) | `SC-{date}-{project_id}` |
| project_id | string (FK) | |
| supervisor_id | string (FK) | |
| date | date | |
| items | json | item name → `pass`/`fail` |
| compliant | boolean | |
| notes | text | |
| submitted_at | timestamp | |

## `time_entries`
| Column | Type | Notes |
|---|---|---|
| entry_id | string (PK) | |
| worker_id | string (FK) | |
| project_id | string (FK) | |
| type | enum | `in`, `out` |
| timestamp | timestamp | |
| location | json | `{lat, lng}` |
| anomaly | boolean | unmatched pair flag |

## `payroll_reports`
| Column | Type | Notes |
|---|---|---|
| payroll_id | string (PK) | `PR-{week_ending}` |
| worker_id | string (FK) | |
| project_id | string (FK) | |
| week_ending | date | |
| regular_hours | decimal | |
| overtime_hours | decimal | |
| regular_pay | decimal | |
| overtime_pay | decimal | |
| total_pay | decimal | |
| approval_status | enum | `pending`, `approved`, `rejected` |

## `expenses`
| Column | Type | Notes |
|---|---|---|
| expense_id | string (PK) | |
| project_id | string (FK) | |
| category | enum | `materials`, `labor`, `equipment` |
| amount | decimal | |
| source_ref | string | PO/payroll/rental invoice ID |
| date | date | |

## `equipment`
| Column | Type | Notes |
|---|---|---|
| equipment_id | string (PK) | |
| type | string | |
| hours_since_last_service | decimal | |
| maintenance_interval_hours | decimal | |
| lifetime_hours | decimal | |
| status | enum | `available`, `in_use`, `maintenance_scheduled`, `in_maintenance`, `overdue` |

## `equipment_usage`
| Column | Type | Notes |
|---|---|---|
| usage_id | string (PK) | |
| equipment_id | string (FK) | |
| project_id | string (FK) | |
| hours_used | decimal | |
| date | date | |

## `maintenance_schedule`
| Column | Type | Notes |
|---|---|---|
| ticket_id | string (PK) | `MT-{YYYY}-{seq}` |
| equipment_id | string (FK) | |
| scheduled_date | date | |
| vendor | string | |
| status | enum | `scheduled`, `in_progress`, `complete` |
| service_notes | text | |

## `milestones`
| Column | Type | Notes |
|---|---|---|
| milestone_id | string (PK) | |
| project_id | string (FK) | |
| name | string | |
| status | enum | `pending`, `in_progress`, `completed` |
| billing_pct | decimal | % of contract value |
| completed_at | date | |

## `invoices`
| Column | Type | Notes |
|---|---|---|
| invoice_id | string (PK) | `INV-{YYYY}-{seq}` |
| project_id | string (FK) | |
| milestone_id | string (FK) | |
| amount | decimal | |
| due_date | date | |
| status | enum | `draft`, `sent`, `paid`, `overdue` |
| payment_link | string | |

## `phases`
| Column | Type | Notes |
|---|---|---|
| phase_id | string (PK) | |
| project_id | string (FK) | |
| name | string | e.g. "Electrical Rough-In" |
| status | enum | `not_started`, `in_progress`, `work_complete`, `correction_needed`, `complete` |
| order_index | integer | sequence within project |

## `qa_inspections`
| Column | Type | Notes |
|---|---|---|
| inspection_id | string (PK) | `QA-{YYYY}-{seq}` |
| project_id | string (FK) | |
| phase_id | string (FK) | |
| inspector_id | string (FK) | |
| scheduled_at | timestamp | |
| verdict | enum | `pass`, `fail`, `pending` |
| checklist | json | item → `pass`/`fail` |
| notes | text | |

## `correction_tasks`
| Column | Type | Notes |
|---|---|---|
| task_id | string (PK) | `CT-{YYYY}-{seq}` |
| inspection_id | string (FK) | |
| assigned_to | string (FK) | |
| description | text | |
| due_date | date | |
| status | enum | `open`, `resolved` |

## `change_orders`
| Column | Type | Notes |
|---|---|---|
| co_id | string (PK) | `CO-{YYYY}-{seq}` |
| project_id | string (FK) | |
| requested_by | string | client contact |
| description | text | |
| date_requested | date | |
| cost_impact | decimal | |
| schedule_impact_days | integer | |
| status | enum | `submitted`, `estimated`, `approved`, `rejected`, `expired` |
| approved_at | date | |

## `audit_log`
| Column | Type | Notes |
|---|---|---|
| log_id | string (PK) | |
| event_type | string | e.g. `project.created`, `co.approved` |
| entity_id | string | ID of the related record |
| payload | json | full event payload |
| created_at | timestamp | |

## `holidays`
| Column | Type | Notes |
|---|---|---|
| date | date (PK) | |
| description | string | |

## Entity Relationship Overview
```
clients 1───* projects *───1 managers
projects 1───* daily_reports
projects 1───* inventory *───1 suppliers
inventory 1───* purchase_orders
projects 1───* safety_checklists
projects *───* workers (via time_entries)
time_entries ──► payroll_reports (aggregated)
projects 1───* expenses
projects 1───* equipment_usage *───1 equipment 1───* maintenance_schedule
projects 1───* milestones 1───1 invoices
projects 1───* phases 1───* qa_inspections 1───* correction_tasks
projects 1───* change_orders
```
