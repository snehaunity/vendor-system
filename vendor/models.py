from django.db import models

# Create your models here.
class Vendor(models.Model):
    name=models.CharField(max_length=500)
    contact_details=models.TextField(null=True,blank=True)
    address=models.TextField(max_length=500)
    vendor_code=models.CharField(null=True,blank=True,unique=True,max_length=30)
    on_time_delivery_rate=models.FloatField(blank=True,null=True)
    quality_rating_avg=models.FloatField(blank=True,null=True)
    average_response_time=models.FloatField(blank=True,null=True)
    fulfillment_rate=models.FloatField(blank=True,null=True)
    
    def __str__(self) -> str:
        return self.name
    

class Purchaseorder(models.Model):
    po_number=models.CharField(unique=True,null=True,blank=True,max_length=50)
    vendor=models.ForeignKey(to=Vendor,on_delete=models.CASCADE)  
    order_date=models.DateTimeField(null=True)
    delivery_date=models.DateTimeField(null=True)
    items=models.JSONField()
    quantity=models.IntegerField(null=True,blank=True)
    status=models.CharField(max_length=250,null=True,blank=True)
    quantity_rating=models.FloatField(blank=True,null=True)
    issue_date=models.DateTimeField(null=True,blank=True)
    acknowledgment_date=models.DateTimeField(null=True,blank=True)

    def __str__(self) -> str:
        return self.po_number


class Historical_Performance_Model(models.Model):
    vendor=models.OneToOneField(to=Vendor,on_delete=models.CASCADE)
    date=models.DateTimeField(null=True,blank=True)
    on_time_delivery_rate=models.FloatField(blank=True,null=True)
    quality_rating_avg=models.FloatField(null=True,blank=True)
    average_response_time=models.FloatField(null=True,blank=True)
    fulfillment_rate=models.FloatField(null=True,blank=True)

    def __str__(self) -> str:
        return self.vendor.name