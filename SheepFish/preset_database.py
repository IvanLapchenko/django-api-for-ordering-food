import requests


def create_printers(check_type):
    url = 'http://localhost:8000/api/create_printer/'

    for point_id in range(1, 6):
        data = {
            'name': f'{check_type}_printer_{point_id}',
            'check_type': check_type,
            'point_id': point_id
        }
        requests.post(url, data=data)


create_printers('client')
create_printers('kitchen')
