from django.apps import AppConfig
import atexit
from apscheduler.schedulers.background import BackgroundScheduler


class VendorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vendor"

    def ready(self):
        # Import the scheduler-related modules here to ensure they are imported after app registry is ready
        from .scheduler import update_metrics_job

        scheduler = BackgroundScheduler()

        # Schedule your job to run every 60 minutes
        scheduler.add_job(update_metrics_job, 'interval', minutes=60)

        # Start the scheduler
        scheduler.start()

        # Ensure that the scheduler is shut down when the Django app is stopped
        atexit.register(lambda: scheduler.shutdown())
