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
    if request.method == 'POST':
        try:
            point_id = int(request.POST.get('point_id'))
            order_data = json.loads(request.POST.get('order'))
        except (ValueError, TypeError, json.JSONDecodeError):
            return JsonResponse({'message': 'Invalid input data'}, status=400)

        printers = Printer.objects.filter(point_id=point_id)

        for printer in printers:
            check = Check.objects.create(
                printer_id=printer,
                type=printer.check_type,
                order=order_data,
                status=Check.NEW
            )
            generate_pdf.apply_async(args=(check.id,))

        return JsonResponse({'message': 'Checks created;PDF generation started'})

    return JsonResponse({'message': 'Invalid request method'}, status=405)



