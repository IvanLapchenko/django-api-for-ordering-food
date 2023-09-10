import requests
import json

url = 'http://localhost:8000/api/create_check/'


data = {
    'point_id': 4,
    'order': json.dumps({'order_id': 123, 'order_items': ['item1', 'item2', 'item3']})
}


response = requests.post(url, data=data)

if response.status_code == 200:
    print('Success:', response.json())
else:
    print('Error:', response.json())
