import requests
import json

url = 'http://localhost:8000/api/create_check/'  # Replace with your actual URL

# Sample data for the POST request
data = {
    'point_id': 1,  # Replace with the desired point_id
    'order': json.dumps(['item1', 'item2', 'item3'])  # Replace with your order data
}

response = requests.post(url, data=data)

if response.status_code == 200:
    print('Success:', response.json())
else:
    print('Error:', response.json())

# headers = {
#     'Content-Type': 'application/json',
# }
# url = 'http://localhost:5001/'
# response = requests.post(url, data=json.dumps({'contents': 'some'}), headers=headers)
# print(response.content)