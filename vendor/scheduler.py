# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from .tasks import update_vendor_performance_metrics
import atexit

scheduler = BackgroundScheduler()

def update_metrics_job():
    update_vendor_performance_metrics()
    print("Metrics Updated")

# Schedule the job to run every 60 minutes
scheduler.add_job(update_metrics_job, 'interval', minutes=60)

# Start the scheduler
scheduler.start()

# Ensure that the scheduler is shut down when the Django app is stopped
atexit.register(lambda: scheduler.shutdown())
