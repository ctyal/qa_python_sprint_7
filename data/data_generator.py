import random
import string
from datetime import datetime, timedelta
from api.courier_api import CourierApi

def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def generate_courier_payload():
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10)
    }

# Измененный прекод из задания
def register_new_courier_and_return_login_password():
    payload = generate_courier_payload()
    response = CourierApi().create_courier(payload)

    if response.status_code == 201:
        return payload
    return {}

def generate_order_payload(color=None):
    delivery_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    payload = {
        "firstName": "Иван",
        "lastName": "Петров",
        "address": "Москва, ул. Русская, д. 1",
        "metroStation": 4,
        "phone": "+7 800 355 35 35",
        "rentTime": 5,
        "deliveryDate": delivery_date,
        "comment": "Комментарий"
    }

    if color is not None:
        payload["color"] = color

    return payload
