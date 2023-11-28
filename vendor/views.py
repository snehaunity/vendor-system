from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from vendor.serializer import VendorSerializer,PurchaseorderSerializer
from rest_framework import viewsets
from vendor.models import Vendor,Purchaseorder




# @api_view(["post"])
# def create_vendor(request):
#     data=request.data
#     serializer=VendorSerializer(data=data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data,status=200)
#     else:
#         return Response(serializer.errors,status=403)


class CrudVendor(viewsets.ModelViewSet):
    serializer_class=VendorSerializer
    queryset=Vendor.objects.all()

class CrudPurchaseorder(viewsets.ModelViewSet):
    serializer_class=PurchaseorderSerializer
    queryset=Purchaseorder.objects.all()  