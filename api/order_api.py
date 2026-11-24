import allure
from api.base_api import BaseClient
from data.urls import Endpoint

class OrderApi(BaseClient):
    @allure.step('Создание заказа')
    def create_order(self, payload):
        return self.post(Endpoint.CREATE_ORDER, json=payload)

    @allure.step('Получение списка всех заказов')
    def get_orders_list(self, params=None):
        if params is None:
            params = {"limit": 5}
        return self.get(Endpoint.GET_ORDERS, params=params)
