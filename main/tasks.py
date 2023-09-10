from pathlib import Path
import json
import base64
import requests
from django.template.loader import get_template

from celery import shared_task
from .models import Check


@shared_task()
def generate_pdf(check_id: int, order_id: int):
    check = Check.objects.get(pk=check_id)
    template = get_template('check.html')
    html_content = template.render({'check': check})
    base64_encoded_html_check = base64.b64encode(html_content.encode()).decode()

    url = 'http://localhost:5001/'
    data = {
        'contents': base64_encoded_html_check
    }
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)

    root_folder = Path(__file__).parents[1]
    pdf_path = root_folder / "media/pdf/"

    with open(f"{pdf_path}\\{order_id}_{check.type}.pdf", "wb") as f:
        f.write(response.content)

    check.status = Check.RENDERED
    check.save()
