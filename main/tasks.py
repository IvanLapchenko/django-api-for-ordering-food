import json
import requests
from django.template.loader import get_template
import os

os.path.join('C:/Users/lapch/PycharmProjects/SheepFish')
from SheepFish.celery import app
from .models import Check


@app.task(track_started=True)
def generate_pdf(check_id):
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

    with open('/file.pdf', 'wb') as f:
        f.write(response.content)

    check.status = Check.RENDERED
    check.save()
