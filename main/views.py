from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Printer
import random
import string


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



# @csrf_exempt
# def generate_check(request, order_id):
#     if request.method == 'POST':
#
#         check_data = request.POST
#         order = Order.objects.get(pk=order_id)
#         check = Check.objects.create(
#             order=order,
#             pdf_link=check_data['pdf_link'],
#             status=check_data['status'],
#             type=check_data['type']
#         )
#
#         response_data = {
#             'order_id': check.order_id,
#             'pdf_link': check.pdf_link.url,
#             'status': check.status,
#             'type': check.type
#         }
#         return JsonResponse(response_data)
#     else:
#         return JsonResponse({'error': 'Invalid request method'})

