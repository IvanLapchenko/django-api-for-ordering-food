import json
import random
import requests
import string

from celery import shared_task
from django.http import JsonResponse
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt

from .models import Check, Printer


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


@shared_task
def generate_pdf(check_id):
    print('penis')
    # check = Check.objects.get(pk=check_id)
    # template = get_template('check.html')
    # html_content = template.render({'check': check})
    #
    # url = 'http://localhost:5001/'
    # data = {
    #     'contents': html_content
    # }
    # headers = {
    #     'Content-Type': 'application/json',
    # }
    # response = requests.post(url, data=json.dumps(data), headers=headers)
    #
    # with open('/file.pdf', 'wb') as f:
    #     f.write(response.content)
    #
    # check.status = Check.RENDERED
    # check.save()
