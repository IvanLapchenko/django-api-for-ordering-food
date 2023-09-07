import json
import requests
from django.template.loader import get_template
import os

from celery import shared_task
from .models import Check


@shared_task()
def generate_pdf(check_id: int):
    check = Check.objects.get(pk=check_id)
    template = get_template('check.html')
    html_content = template.render({'check': check})

    url = 'http://localhost:5001/'
    data = {
        'contents': html_content
    }
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    with open("../media/pdf/pdfile.pdf", "w") as f:
        print('some')
        f.write(response.content)
        print(f)

    check.status = Check.RENDERED
    check.save()
