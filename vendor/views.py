from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from vendor.serializer import VendorSerializer,PurchaseorderSerializer
from rest_framework import viewsets, status
from vendor.models import Vendor,Purchaseorder, Historical_Performance_Model




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

@api_view(['GET'])
def vendor_performance_history(request, vendor_id):
    try:
        vendor_with_history = Vendor.objects.select_related('historical_performance_model').get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

    # Access the associated HistoricalPerformance using vendor_with_history.historical_performance_model
    history_data = vendor_with_history.historical_performance_model

    # Return the historical performance metrics
    response_data = {
        'vendor_name': vendor_with_history.name,
        'performance_history': {
            'date': history_data.date,
            'on_time_delivery_rate': history_data.on_time_delivery_rate,
            'quality_rating_avg': history_data.quality_rating_avg,
            'average_response_time': history_data.average_response_time,
            'fulfillment_rate': history_data.fulfillment_rate,
        }
    }

    return Response(response_data, status=status.HTTP_200_OK)