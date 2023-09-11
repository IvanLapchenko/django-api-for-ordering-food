from django.shortcuts import render, redirect

import sys
sys.path.append('../')

from main.models import Printer, Check


def admin_view(request):
    printers = Printer.objects.all()
    checks = Check.objects.all()

    sort_by = request.GET.get('sort_by', 'printer')
    if sort_by == 'type':
        checks = checks.order_by('type')
    elif sort_by == 'status':
        checks = checks.order_by('status')

    return render(request, 'admin.html', {'printers': printers, 'checks': checks})



