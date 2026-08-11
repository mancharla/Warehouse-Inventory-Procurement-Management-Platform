Warehouse Inventory & Procurement Management Platform

1. Project Overview

The Warehouse Inventory & Procurement Management Platform is a backend-focused system designed to manage warehouse operations, inventory, suppliers, procurement, stock transfers, alerts, reports, and scheduled background activities.

The platform provides role-based access, secure authentication, inventory management, procurement workflows, real-time WebSocket notifications, and automated background processing using Celery and Redis.

The project was implemented primarily with FastAPI, SQLAlchemy, MySQL, JWT authentication, Celery, Redis, and WebSockets.

2. Main Objectives

The main objectives of the platform are:

Manage warehouses and warehouse users.

Manage inventory and stock quantities.

Manage suppliers.

Create and manage purchase orders.

Manage stock transfer operations.

Receive purchased stock.

Generate inventory-related alerts.

Provide real-time notifications through WebSockets.

Automate recurring inventory and reporting tasks.

Generate operational reports.

Maintain secure authentication and role-based authorization.

Maintain database schema changes using Alembic migrations.

3. Technology Stack

Backend

Python

FastAPI

Uvicorn

Database

MySQL

SQLAlchemy ORM

PyMySQL

Authentication and Security

JWT Authentication

Access Tokens

Refresh Tokens

Password Hashing

Role-Based Access Control (RBAC)

Database Migrations

Alembic

Background Processing

Celery

Redis

Celery Beat

Real-Time Communication

WebSockets

Data and Reports

Pandas

openpyxl

Report generation/export functionality

Development Tools

Git

GitHub

Python Virtual Environment

4. System Architecture

The project follows a layered backend architecture.

                    Client / Frontend
                           |
                           v
                    FastAPI REST API
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
      Routers          Services          WebSockets
          |                |                |
          +----------------+----------------+
                           |
                           v
                     SQLAlchemy ORM
                           |
                           v
                         MySQL

                           +
                           |
                           v
                    Celery Background
                       Task System
                           |
                           v
                         Redis
                           |
                           v
                      Celery Worker

                    Celery Beat Scheduler

Architecture flow

The client sends an HTTP request to FastAPI.

FastAPI routes the request to the appropriate API router.

Authentication and authorization are checked.

Business logic is handled by service-layer components.

SQLAlchemy communicates with MySQL.

For background processing, tasks are sent to Celery through Redis.

Celery Worker executes the background task.

Celery Beat schedules recurring tasks.

WebSockets provide real-time notifications to connected clients.

5. Authentication and Authorization

The platform implements JWT-based authentication.

Registration

Users can register with required account information and a role.

Login

After successful login, the system generates an authentication token.

The access token is used to authenticate API requests.

Refresh Token

A refresh token is used to obtain a new access token when the access token expires.

This avoids requiring the user to log in again every time the short-lived access token expires.

Role-Based Authorization

Different roles have different responsibilities.

Super Admin

Can manage:

Users

Warehouses

Suppliers

Inventory settings

Reports

System-level operations

Warehouse Manager

Can manage:

Warehouse inventory

Purchase orders

Stock transfer approvals

Receiving purchased goods

Inventory Staff

Can:

Add stock

Update stock

Create stock transfer requests

Work with inventory operations

Procurement Officer

Can:

Manage suppliers

Create purchase orders

Track procurement deliveries

Authorization checks prevent users from performing operations outside their assigned role.

6. Warehouse Management

Warehouse management supports the main warehouse information required by the platform.

Typical warehouse information includes:

Warehouse name

Warehouse code

Address

Capacity

Current utilization

Status

Manager information

Warehouse APIs are protected using authentication and role-based permissions.

7. Supplier Management

The supplier module manages supplier information used during procurement.

Supplier information includes:

Supplier name

Contact person

Supplier-related operational information

Procurement officers can manage suppliers and supplier-related procurement activities.

8. Inventory Management

The inventory module manages the quantity and state of products stored in warehouses.

Inventory operations include:

Adding stock

Updating stock

Checking available quantity

Receiving stock

Detecting low stock

Detecting out-of-stock products

Detecting over-stock situations

Cleaning negative stock values

Inventory reconciliation

The system also generates inventory alerts based on inventory conditions.

9. Purchase Order Management

Purchase orders are used to manage procurement activities.

The procurement workflow includes:

Supplier
   |
   v
Purchase Order
   |
   v
Approval
   |
   v
Delivery
   |
   v
Stock Received
   |
   v
Inventory Updated

The system also supports real-time purchase-order notifications.

For example:

purchase_order_approved

can be sent to connected clients when a purchase order is approved.

10. Stock Transfer Management

The platform supports transferring inventory between warehouse locations.

The transfer workflow can be represented as:

Transfer Request
       |
       v
Approval
       |
       v
Transfer Processing
       |
       v
Transfer Completed

Real-time notifications are provided through the transfer WebSocket.

Example event:

transfer_completed

with a transfer number such as:

TR-000001

11. Receiving Stock

When purchased inventory is received, the system can notify connected inventory clients.

Example event:

stock_received

Example notification data:

{
  "event": "stock_received",
  "po_number": "PO-000001",
  "product": "Dell Laptop",
  "quantity": 50
}

This allows the client application to immediately know that stock has been received.

12. Real-Time WebSocket Notifications

The project implements separate WebSocket channels for different operational areas.

Implemented WebSocket endpoints include:

/ws/alerts
/ws/purchase-orders
/ws/transfers
/ws/inventory
/ws/audits

Alert WebSocket

Used for inventory and alert notifications.

Example:

{
  "event": "low_stock",
  "product": "Dell Laptop",
  "quantity": 100
}

Purchase Order WebSocket

Used for purchase-order events.

Example:

{
  "event": "purchase_order_approved",
  "po_number": "PO-000001"
}

Transfer WebSocket

Used for stock transfer events.

Example:

{
  "event": "transfer_completed",
  "transfer_number": "TR-000001"
}

Inventory WebSocket

Used for inventory events.

Example:

{
  "event": "stock_received",
  "po_number": "PO-000001",
  "product": "Dell Laptop",
  "quantity": 50
}

Audit WebSocket

Used for inventory audit notifications.

Example:

{
  "event": "inventory_audit_due",
  "message": "Inventory audit is due. Please review and reconcile inventory."
}

13. WebSocket Testing

The WebSocket notification system was tested successfully.

The backend logs confirmed successful connections and notification delivery.

Example:

WebSocket /ws/alerts [accepted]
Alert WebSocket connected. Total: 1
Sending alert notification
Alert notification sent successfully

Similar successful tests were performed for:

Alerts

Purchase orders

Transfers

Inventory

Audits

The test HTTP endpoints returned:

200 OK

after sending the notifications.

14. Celery Background Processing

Celery is used for background and scheduled processing.

The Celery application is configured to use Redis as:

redis://localhost:6379/0

Redis acts as the message broker and result backend.

The Celery worker receives tasks from Redis and executes them.

15. Celery Tasks Implemented

The project contains background task modules for:

app/celery_tasks/inventory_tasks.py
app/celery_tasks/supplier_tasks.py
app/celery_tasks/report_tasks.py
app/celery_tasks/alert_tasks.py

The worker successfully discovered the following tasks:

app.celery_tasks.alert_tasks.check_out_of_stock
app.celery_tasks.alert_tasks.check_over_stock
app.celery_tasks.alert_tasks.generate_inventory_alerts

app.celery_tasks.inventory_tasks.check_low_stock
app.celery_tasks.inventory_tasks.cleanup_negative_stock
app.celery_tasks.inventory_tasks.reconcile_inventory

app.celery_tasks.report_tasks.generate_daily_inventory_report
app.celery_tasks.report_tasks.generate_procurement_report
app.celery_tasks.report_tasks.generate_transfer_report

app.celery_tasks.supplier_tasks.calculate_supplier_performance
app.celery_tasks.supplier_tasks.supplier_summary

16. Inventory Background Tasks

Reconcile Inventory

The reconciliation task:

Opens a database session.

Reads inventory records.

Checks for negative available quantities.

Corrects negative quantities.

Generates inventory alerts.

Performs the configured inventory audit notification operation.

Commits required database changes.

Closes the database session.

Low Stock Check

The low-stock task:

Reads inventory records.

Checks inventory conditions.

Uses the inventory alert service.

Generates low-stock alerts when applicable.

A successful test produced:

{
  "status": "success",
  "message": "Low stock check completed",
  "checked_records": 1,
  "alerts_generated": 0
}

Cleanup Negative Stock

This task finds inventory records with:

available_quantity < 0

and changes the available quantity to:

0

It also returns the number of corrected records.

17. Automated Alert Tasks

The project contains automated alert tasks for:

Inventory Alerts

generate_inventory_alerts

Out-of-Stock Check

check_out_of_stock

Over-Stock Check

check_over_stock

Example successful executions were observed:

out_of_stock_products: 0

processed_records: 1

over_stock_products: 0

These tasks allow the system to continuously monitor inventory conditions.

18. Supplier Background Tasks

Supplier-related scheduled tasks include:

calculate_supplier_performance
supplier_summary

These tasks are designed to process supplier-related information and generate supplier performance/summary data.

19. Automated Report Tasks

The project contains scheduled report tasks for:

generate_daily_inventory_report
generate_procurement_report
generate_transfer_report

These tasks automate report generation without requiring the user to manually start the process every time.

20. Celery Beat Scheduling

Celery Beat is used as the scheduler.

The configured schedules are:

Task

Schedule

Inventory reconciliation

Daily at 00:00

Low-stock check

Every 30 minutes

Cleanup negative stock

Daily at 01:00

Supplier performance

Daily at 02:00

Supplier summary

Daily at 02:30

Daily inventory report

Daily at 23:55

Procurement report

Daily at 23:56

Transfer report

Daily at 23:57

Inventory alerts

Every 15 minutes

Out-of-stock check

Every 20 minutes

Over-stock check

Every 30 minutes

Timezone:

Asia/Kolkata

The Celery Beat logs confirmed that scheduled tasks were being sent.

Example:

Scheduler: Sending due task low-stock-check
Scheduler: Sending due task inventory-alerts
Scheduler: Sending due task over-stock-check
Scheduler: Sending due task out-of-stock-check

21. Redis

Redis is used by Celery for:

Message brokering

Task communication

Result backend

Configured Redis URL:

redis://localhost:6379/0

The worker successfully connected to Redis:

Connected to redis://localhost:6379/0

This confirmed that Redis was running and accessible to the Celery worker.

22. Windows Celery Worker Configuration

During development on Windows, the default Celery prefork worker encountered Windows process/permission errors involving Billiard.

The error included:

PermissionError: [WinError 5] Access is denied

and:

OSError: [WinError 6] The handle is invalid

The worker was therefore run using the solo pool:

celery -A celery_worker:celery_app worker --loglevel=info --pool=solo

This successfully executed the scheduled tasks.

The worker reached:

celery@DESKTOP-6G0II7F ready.

and successfully processed tasks.

23. Celery Configuration

The project uses:

broker_url = "redis://localhost:6379/0"
result_backend = "redis://localhost:6379/0"

timezone = "Asia/Kolkata"
enable_utc = False

task_serializer = "json"
accept_content = ["json"]
result_serializer = "json"

The Celery configuration imports:

app.celery_tasks.inventory_tasks
app.celery_tasks.supplier_tasks
app.celery_tasks.report_tasks
app.celery_tasks.alert_tasks

This allows Celery to discover the implemented tasks.

24. Database and ORM

SQLAlchemy is used as the ORM.

The application creates database sessions through:

SessionLocal()

Tasks use a database session to:

Query records.

Modify records.

Commit successful changes.

Roll back when errors occur.

Close the session in the finally block.

This prevents database sessions from remaining open after task execution.

25. Alembic Database Migrations

Alembic is used to manage database schema changes.

Typical migration workflow:

alembic revision --autogenerate -m "migration message"

followed by:

alembic upgrade head

The first command generates a migration based on model/schema changes.

The second command applies the migration to the database.

Alembic allows database schema changes to be tracked instead of manually modifying the database each time.

26. Error Handling

The backend uses exception handling in database operations.

Typical pattern:

try
    perform operation
except
    rollback
finally
    close database session

For background tasks, errors are raised after rollback so Celery can detect the task failure.

For WebSocket notification operations, notification failures can be caught separately so that notification errors do not unnecessarily stop the main inventory operation.

27. Notification Architecture

The notification flow is:

Business Event
      |
      v
Notification Service
      |
      v
WebSocket Manager
      |
      v
Connected Clients

Examples of business events:

low_stock
purchase_order_approved
transfer_completed
stock_received
inventory_audit_due

The notification service sends the event to the appropriate WebSocket connections.

The backend logs confirmed:

Sending to ... connections: 1
... notification sent successfully

28. Testing Performed

The following functionality was tested during development.

WebSocket Tests

Alert notification

Purchase-order approval notification

Transfer completion notification

Stock received notification

Inventory audit notification

Celery Tests

Low-stock check

Out-of-stock check

Inventory alert generation

Over-stock check

Example successful task:

Task app.celery_tasks.inventory_tasks.check_low_stock
succeeded

Result:

{
  "status": "success",
  "message": "Low stock check completed",
  "checked_records": 1,
  "alerts_generated": 0
}

29. Project Folder Structure

The important backend structure is approximately:

backend/
│
├── app/
│   ├── celery_tasks/
│   │   ├── alert_tasks.py
│   │   ├── inventory_tasks.py
│   │   ├── report_tasks.py
│   │   ├── supplier_tasks.py
│   │   └── __init__.py
│   │
│   ├── models/
│   │   └── database models
│   │
│   ├── routers/
│   │   └── API routes
│   │
│   ├── services/
│   │   ├── inventory_alert_service
│   │   ├── notification_service
│   │   └── other business services
│   │
│   └── database/
│       └── database configuration
│
├── alembic/
│   └── database migrations
│
├── celery_worker.py
├── celeryconfig.py
├── requirements.txt
└── README.md

30. Running the Project

Step 1: Activate Virtual Environment

Windows PowerShell:

.\venv\Scripts\Activate.ps1

Step 2: Start Redis

Redis must be running before starting Celery.

Verify Redis is available on:

localhost:6379

Step 3: Start FastAPI

Example:

uvicorn app.main:app --reload

The exact application module should match the project's main.py location.

Step 4: Start Celery Worker

For Windows development, use:

celery -A celery_worker:celery_app worker --loglevel=info --pool=solo

A successful worker should eventually show:

Connected to redis://localhost:6379/0

and:

celery@DESKTOP-... ready.

Step 5: Start Celery Beat

Open another terminal:

celery -A celery_worker:celery_app beat --loglevel=info

Beat will schedule tasks according to celeryconfig.py.

31. Important Development Commands

Start FastAPI

uvicorn app.main:app --reload

Start Celery Worker

celery -A celery_worker:celery_app worker --loglevel=info --pool=solo

Start Celery Beat

celery -A celery_worker:celery_app beat --loglevel=info

Create Alembic Migration

alembic revision --autogenerate -m "description"

Apply Migrations

alembic upgrade head

32. Complete Functional Flow

The overall platform can be understood as:

User Login
    |
    v
JWT Authentication
    |
    v
Role Authorization
    |
    v
Warehouse / Inventory / Supplier / Procurement Operations
    |
    +----------------------+
    |                      |
    v                      v
Database              Business Events
    |                      |
    |                      v
    |               Notification Service
    |                      |
    |                      v
    |                  WebSockets
    |
    v
Celery Background Tasks
    |
    v
Redis Broker
    |
    v
Celery Worker
    |
    v
Inventory / Supplier / Report / Alert Processing

Celery Beat
    |
    v
Schedules Background Tasks Automatically

33. Current Implementation Status

The following major components have been implemented and tested:

FastAPI backend

MySQL database integration

SQLAlchemy ORM

JWT authentication

Refresh-token based authentication flow

Role-based authorization

Warehouse management

Inventory management

Supplier management

Purchase-order management

Stock-transfer functionality

Inventory alerts

WebSocket notifications

Alert WebSocket

Purchase-order WebSocket

Transfer WebSocket

Inventory WebSocket

Audit WebSocket

Redis integration

Celery worker

Celery Beat scheduler

Scheduled inventory tasks

Scheduled alert tasks

Scheduled supplier tasks

Scheduled report tasks

Inventory reconciliation

Negative-stock cleanup

Low-stock checking

Out-of-stock checking

Over-stock checking

Database transaction handling

Alembic migrations

Background task testing

WebSocket notification testing

34. Known Development Note

The Celery worker initially produced Windows Billiard process errors when using the default prefork pool:

PermissionError: [WinError 5] Access is denied
OSError: [WinError 6] The handle is invalid

The project was successfully run using:

--pool=solo

This is the development configuration used on Windows for reliable local execution.

35. What This Project Demonstrates

This assignment demonstrates practical backend development involving:

REST API development

Authentication and authorization

Database design and ORM usage

Transaction handling

Background task processing

Scheduled automation

Message brokering

Real-time communication

Inventory business logic

Procurement workflows

Alert systems

Report automation

Database migration management

Error handling

Modular service-based architecture

The combination of FastAPI + SQLAlchemy + MySQL + JWT + Redis + Celery + WebSockets provides a backend architecture suitable for an inventory and procurement management system.

36. Summary

The Warehouse Inventory & Procurement Management Platform is a backend system that centralizes warehouse inventory, procurement, supplier, stock-transfer, alert, and reporting operations.

FastAPI handles the API layer, SQLAlchemy manages database communication, MySQL stores application data, JWT provides authentication, Redis provides the messaging layer for Celery, Celery executes background tasks, Celery Beat schedules recurring operations, and WebSockets provide real-time operational notifications.

The project has been tested through API, WebSocket, and Celery task execution, including successful scheduled task processing and real-time notification delivery.