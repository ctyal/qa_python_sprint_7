import pytest
from api.courier_api import CourierApi
from api.order_api import OrderApi
from data.data_generator import generate_courier_payload, register_new_courier_and_return_login_password

def _cleanup_courier(api, courier_data):
    if (
        not courier_data
        or not courier_data.get("login")
        or not courier_data.get("password")
    ):
        return
    login_response = api.login(
        {"login": courier_data["login"], "password": courier_data["password"]}
    )
    if login_response.status_code == 200:
        courier_id = login_response.json().get("id")
        if courier_id:
            api.delete_courier(courier_id)

@pytest.fixture
def courier_api():
    return CourierApi()

@pytest.fixture
def order_api():
    return OrderApi()

@pytest.fixture
def new_courier_data_lifecycle(courier_api): #Генерирует данные нового курьера и удаляет его после теста, если он был создан.
    payload = generate_courier_payload()
    yield payload
    _cleanup_courier(courier_api, payload)

@pytest.fixture
def create_new_courier_lifecycle(courier_api): #Регистрирует нового курьера и удаляет его после теста.
    courier = register_new_courier_and_return_login_password()
    assert courier, "Не удалось создать тестового курьера в фикстуре"
    yield courier
    _cleanup_courier(courier_api, courier)
