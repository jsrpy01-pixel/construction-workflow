# 7. Equipment Maintenance Schedule

## Purpose
Keep heavy equipment (excavators, cranes, mixers, generators, etc.) in safe working order by tracking usage hours and automatically scheduling maintenance before it's overdue.

## Trigger
- **Event-based:** Equipment usage logged (from telematics/IoT sensor, or manual entry via mobile app when checking equipment in/out of a site).
- **Scheduled:** Daily cron check (e.g. **06:00**) comparing `hours_since_last_service` against `maintenance_interval_hours` for all equipment.

## Conditions
| # | Condition | Action if false |
|---|---|---|
| 1 | `hours_since_last_service >= maintenance_interval_hours * 0.9` (90% threshold — reminder) | No reminder |
| 2 | `hours_since_last_service >= maintenance_interval_hours` (due) | No scheduling action |
| 3 | Equipment not already `status = in_maintenance` | Skip (already scheduled) |

## Actions
1. **Log Usage Hours** — on each use event, append to `equipment_usage` table and increment `equipment.hours_since_last_service` and `equipment.lifetime_hours`.
2. **Send Reminder (90% threshold)** — notify Maintenance Team (Slack/email) that equipment `X` is approaching its service interval, with days/hours remaining estimate.
3. **Maintenance Due — Schedule Appointment** — when threshold reached: create a maintenance ticket in `maintenance_schedule` table, contact internal maintenance team or external vendor to book an appointment (calendar invite / vendor API), set `equipment.status = maintenance_scheduled`.
4. **Update Equipment Status** — on the appointment date, mark `status = in_maintenance` (equipment pulled from availability pool); on completion confirmation (technician submits service form), reset `hours_since_last_service = 0`, log `service_notes`, set `status = available`.
5. **Escalate Overdue** — if equipment continues to be used past 100% of interval without a scheduled appointment, escalate to Maintenance Manager and flag equipment as `overdue` (should be pulled from active use).

## Data Flow
```
Telematics/IoT or manual log ──► equipment_usage DB ──► equipment.hours_since_last_service (increment)
                                                                    │
                                          Cron (daily 06:00) ──► Threshold check
                                                                    │
                              ┌─────────────────────────────────────┼─────────────────────────┐
                              ▼ 90% (reminder)                       ▼ 100% (due)               ▼ overdue+in-use
                    Maintenance Team notified          Maintenance ticket + appointment      Escalate to Manager
                                                        booked (calendar/vendor API)
                                                                    │
                                                        equipment.status updated
                                                        (scheduled → in_maintenance → available)
```

## n8n Node Mapping
`Webhook/IoT (usage event)` → `Postgres (update hours)`
Daily: `Cron` → `Postgres (query equipment nearing/at interval)` → `IF (>=90%)` → `Slack/Email (reminder)` → `IF (>=100%)` → `Function (create ticket)` → `Google Calendar/HTTP Request (book appointment with vendor)` → `Postgres (update status)` → `Webhook (technician completes service form)` → `Postgres (reset hours, log notes, status=available)`

## Sample Records
```json
// equipment
{
  "equipment_id": "EQ-CRANE-02",
  "type": "Tower Crane",
  "hours_since_last_service": 248,
  "maintenance_interval_hours": 250,
  "lifetime_hours": 5120,
  "status": "maintenance_scheduled"
}
```
```json
// maintenance_schedule
{
  "ticket_id": "MT-2026-0044",
  "equipment_id": "EQ-CRANE-02",
  "scheduled_date": "2026-03-10",
  "vendor": "CraneCare Services",
  "status": "scheduled"
}
```

Related template: [`docs/templates/equipment-service-form.md`](../templates/equipment-service-form.md)
