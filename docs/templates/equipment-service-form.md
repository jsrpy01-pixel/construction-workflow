# Template: Equipment Service Form

**Sent to:** Maintenance Technician, on scheduled service date

| Field | Type | Required |
|---|---|---|
| Equipment ID | dropdown (auto-filled) | Yes |
| Service Date | date (auto-filled) | Yes |
| Technician Name | text | Yes |
| Service Performed | checklist (Oil change / Filter replacement / Hydraulic check / Brake inspection / Other) | Yes |
| Parts Replaced | text area | No |
| Hours Reading at Service | number | Yes |
| Issues Found | text area | No |
| Next Service Recommendation | text | No |
| Equipment Status After Service | dropdown (Available / Needs Follow-up / Out of Service) | Yes |

**On submit:** resets `hours_since_last_service` to 0, updates `equipment.status`, logs `service_notes`, closes the maintenance ticket.
