import allure
from api.base_api import BaseClient
from data.urls import Endpoint

class CourierApi(BaseClient):
    @allure.step('Регистрация нового курьера')
    def create_courier(self, payload):
            return self.post(Endpoint.CREATE_COURIER, json=payload)

    @allure.step('Авторизация курьера')
    def login(self, payload):
        return self.post(Endpoint.LOGIN_COURIER, json=payload)

    @allure.step("Удаление курьера по ID")
    def delete_courier(self, courier_id):
        return self.delete(Endpoint.DELETE_COURIER.format(courier_id))
    