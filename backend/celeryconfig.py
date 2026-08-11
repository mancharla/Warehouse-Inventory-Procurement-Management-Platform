from celery.schedules import crontab

broker_url = "redis://localhost:6379/0"

result_backend = "redis://localhost:6379/0"

timezone = "Asia/Kolkata"

enable_utc = False

task_serializer = "json"

accept_content = ["json"]

result_serializer = "json"

imports = (
    "app.celery_tasks.inventory_tasks",
    "app.celery_tasks.supplier_tasks",
    "app.celery_tasks.report_tasks",
    "app.celery_tasks.alert_tasks",
)

beat_schedule = {

    "inventory-reconciliation": {

        "task": "app.celery_tasks.inventory_tasks.reconcile_inventory",

        "schedule": crontab(hour=0, minute=0),
    },

    "low-stock-check": {

        "task": "app.celery_tasks.inventory_tasks.check_low_stock",

        "schedule": crontab(minute="*/30"),
    },

    "cleanup-negative-stock": {

        "task": "app.celery_tasks.inventory_tasks.cleanup_negative_stock",

        "schedule": crontab(hour=1, minute=0),
    },

    "supplier-performance": {

        "task": "app.celery_tasks.supplier_tasks.calculate_supplier_performance",

        "schedule": crontab(hour=2, minute=0),
    },

    "supplier-summary": {

        "task": "app.celery_tasks.supplier_tasks.supplier_summary",

        "schedule": crontab(hour=2, minute=30),
    },

    "daily-inventory-report": {

        "task": "app.celery_tasks.report_tasks.generate_daily_inventory_report",

        "schedule": crontab(hour=23, minute=55),
    },

    "procurement-report": {

        "task": "app.celery_tasks.report_tasks.generate_procurement_report",

        "schedule": crontab(hour=23, minute=56),
    },

    "transfer-report": {

        "task": "app.celery_tasks.report_tasks.generate_transfer_report",

        "schedule": crontab(hour=23, minute=57),
    },

    "inventory-alerts": {

        "task": "app.celery_tasks.alert_tasks.generate_inventory_alerts",

        "schedule": crontab(minute="*/15"),
    },

    "out-of-stock-check": {

        "task": "app.celery_tasks.alert_tasks.check_out_of_stock",

        "schedule": crontab(minute="*/20"),
    },

    "over-stock-check": {

        "task": "app.celery_tasks.alert_tasks.check_over_stock",

        "schedule": crontab(minute="*/30"),
    },
}