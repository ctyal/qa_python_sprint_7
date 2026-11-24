import allure
import pytest
from data.data_generator import generate_order_payload

@allure.epic('Учебный сервис Яндекс Самокат')
@allure.feature('Заказы')
@allure.story('Создание Заказа - Ручка /api/v1/orders')
class TestCreateOrder:
    @allure.title('Позитивный сценарий: создание заказа с разными вариантами цвета')
    @allure.description('Проверка создания заказа при выборе BLACK, GREY, обоих цветов или без указания цвета')
    @pytest.mark.positive
    @pytest.mark.parametrize("color", [
        ["BLACK"],
        ["GREY"],
        ["BLACK", "GREY"],
        [],
        None
    ], ids=[
        "Выбран Чёрный цвет",
        "Выбран Серый цвет",
        "Выбраны оба цвета",
        "Цвет не выбран",
        "Без поля цвета"
    ])
    def test_create_order_with_color_options_success(self, order_api, color):
        with allure.step(f'Генерация данных заказа: {color}'):
            payload = generate_order_payload(color)
            if color is None:
                payload.pop('color', None)
        with allure.step('Отправка запроса на создание заказа'):
            response = order_api.create_order(payload)
        with allure.step('Проверка ответа'):
            assert response.status_code == 201, \
                f"Ожидался статус 201, получен {response.status_code}. Тело: {response.text}"
            assert "track" in response.json(), \
                f"В ответе должен быть 'track' заказа, получено: {response.json()}"
            assert isinstance(response.json()["track"], int)

@allure.epic('Учебный сервис Яндекс Самокат')
@allure.feature('Заказы')
@allure.story('Список Заказов - Ручка /api/v1/orders')
class TestOrderList:
    @allure.title('Позитивный сценарий: получение списка заказов')
    @allure.description('Проверка получения списка существующих заказов')
    @pytest.mark.positive
    def test_get_orders_list_success(self, order_api):
        with allure.step('Отправка GET-запроса на получение списка заказов'):
            response = order_api.get_orders_list()
        with allure.step('Проверка статус-кода 200 и наличия списка заказов в ответе'):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}. Тело: {response.text}"
            assert "orders" in response.json(), \
                f"В ответе должен быть ключ 'orders', получено: {response.json()}"
            assert isinstance(response.json()["orders"], list), \
                "Значение по ключу 'orders' должно быть списком"
            assert len(response.json()["orders"]) > 0, \
                "Список заказов вернулся пустым"
            