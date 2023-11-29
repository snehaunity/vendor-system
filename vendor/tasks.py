from celery import shared_task
from django.utils import timezone
from django.db.models import Avg
from django.db import models
from .models import Vendor, Historical_Performance_Model

def update_vendor_performance_metrics():
    vendors = Vendor.objects.all()
    #TODO We can use batch processing instead of getting all vendor at once, but keeping things simple for now

    for vendor in vendors:
        total_orders = vendor.purchaseorder_set.count()
        on_time_delivery_count = vendor.purchaseorder_set.filter(status='Delivered', delivery_date__lte=models.F('acknowledgment_date')).count()
        quality_rating_avg = vendor.purchaseorder_set.filter(quantity_rating__isnull=False).aggregate(Avg('quantity_rating'))['quantity_rating__avg']
        average_response_time = vendor.purchaseorder_set.filter(acknowledgment_date__isnull=False).aggregate(Avg(models.F('acknowledgment_date') - models.F('issue_date')))['acknowledgment_date__avg']
        fulfillment_rate = on_time_delivery_count / total_orders * 100 if total_orders > 0 else 0

        # Save historical performance metrics
        history_data = Historical_Performance_Model(
            vendor=vendor,
            date = timezone.now(),
            on_time_delivery_rate=fulfillment_rate,
            quality_rating_avg=quality_rating_avg,
            average_response_time=average_response_time,
            fulfillment_rate=fulfillment_rate,
        )
        history_data.save()