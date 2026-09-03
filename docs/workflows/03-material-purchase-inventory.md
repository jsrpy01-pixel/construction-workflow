# 3. Material Purchase & Inventory

## Purpose
Prevent material shortages from stalling work by automatically generating purchase orders when stock falls below a defined threshold, and tracking delivery until stock is replenished.

## Trigger
- **Event:** `inventory` table row updated (stock quantity changed) **or** scheduled inventory-level check (e.g. every 4 hours) via cron.

## Conditions
| # | Condition | Action if false |
|---|---|---|
| 1 | `quantity_on_hand` < `reorder_threshold` for a material/project | Skip |
| 2 | No open purchase order already exists for this material+project | Skip (avoid duplicate PO) |
| 3 | Preferred supplier is active/not blacklisted | Route to backup supplier list |

## Actions
1. **Create Purchase Order** — generate PO with format `PO-{YYYY}-{sequence}`; auto-fill quantity = `reorder_quantity` (or economic order quantity), preferred supplier, unit cost from `suppliers` table, project cost code.
2. **Send PO to Supplier** — email/EDI/API call to supplier with PO attached (PDF generated from template).
3. **Notify Procurement Team** — Slack/email alert to `#procurement` with material, quantity, supplier, expected cost, project.
4. **Track Delivery Status** — create tracking record in `purchase_orders` table with status `pending`; poll supplier API or wait for manual status update (`shipped`, `delivered`, `delayed`).
5. **On Delivery Confirmation** — increment `quantity_on_hand` in `inventory` table, mark PO `status = delivered`, notify site supervisor materials arrived.
6. **On Delay** — if `expected_delivery_date` passes without status = delivered, escalate to procurement manager.

## Data Flow
```
Inventory DB (stock change / cron check)
   │
   ▼
IF stock < threshold ──► Purchase Orders DB (create PO) ──► Supplier (email/API)
   │                                                              │
   ▼                                                              ▼
Procurement Team (Slack/email)                          Delivery status updates
                                                                    │
                                                                    ▼
                                                        Inventory DB (stock replenished)
                                                                    │
                                                                    ▼
                                                        Site Supervisor notified
```

## n8n Node Mapping
`Postgres/Airtable Trigger (inventory update)` OR `Cron` → `IF (below threshold)` → `IF (no open PO)` → `Function (build PO number)` → `HTTP Request/Email (send PO to supplier)` → `Slack (notify procurement)` → `Airtable/Postgres (insert PO record, status=pending)` → `Wait/Webhook (delivery status)` → `IF (delivered)` → `Postgres (update inventory)` → `Send Email (notify supervisor)` / `IF (overdue)` → `Slack (escalate)`

## Sample PO Record
```json
{
  "po_id": "PO-2026-0087",
  "project_id": "PRJ-2026-014",
  "material": "Rebar #4 (20ft)",
  "quantity": 500,
  "unit": "pcs",
  "unit_cost": 8.75,
  "total_cost": 4375.00,
  "supplier_id": "SUP-STEEL-01",
  "status": "pending",
  "expected_delivery_date": "2026-03-06",
  "created_at": "2026-03-02T09:00:00Z"
}
```

Related template: [`docs/templates/purchase-order-template.md`](../templates/purchase-order-template.md)
