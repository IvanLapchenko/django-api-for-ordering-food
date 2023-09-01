# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order, Check


@csrf_exempt
def create_order(request):
    if request.method == 'POST':

        order_data = request.POST
        order = Order.objects.create(
            order_number=order_data['order_number'],
            order_type=order_data['order_type']
        )

        response_data = {
            'order_number': order.order_number,
            'order_type': order.order_type,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})


@csrf_exempt
def generate_check(request, order_id):
    if request.method == 'POST':

        check_data = request.POST
        order = Order.objects.get(pk=order_id)
        check = Check.objects.create(
            order=order,
            pdf_link=check_data['pdf_link'],
            status=check_data['status'],
            type=check_data['type']
        )

        response_data = {
            'order_id': check.order_id,
            'pdf_link': check.pdf_link.url,
            'status': check.status,
            'type': check.type
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})

