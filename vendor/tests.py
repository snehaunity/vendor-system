from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from datetime import datetime
from .models import Vendor, Purchaseorder, Historical_Performance_Model

class VendorAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(
            name='Test Vendor',
            contact_details='Contact Details',
            address='Vendor Address',
            vendor_code='V123',
            on_time_delivery_rate=95.0,
            quality_rating_avg=4.5,
            average_response_time=2.5,
            fulfillment_rate=98.0,
        )
        self.purchase_order = Purchaseorder.objects.create(
            po_number='PO123',
            vendor=self.vendor,
            order_date=datetime.now(),
            delivery_date=datetime.now(),
            items={'item': 'Product A'},
            quantity=10,
            status='Delivered',
            quantity_rating=4.0,
            issue_date=datetime.now(),
            acknowledgment_date=datetime.now(),
        )
        self.historical_performance = Historical_Performance_Model.objects.create(
            vendor=self.vendor,
            date=datetime.now(),
            on_time_delivery_rate=90.0,
            quality_rating_avg=4.2,
            average_response_time=2.8,
            fulfillment_rate=96.0,
        )

    def test_vendor_model(self):
        self.assertEqual(str(self.vendor), 'Test Vendor')

    def test_purchaseorder_model(self):
        self.assertEqual(str(self.purchase_order), 'PO123')

    def test_historical_performance_model(self):
        print(self.historical_performance, "self.historical_performance")
        self.assertIn('Test Vendor', str(self.historical_performance))

    def test_vendor_performance_history_endpoint(self):
        url = reverse('vendor_performance_history', args=[self.vendor.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIn('vendor_name', data)
        self.assertIn('performance_history', data)

        self.assertEqual(data['vendor_name'], self.vendor.name)
        self.assertIn('date', data['performance_history'])
        self.assertIn('on_time_delivery_rate', data['performance_history'])
        self.assertIn('quality_rating_avg', data['performance_history'])
        self.assertIn('average_response_time', data['performance_history'])
        self.assertIn('fulfillment_rate', data['performance_history'])

    def test_vendor_performance_history_endpoint_with_invalid_vendor_id(self):
        invalid_vendor_id = 9999  # An invalid vendor ID
        url = reverse('vendor_performance_history', args=[invalid_vendor_id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_vendor(self):
        url = reverse('crudvendor-list')
        data = {
            'name': 'New Vendor',
            'contact_details': 'Contact Details',
            'address': 'New Vendor Address',
            'vendor_code': 'V124',
            'on_time_delivery_rate': 96.0,
            'quality_rating_avg': 4.8,
            'average_response_time': 2.3,
            'fulfillment_rate': 97.5,
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_vendor = Vendor.objects.get(name='New Vendor')
        self.assertIsNotNone(new_vendor)

    def test_update_vendor(self):
        url = reverse('crudvendor-detail', args=[self.vendor.pk])
        data = {'name': 'Updated Vendor Name'}

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_vendor = Vendor.objects.get(pk=self.vendor.pk)
        self.assertEqual(updated_vendor.name, 'Updated Vendor Name')

    def test_delete_vendor(self):
        url = reverse('crudvendor-detail', args=[self.vendor.pk])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Vendor.DoesNotExist):
            Vendor.objects.get(pk=self.vendor.pk)

    def test_create_purchaseorder(self):
        url = reverse('crudpurchaseorder-list')
        data = {
            'po_number': 'PO124',
            'vendor': self.vendor.pk,
            'order_date': datetime.now().isoformat(),
            'delivery_date': datetime.now().isoformat(),
            'items': {'item': 'Product B'},
            'quantity': 15,
            'status': 'Shipped',
            'quantity_rating': 4.5,
            'issue_date': datetime.now().isoformat(),
            'acknowledgment_date': datetime.now().isoformat(),
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_purchase_order = Purchaseorder.objects.get(po_number='PO124')
        self.assertIsNotNone(new_purchase_order)

    def test_update_purchaseorder(self):
        url = reverse('crudpurchaseorder-detail', args=[self.purchase_order.pk])
        data = {'po_number': 'Updated PO Number'}

        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        updated_purchase_order = Purchaseorder.objects.get(pk=self.purchase_order.pk)
        self.assertEqual(updated_purchase_order.po_number, 'Updated PO Number')

    def test_delete_purchaseorder(self):
        url = reverse('crudpurchaseorder-detail', args=[self.purchase_order.pk])

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        with self.assertRaises(Purchaseorder.DoesNotExist):
            Purchaseorder.objects.get(pk=self.purchase_order.pk)
