
# System Architecture

## 1. Project Overview

The NIT CDI Order-to-Audit Management System is a centralized web application designed for small-scale food manufacturing businesses.

It integrates sales, inventory, production, GST billing, product costing and auditing.

## 2. Technology Stack

- Frontend: React.js
- Styling: Tailwind CSS
- Backend: Python FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy
- Authentication: JWT
- Version Control: Git and GitHub
- Deployment: Docker

## 3. User Roles

1. Salesman
2. Factory Admin
3. Production Supervisor
4. Accountant / Auditor
5. Owner

## 4. Application Modules

1. Authentication and Role Management
2. Sales and Order Management
3. Inventory Management
4. BOM and Production Management
5. GST Billing
6. Product Costing
7. Reports and Auditing

## 5. Sales Workflow

Salesman Order
→ Admin Verification
→ GST Invoice
→ Dispatch
→ Finished Goods Stock Reduction
→ Payment and Receivables

## 6. Production Workflow

Purchase
→ Raw Material Inventory
→ BOM-based Material Issue
→ Production Run
→ Actual Output and Wastage
→ Finished Goods Inventory
→ Production Variance

## 7. Database

PostgreSQL will store:

- Users and roles
- Customers and suppliers
- Products and raw materials
- Bills of Materials
- Purchases
- Production runs
- Stock movements
- Orders and invoices
- Payments

## 8. Design Principles

- Role-based access control
- Ledger-based inventory tracking
- Accurate financial calculations
- Traceable stock movements
- Automated production variance calculations
- Audit trail for important transactions

## 9. Project Status

System architecture documentation in progress.
