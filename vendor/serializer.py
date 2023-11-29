from rest_framework import serializers
from vendor.models import *


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendor
        fields="__all__"


class PurchaseorderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Purchaseorder
        fields="__all__"        