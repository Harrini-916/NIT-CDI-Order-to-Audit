# Entity Relationship Diagram

This diagram matches the entities and relationships in `docs/database-schema.md`.
That schema file is the source of truth for columns, checks, indexes, and posting rules.

Calculated results are not entities. Yield, material variance, cost per good packet, and invoice outstanding amount are derived when they are read.

PostgreSQL tables have not been created.

```mermaid
erDiagram
    STATES ||--o{ COMPANY_PROFILE : locates
    STATES ||--o{ CUSTOMERS : locates
    STATES ||--o{ SUPPLIERS : locates
    STATES ||--o{ INVOICES : place_of_supply

    COMPANY_PROFILE ||--o{ INVOICE_SEQUENCES : numbers
    COMPANY_PROFILE ||--o{ INVOICES : issues

    ROLES ||--o{ USERS : assigns
    USERS ||--o{ ORDERS : creates
    USERS ||--o{ ORDERS : verifies
    USERS ||--o{ PURCHASES : records
    USERS ||--o{ PRODUCTION_RUNS : supervises
    USERS ||--o{ DISPATCHES : dispatches
    USERS ||--o{ PAYMENTS : receives
    USERS ||--o{ AUDIT_LOGS : performs

    CUSTOMERS ||--o{ ORDERS : places
    ORDERS ||--|{ ORDER_ITEMS : contains
    PRODUCTS ||--o{ ORDER_ITEMS : ordered_as
    ORDERS ||--o| INVOICES : generates
    ORDER_ITEMS ||--o{ INVOICE_ITEMS : billed_from
    INVOICES ||--|{ INVOICE_ITEMS : contains
    PRODUCTS ||--o{ INVOICE_ITEMS : billed_as

    ORDERS ||--o{ DISPATCHES : ships
    INVOICES ||--o{ DISPATCHES : accompanies
    DISPATCHES ||--|{ DISPATCH_ITEMS : contains
    ORDER_ITEMS ||--o{ DISPATCH_ITEMS : fulfilled_from
    INVOICE_ITEMS ||--o{ DISPATCH_ITEMS : shipped_from
    PRODUCTS ||--o{ DISPATCH_ITEMS : shipped_as

    INVOICES ||--o{ PAYMENTS : collects
    PAYMENTS ||--o{ PAYMENTS : reverses

    SUPPLIERS ||--o{ PURCHASES : supplies
    PURCHASES ||--|{ PURCHASE_ITEMS : contains
    RAW_MATERIALS ||--o{ PURCHASE_ITEMS : purchased_as

    PRODUCTS ||--o{ BOM_HEADERS : has
    BOM_HEADERS ||--|{ BOM_ITEMS : contains
    RAW_MATERIALS ||--o{ BOM_ITEMS : required_in

    PRODUCTS ||--o{ PRODUCTION_RUNS : manufactured_in
    BOM_HEADERS ||--o{ PRODUCTION_RUNS : used_by
    PRODUCTION_RUNS ||--|{ PRODUCTION_MATERIAL_USAGE : consumes
    BOM_ITEMS ||--o{ PRODUCTION_MATERIAL_USAGE : plans
    RAW_MATERIALS ||--o{ PRODUCTION_MATERIAL_USAGE : used_as

    RAW_MATERIALS ||--o| RAW_MATERIAL_BALANCES : balances
    RAW_MATERIALS ||--o{ RAW_MATERIAL_MOVEMENTS : tracks
    PURCHASE_ITEMS ||--o{ RAW_MATERIAL_MOVEMENTS : received_by
    PRODUCTION_MATERIAL_USAGE ||--o{ RAW_MATERIAL_MOVEMENTS : issued_by
    RAW_MATERIAL_MOVEMENTS ||--o{ RAW_MATERIAL_MOVEMENTS : reverses

    PRODUCTS ||--o| FINISHED_GOODS_BALANCES : balances
    PRODUCTS ||--o{ FINISHED_GOODS_MOVEMENTS : tracks
    PRODUCTION_RUNS ||--o{ FINISHED_GOODS_MOVEMENTS : received_by
    DISPATCH_ITEMS ||--o{ FINISHED_GOODS_MOVEMENTS : issued_by
    FINISHED_GOODS_MOVEMENTS ||--o{ FINISHED_GOODS_MOVEMENTS : reverses

    STATES {
        bigint state_id PK
        string state_name
        string state_code
        boolean is_union_territory
    }

    COMPANY_PROFILE {
        bigint company_id PK
        bigint state_id FK
        string legal_name
        string gstin
        string costing_method
    }

    INVOICE_SEQUENCES {
        bigint sequence_id PK
        bigint company_id FK
        string financial_year
        int next_number
    }

    ROLES {
        bigint role_id PK
        string role_name
    }

    USERS {
        bigint user_id PK
        bigint role_id FK
        string name
        string email
        boolean is_active
    }

    CUSTOMERS {
        bigint customer_id PK
        bigint state_id FK
        string customer_name
        string customer_type
        string gstin
    }

    PRODUCTS {
        bigint product_id PK
        string product_name
        string hsn_code
        decimal selling_price
        decimal gst_rate
        int reorder_level
    }

    ORDERS {
        bigint order_id PK
        bigint customer_id FK
        bigint salesman_id FK
        bigint verified_by FK
        string status
        timestamptz order_date
    }

    ORDER_ITEMS {
        bigint order_item_id PK
        bigint order_id FK
        bigint product_id FK
        int quantity
        decimal unit_price
    }

    INVOICES {
        bigint invoice_id PK
        bigint company_id FK
        bigint order_id FK
        bigint place_of_supply_state_id FK
        string invoice_number
        string supply_type
        decimal cgst_amount
        decimal sgst_amount
        decimal igst_amount
        decimal total_amount
        string invoice_status
    }

    INVOICE_ITEMS {
        bigint invoice_item_id PK
        bigint invoice_id FK
        bigint order_item_id FK
        bigint product_id FK
        string hsn_code
        int quantity
        decimal unit_price
        decimal gst_rate
        decimal cgst_amount
        decimal sgst_amount
        decimal igst_amount
    }

    DISPATCHES {
        bigint dispatch_id PK
        bigint order_id FK
        bigint invoice_id FK
        bigint dispatched_by FK
        string dispatch_status
        string eway_bill_number
    }

    DISPATCH_ITEMS {
        bigint dispatch_item_id PK
        bigint dispatch_id FK
        bigint order_item_id FK
        bigint invoice_item_id FK
        bigint product_id FK
        int dispatched_quantity
    }

    PAYMENTS {
        bigint payment_id PK
        bigint invoice_id FK
        bigint reverses_payment_id FK
        string entry_type
        decimal amount
        string payment_method
    }

    SUPPLIERS {
        bigint supplier_id PK
        bigint state_id FK
        string supplier_name
        string gstin
    }

    PURCHASES {
        bigint purchase_id PK
        bigint supplier_id FK
        bigint created_by FK
        date purchase_date
        string status
    }

    PURCHASE_ITEMS {
        bigint purchase_item_id PK
        bigint purchase_id FK
        bigint material_id FK
        decimal quantity
        decimal unit_cost
    }

    RAW_MATERIALS {
        bigint material_id PK
        string material_name
        string unit
        decimal reorder_level
    }

    BOM_HEADERS {
        bigint bom_id PK
        bigint product_id FK
        string version_label
        int planned_output_quantity
        boolean is_active
        boolean is_locked
    }

    BOM_ITEMS {
        bigint bom_item_id PK
        bigint bom_id FK
        bigint material_id FK
        decimal planned_quantity
    }

    PRODUCTION_RUNS {
        bigint production_run_id PK
        bigint product_id FK
        bigint bom_id FK
        bigint supervisor_id FK
        int planned_quantity
        int good_quantity
        int damaged_quantity
        string status
    }

    PRODUCTION_MATERIAL_USAGE {
        bigint usage_id PK
        bigint production_run_id FK
        bigint bom_item_id FK
        bigint material_id FK
        decimal planned_quantity
        decimal actual_quantity
        decimal unit_cost
        decimal total_cost
    }

    RAW_MATERIAL_BALANCES {
        bigint material_id PK
        decimal quantity_on_hand
        decimal total_value
        decimal average_unit_cost
    }

    RAW_MATERIAL_MOVEMENTS {
        bigint movement_id PK
        bigint material_id FK
        bigint purchase_item_id FK
        bigint usage_id FK
        bigint reverses_movement_id FK
        string movement_type
        string direction
        decimal quantity
    }

    FINISHED_GOODS_BALANCES {
        bigint product_id PK
        int quantity_on_hand
        int quantity_reserved
        decimal total_value
        decimal average_unit_cost
    }

    FINISHED_GOODS_MOVEMENTS {
        bigint movement_id PK
        bigint product_id FK
        bigint production_run_id FK
        bigint dispatch_item_id FK
        bigint reverses_movement_id FK
        string movement_type
        string direction
        int quantity
    }

    AUDIT_LOGS {
        bigint log_id PK
        bigint user_id FK
        string action
        string entity_type
        bigint entity_id
        jsonb old_values
        jsonb new_values
        timestamptz created_at
    }
```

## Relationship notes

- One company row is allowed. Its state is the factory state used for GST.
- One customer order has one invoice and can have many dispatches.
- Each invoice line and each dispatch line points at the order line it fulfills.
- A dispatch points at both an order and an invoice, and those two must be the same order.
- One product has many BOM versions and only one active version. A production run points at the product and at the BOM version it used.
- Raw-material stock and finished-goods stock have separate balances and separate movement ledgers.
- A purchase line, a material-usage line, a production run, and a dispatch line are the document links on stock movements.
- A payment reversal points at the receipt it reverses. A stock reversal points at the movement it reverses.
- Damaged production output is stored on the production run. It does not create a finished-goods movement.
