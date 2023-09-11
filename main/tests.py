import json

from django.test import TestCase
from django.urls import reverse

from .models import Printer, Check
from .tasks import generate_pdf


class CreatePrinterViewTest(TestCase):

    def test_create_printer_post(self):
        data = {
            'name': 'Test Printer',
            'check_type': 'client',
            'point_id': 123,
        }

        expected_response = {
            'message': 'Printer created successfully'
        }

        initial_printer_count = Printer.objects.count()

        response = self.client.post(reverse('create_printer'), data)

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), expected_response)

        self.assertEqual(Printer.objects.count(), initial_printer_count + 1)

        self.assertEqual(len(Printer.objects.last().api_key), 32)

    def test_create_printer_invalid_method(self):
        response = self.client.get(reverse('create_printer'))

        self.assertEqual(response.status_code, 405)

        expected_error = {'message': 'Invalid request method'}
        self.assertEqual(response.json(), expected_error)

    def tearDown(self):
        Printer.objects.filter(name='Test Printer').delete()


class CreateChecksViewTest(TestCase):
    def setUp(self):
        self.printer = Printer.objects.create(
            name='Test Printer',
            api_key='test_api_key',
            check_type='client',
            point_id=123
        )

    def test_create_checks_post(self):
        data = {
            'point_id': self.printer.point_id,
            'order_id': 123,
            'order_items': ['item1', 'item2', 'item3'],
        }

        expected_response = {
            'message': 'Checks created;PDF generation started'
        }

        initial_check_count = Check.objects.count()

        response = self.client.post(reverse('create_checks'), json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.json(), expected_response)

        self.assertEqual(Check.objects.count(), initial_check_count + 1)

        self.assertTrue(generate_pdf.delay.called)

    def test_create_checks_invalid_method(self):
        response = self.client.get(reverse('create_checks'))

        self.assertEqual(response.status_code, 405)

        expected_error = {'message': 'Invalid request method'}
        self.assertEqual(response.json(), expected_error)

    def test_create_checks_invalid_input_data(self):
        invalid_data = {
            'point_id': self.printer.point_id,
            'order_items': ['item1', 'item2', 'item3'],
        }

        response = self.client.post(reverse('create_checks'), json.dumps(invalid_data), content_type='application/json')

        self.assertEqual(response.status_code, 400)

        expected_error = {'message': 'Invalid input data'}
        self.assertEqual(response.json(), expected_error)

    def tearDown(self):
        Printer.objects.filter(name='Test Printer').delete()
        Check.objects.filter(order_id=123).delete()
