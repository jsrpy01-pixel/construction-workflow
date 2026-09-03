# Template: Purchase Order

**PO Number:** {{po_id}}
**Date:** {{created_at}}
**Project:** {{project_name}} ({{project_id}})

**Bill To:**
{{company_name}}
{{company_address}}

**Supplier:**
{{supplier_name}}
{{supplier_email}}

| Item | Quantity | Unit | Unit Cost | Total |
|---|---|---|---|---|
| {{material_name}} | {{quantity}} | {{unit}} | {{unit_cost}} | {{total_cost}} |

**Requested Delivery Date:** {{expected_delivery_date}}
**Delivery Address:** {{site_address}}

**Notes:** {{notes}}

---
*This purchase order was generated automatically by the Construction Workflow Automation System. Please confirm receipt and expected delivery date by replying to this email.*
