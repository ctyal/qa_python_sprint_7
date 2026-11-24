import requests
import allure
from data.urls import Url

class BaseClient:
    def __init__(self):
        self.base_url = Url.URL

    @allure.step("Выполнение POST запроса")
    def post(self, endpoint, data=None, json=None, params=None):
        url = f"{self.base_url}{endpoint}"
        return requests.post(url, data=data, json=json, params=params)

    @allure.step("Выполнение GET запроса")
    def get(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        return requests.get(url, params=params)

    @allure.step("Выполнение DELETE запроса")
    def delete(self, endpoint, params=None):
        url = f"{self.base_url}{endpoint}"
        return requests.delete(url, params=params)
