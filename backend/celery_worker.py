from celery import Celery

celery_app = Celery("warehouse_inventory_management")

celery_app.config_from_object("celeryconfig")

# Do NOT use autodiscover_tasks here because
# the task modules are already listed in celeryconfig.py