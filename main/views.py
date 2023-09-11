import json
import random
import string

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Check, Printer
from .tasks import generate_pdf


@csrf_exempt
def create_printer(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        check_type = request.POST.get('check_type')
        point_id = request.POST.get('point_id')

        # Generate a random API key
        api_key = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))

        # Create a new Printer object
        printer = Printer.objects.create(
            name=name,
            api_key=api_key,
            check_type=check_type,
            point_id=point_id
        )
        printer.save()

        return JsonResponse({'message': 'Printer created successfully'})

    return JsonResponse({'message': 'Invalid request method'})


@csrf_exempt
def create_checks(request):
    if request.method != 'POST':
        return JsonResponse({'message': 'Invalid request method'}, status=405)

    try:
        data_from_client = json.loads(request.body)
        point_id = int(data_from_client.get('point_id'))
        order_data = data_from_client.get('order_items')
        order_id = data_from_client.get('order_id')
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({'message': 'Invalid input data'}, status=400)

    existing_checks = Check.objects.filter(order__contains={'order_id': order_id})

    if existing_checks.exists():
        return JsonResponse({'message': f'Checks for order_id {order_id} already exist'}, status=409)

    printers = Printer.objects.filter(point_id=point_id)

    if not printers:
        return JsonResponse({'message': f'No printers at point {point_id}'}, status=404)

    for printer in printers:
        check = Check.objects.create(
            printer_id=printer,
            type=printer.check_type,
            order=order_data,
        )

        generate_pdf.delay(check_id=check.id, order_id=order_id)

    return JsonResponse({'message': 'Checks created;PDF generation started'})
