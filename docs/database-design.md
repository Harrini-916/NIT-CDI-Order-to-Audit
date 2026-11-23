# Database Design

## 1. Overview

The application uses PostgreSQL. This design covers the internship workflow for a small-scale snacks factory: roles, sales orders, purchases, raw-material and finished-goods inventory, BOM and production, GST billing, product costing, dispatch, payments, and an audit trail.

`docs/database-schema.md` is the source of truth for tables, keys, checks, and posting rules. `docs/er-diagram.md` shows the same entities and relationships. This file explains the design. No SQL has been written, and no feature is implemented.

## 2. Internship modules

The database supports these modules. They are designed here and not yet built.

1. Authentication and role management.
2. Sales and order management.
3. Inventory management.
4. BOM and production management.
5. GST billing.
6. Product costing.
7. Reports and auditing.

The application roles are salesman, factory admin, production supervisor, accountant / auditor, and owner.

The sales path is salesman order, admin verification, GST invoice, dispatch, finished-goods reduction, then payment.

The production path is purchase, raw-material stock, BOM-based material issue, production run, actual output and damage, finished-goods stock, then yield and material variance.

## 3. Main tables

### Organisation

- states: GST state names and codes.
- company_profile: the single factory, its GSTIN, and its state.

### Users

- roles: the five application roles.
- users: accounts, password hashes, and one role each.

### Sales

- customers: retailers and distributors, each linked to a state.
- products: packets for sale, with HSN, tax-exclusive price, GST rate, and reorder level.
- orders: customer orders, the salesman, and the verifying user.
- order_items: one row per product on an order.

### Purchases

- suppliers: material suppliers and their state.
- raw_materials: materials, stock units, and reorder levels.
- purchases: purchase documents and their status.
- purchase_items: material, quantity, and unit cost.

### Production

- bom_headers: one versioned recipe per product batch size, with one active version.
- bom_items: materials required for that batch size.
- production_runs: planned, issued, completed, and posted batches.
- production_material_usage: snapshotted plan, actual quantity, and issued cost.

### Inventory

- raw_material_balances and finished_goods_balances: current quantity and value, locked during posting.
- raw_material_movements and finished_goods_movements: the stock ledger.

### Billing and collection

- invoice_sequences: consecutive invoice numbers for each financial year.
- invoices and invoice_items: posted GST invoices, frozen party details, and line tax.
- dispatches and dispatch_items: deliveries against an invoice and its order lines.
- payments: receipts and reversals against an invoice.

### Audit

- audit_logs: append-only history of who changed which record, and the old and new values.

## 4. Relationships

- One state is used by the company, many customers, many suppliers, and many invoices as the place of supply.
- One role is assigned to many users. Each user has one role.
- One customer places many orders. One salesman creates an order, and one user may verify it.
- One order contains many order lines. One order has one invoice.
- One invoice contains many invoice lines. Each invoice line points at one order line.
- One order can have many dispatches. Each dispatch belongs to one invoice of that same order.
- Each dispatch line points at one order line and one invoice line.
- One invoice has many payments. A reversal payment points at the receipt it reverses.
- One supplier has many purchases. Each purchase line points at one raw material.
- One product has many BOM versions. One BOM has many materials.
- One production run manufactures one product with one BOM. Each usage line points at one BOM item.
- Raw-material movements point at a purchase line or a usage line. Finished-goods movements point at a production run or a dispatch line.
- Every balance row belongs to one material or one product.

Foreign keys are mandatory unless this design names them optional, such as the verifying user before verification, the invoice number before posting, and the unused document link on a stock movement. Foreign keys restrict deletion. Users and masters are deactivated instead of deleted.

## 5. GST design

The factory state lives on `company_profile`. The customer state lives on `customers`. Both use `states`, so the name and the GST state code stay together.

At invoice posting the transaction copies legal name, address, GSTIN, and both state codes onto the invoice. It also copies HSN, quantity, tax-exclusive price, and GST rate onto each line. Later edits to the customer or product do not change a posted invoice.

Place of supply for these goods is the customer state. Supply is intra-state when the company state code equals the customer state code, including a union territory. Supply is inter-state when the codes differ.

Intra-state tax is CGST plus SGST, each half of the line tax, and IGST is zero. The extra paise on an odd tax amount goes to CGST. Inter-state tax is all IGST. Header totals are the sums of the lines.

Prices on products, order lines, and invoice lines are tax-exclusive. Line taxable value is quantity times unit price, rounded to one paise. Line tax is rounded to one paise before the CGST and SGST split.

The invoice number is assigned when the invoice is posted, from `invoice_sequences`, and it stays unique for that financial year. The year starts in the month stored on the company, which defaults to April. A cancelled invoice keeps its number.

## 6. Inventory design

Raw materials and finished goods use separate balance and movement tables. Material quantities are decimals. Finished goods are whole packets.

The movement ledger is the history. The balance row is the current position used for locking and for reorder checks. Posting updates both in one transaction. A movement quantity is always positive, and its direction is `in` or `out`.

Inbound raw-material types are opening balance, purchase receipt, production-issue reversal, and adjustment in. Outbound types are production issue, purchase-receipt reversal, and adjustment out.

Inbound finished-goods types are opening balance, production receipt, dispatch reversal, and adjustment in. Finished-goods outbound movements include dispatch, warehouse damage write-off, and adjustment out.

Purchase receipt quantity cannot exceed the purchase line. Production receipt quantity equals good packets. Dispatch quantity equals the dispatch line. Opening balance is allowed only when the balance is zero.

On-hand quantity and value cannot fall below zero. Order verification reserves finished goods. Available quantity is on hand minus reserved. A verified order that is cancelled or closed releases the quantity that was not dispatched. Raw material is not reserved at the planning stage. The issue transaction fails when the material balance is short.

Damaged packets recorded on a production run do not enter finished-goods stock. Warehouse damage of packets already in stock is a `damage_write_off` movement.

## 7. BOM, yield, and costing

A BOM version states the packets it produces and the material required for that batch. Production scales the recipe:

planned usage = BOM material quantity × run planned packets / BOM output packets.

That planned quantity is copied onto the usage line. The first run that uses a BOM locks it. A changed recipe is a new version. Only one version of a product is active.

A run moves from planned, to material issued, to completed, to posted. Good quantity is empty until the run is completed. Posted quantities do not change.

Yield percent, yield variance, unexplained loss, and material variance are calculated from the stored quantities. They are not saved as their own columns.

Costing is weighted average, stored as the company costing method. Each issue snapshots unit cost and total cost. Cost per good packet is the sum of issued material cost divided by good packets. It is calculated for a posted run whose good quantity is greater than zero. Damage cost stays inside that material total, so good packets carry it. Labour and overhead are outside this version of the design.

## 8. Invoice, dispatch, and payment

The business path is verified order, one posted GST invoice, one or more dispatches, then payments.

Invoice lines and dispatch lines both reference the order line, so billed and shipped products stay tied to what was ordered. Net dispatched quantity cannot exceed the invoiced quantity or the ordered quantity.

Dispatch posting creates the finished-goods issue and reduces the reservation. An inter-state dispatch stores an e-way bill number when the invoice total meets the statutory threshold in force on that day.

Outstanding amount is the invoice total minus receipts plus reversals. A receipt cannot exceed the outstanding amount. A reversal cannot exceed the receipt it reverses. Payments are new rows. They are not edited.

## 9. Audit and transaction safety

Each posting action is one database transaction. It writes the business rows, the stock rows, and the audit row together, or it rolls back.

The transaction locks the stock balance it changes. Editable documents carry `row_version`. An update must carry the version that was read.

Posted invoices, payments, stock movements, posted production runs, locked BOM lines, and audit logs are append-only. A mistake is corrected by a reversal row, a cancellation that preserves amounts, or a stock adjustment with a reason.

Audit rows store the user, the action, the record, the time, and the old and new values. Times are stored with a time zone. Users are deactivated rather than deleted, so the audit trail can keep its foreign key.

## 10. Decisions recorded in this design

- One legal entity and one factory.
- One GST invoice per order, with partial delivery handled by multiple dispatches.
- Tax-exclusive prices and paise rounding, with the extra intra-state paise assigned to CGST.
- Separate raw-material and finished-goods ledgers.
- Weighted-average material cost, without labour or overhead.
- Production damage stays off the finished-goods ledger.
- Finished goods are reserved at order verification. Raw materials are reserved only by issuing them.
- Yield, variance, cost per packet, and outstanding balance are calculated, not stored.

## 11. Remaining design decisions

- Sales returns and credit notes are not part of this schema. Posted invoices can be cancelled only before dispatch and payment.
- The e-way bill threshold follows current law at posting time. It is not stored as a permanent rupee amount.
- Purchase input-tax credit is not calculated. Supplier GSTIN and state are stored for a later ledger.
- The factory has one stock location. Bins and warehouses are not modelled.
- A posted production run is not unposted. A stock correction after posting is an adjustment movement with a reason.

## 12. Project status

Database design documentation is complete. PostgreSQL implementation has not started.
