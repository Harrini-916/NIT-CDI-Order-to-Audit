
# Database Design

## 1. Overview

The application uses PostgreSQL as its relational database.
The database is designed to manage sales, purchases, production,
inventory, billing, payments and audit records.

## 2. Main Tables

### User Management

- roles: Stores available application roles.
- users: Stores user accounts and their assigned roles.

### Sales Management

- customers: Stores retailer and distributor details.
- products: Stores finished product information.
- orders: Stores customer orders.
- order_items: Stores products and quantities in each order.

### Billing and Payments

- invoices: Stores GST invoice details.
- invoice_items: Stores invoice product details.
- payments: Stores customer payment records.

### Purchase Management

- suppliers: Stores supplier information.
- purchases: Stores purchase transactions.
- purchase_items: Stores purchased materials and quantities.

### Production Management

- raw_materials: Stores raw material information.
- bom_headers: Stores product-level Bill of Materials.
- bom_items: Stores materials and planned quantities in each BOM.
- production_runs: Stores production batch details.
- production_material_usage: Stores actual material consumption.

### Inventory Management

- stock_movements: Records every stock increase and decrease.

### Audit Management

- audit_logs: Records important user actions and transaction changes.

## 3. Important Relationships

- One role can be assigned to many users.
- One customer can place many orders.
- One order can contain many order items.
- One order can have an invoice.
- One invoice can have multiple payments.
- One product can have a BOM.
- One BOM can contain multiple raw materials.
- One product can have multiple production runs.
- One production run can record multiple material usage entries.
- Stock movements record inventory transactions.

## 4. Inventory Design

Stock will be calculated using stock movement records.

Stock Balance = Total Stock In - Total Stock Out

The application will not rely on manually overwriting stock quantities.

Every purchase, production issue, production receipt,
damage and dispatch must create an appropriate stock movement.

## 5. Production Design

The BOM defines the expected raw materials required to manufacture a product.

Each production run records:

- Planned production quantity
- Actual good quantity
- Damaged quantity
- Planned material consumption
- Actual material consumption
- Yield variance
- Material consumption variance

## 6. Financial Design

- Store monetary values using decimal precision or integer paise.
- Calculate GST according to the customer's state and factory location.
- Track invoice totals and outstanding payments.
- Calculate production cost per good packet.

## 7. Auditability

Important operations must record:

- User who performed the action
- Action performed
- Related record
- Date and time
- Previous and updated values where applicable

## 8. Project Status

Initial database design completed.
Detailed schema and ER diagram pending.
