import allure
import pytest

@allure.epic('Учебный сервис Яндекс Самокат')
@allure.feature('Курьеры')
@allure.story('Создание Курьера - Ручка /api/v1/courier')
class TestCreateCourier:
    @allure.title('Позитивный сценарий: создание курьера')
    @allure.description('Проверка создания курьера с корректными и полными данными')
    @pytest.mark.positive
    def test_create_courier_success(self, courier_api,new_courier_data_lifecycle):
        with allure.step('Отправка запроса на создание курьера'):
            response = courier_api.create_courier(new_courier_data_lifecycle)
        with allure.step('Проверка ответа'):
            assert response.status_code == 201, \
                f"Ожидался статус 201, получен {response.status_code}. Тело: {response.text}"
            assert response.json() == {"ok": True}, \
                f"Ожидалось {{'ok': True}}, получено {response.json()}"

    @allure.title('Позитивный сценарий: создание курьера без имени')
    @allure.description('Проверка создания курьера с отсутствующим необязательным полем firstName')
    @pytest.mark.positive
    def test_create_courier_without_firstname(self, courier_api, new_courier_data_lifecycle):
        with allure.step('Удаление поля firstName из данных'):
            del new_courier_data_lifecycle['firstName']          
        with allure.step('Отправка запроса на создание курьера'):
            response = courier_api.create_courier(new_courier_data_lifecycle)
        with allure.step('Проверка ответа'):
            assert response.status_code == 201, \
                f"Ожидался статус 201, получен {response.status_code}. Тело: {response.text}"
            assert response.json() == {"ok": True}, \
                f"Ожидалось {{'ok': True}}, получено {response.json()}"

    @allure.title('Негативный сценарий: создание курьера с отсутствующим полем')
    @allure.description('Проверка создания курьера, когда отсутствует одно из обязательных полей (login или password)')
    @pytest.mark.negative
    @pytest.mark.parametrize('missing_field', ['login', 'password'], ids=['Нет поля login','Нет поля password'])
    def test_create_courier_missing_field_fail(self, courier_api, new_courier_data_lifecycle, missing_field):
        with allure.step(f'Удаление поля {missing_field} из данных'):
            del new_courier_data_lifecycle[missing_field]
        with allure.step('Отправка запроса на создание курьера'):
            response = courier_api.create_courier(new_courier_data_lifecycle)
        with allure.step('Проверка ошибки валидации'):
            assert response.status_code == 400, \
                f"Ожидался статус 400, получен {response.status_code}. Тело: {response.text}"
            expected_error = "Недостаточно данных для создания учетной записи"
            assert expected_error in response.text, \
                f"Ожидалось сообщение '{expected_error}', получено: {response.text}"

    @allure.title('Негативный сценарий: создание курьера без login и password')
    @allure.description('Проверка создания курьера, когда отсутствуют оба обязательных поля (login и password)')
    @pytest.mark.negative
    def test_create_courier_missing_both_fields_fail(self, courier_api, new_courier_data_lifecycle):
        with allure.step('Удаление полей login и password из данных'):
            del new_courier_data_lifecycle['login']
            del new_courier_data_lifecycle['password']

        with allure.step('Отправка запроса на создание курьера'):
            response = courier_api.create_courier(new_courier_data_lifecycle)

        with allure.step('Проверка ошибки валидации'):
            assert response.status_code == 400, \
                f"Ожидался статус 400, получен {response.status_code}. Тело: {response.text}"
            expected_error = "Недостаточно данных для создания учетной записи"
            assert expected_error in response.text, \
                f"Ожидалось сообщение '{expected_error}', получено: {response.text}"

    @allure.title('Негативный сценарий: создание курьера с пустыми значением поля')
    @allure.description('Проверка создания курьера, когда пустое одно из обязательных полей (login или password)')
    @pytest.mark.negative
    @pytest.mark.parametrize('empty_field', ['login', 'password'], ids=['Пустое поле login','Пустое поле password'])
    def test_create_courier_empty_field_fail(self, courier_api, new_courier_data_lifecycle, empty_field):
        with allure.step(f'Установка пустого значения для поля {empty_field}'):
            new_courier_data_lifecycle[empty_field] = ""
        with allure.step(f'Отправка запроса с пустым полем: {empty_field}'):
            response = courier_api.create_courier(new_courier_data_lifecycle)
        with allure.step('Проверка ошибки валидации'):
            assert response.status_code == 400, \
                f"Ожидался статус 400, получен {response.status_code}. Тело: {response.text}"
            expected_error = "Недостаточно данных для создания учетной записи"
            assert expected_error in response.text, \
                f"Ожидалось сообщение '{expected_error}', получено: {response.text}"

    @allure.title('Негативный сценарий: создание курьера с пустыми login и password')
    @allure.description('Проверка создания курьера, когда пустые оба обязательных поля (login и password)')
    @pytest.mark.negative
    def test_create_courier_empty_both_fields_fail(self, courier_api, new_courier_data_lifecycle):
        with allure.step(f'Установка пустого значения для полей login и password'):
            new_courier_data_lifecycle['login'] = ""
            new_courier_data_lifecycle['password'] = ""
        with allure.step('Отправка запроса с обоими пустыми полями'):
            response = courier_api.create_courier(new_courier_data_lifecycle)
        with allure.step('Проверка ошибки валидации'):
            assert response.status_code == 400, \
                f"Ожидался статус 400, получен {response.status_code}. Тело: {response.text}"
            expected_error = "Недостаточно данных для создания учетной записи"
            assert expected_error in response.text, \
                f"Ожидалось сообщение '{expected_error}', получено: {response.text}"

    @allure.title('Негативный сценарий: создание дубликата курьера')
    @allure.description('Проверка создания курьера с уже существующим логином')
    @pytest.mark.negative
    def test_create_duplicate_courier_fail(self, courier_api, new_courier_data_lifecycle):
        with allure.step('Создание первого курьера для последующего дублирования'):
            first_response = courier_api.create_courier(new_courier_data_lifecycle)
            assert first_response.status_code == 201, \
                f"Не удалось создать первого курьера для теста дубликата. Код: {first_response.status_code}"
        with allure.step('Отправка запроса с тем же логином'):
            second_response = courier_api.create_courier(new_courier_data_lifecycle)
        with allure.step('Проверка ошибки дубликата'):
            assert second_response.status_code == 409, \
                f"Ожидался статус 409 (Conflict), получен {second_response.status_code}. Тело: {second_response.text}"
            expected_error = "Этот логин уже используется"
            assert expected_error in second_response.text, \
                f"Ожидалось сообщение '{expected_error}', получено: {second_response.text}"

@allure.epic('Учебный сервис Яндекс Самокат')
@allure.feature('Курьеры')
@allure.story('Логин Курьера - Ручка /api/v1/courier/login')
class TestLoginCourier:
    @allure.title('Позитивный сценарий: авторизация курьера')
    @allure.description('Проверка входа с валидными учетными данными')
    @pytest.mark.positive
    def test_login_courier_success(self, courier_api, create_new_courier_lifecycle):
        payload = {
            "login": create_new_courier_lifecycle['login'],
            "password": create_new_courier_lifecycle['password']
        }
        with allure.step('Отправка запроса на логин с полученными данными'):
            response = courier_api.login(payload)
        with allure.step('Проверка успешного входа'):
            assert response.status_code == 200, \
                f"Ожидался статус 200, получен {response.status_code}. Тело: {response.text}"
            assert "id" in response.json(), \
                f"В ответе должен быть 'id' пользователя, получено: {response.json()}"
            assert isinstance(response.json()["id"], int)

    @allure.title('Негативный сценарий: авторизация при отсутствии обязательного поля')
    @allure.description('Проверка входа, когда при отсутствии обязательных полей (login, password)')
    @pytest.mark.negative
    @pytest.mark.parametrize('payload', [
        pytest.param({"password": "password123"}, id="Проверка входа без поля логина"),
        pytest.param(
            {"login": "my_login"},
            id="Проверка входа без поля пароля",
            marks=pytest.mark.xfail(reason="Баг стенда: сервер возвращает 504 при отсутствии ключа password вместо 400")
        ),
        pytest.param(
            {},
            id="Пустой запрос без полей",
            marks=pytest.mark.xfail(reason="Баг стенда: сервер возвращает 504 при пустом теле запроса вместо 400")
        )
    ])
    def test_login_courier_missing_fields_fail(self, courier_api, payload):
        with allure.step('Отправка запроса с неполным payload'):
            response = courier_api.login(payload)
        with allure.step('Проверка ошибки валидации'):
            assert response.status_code == 400, \
                f"Ожидался статус 400, получен {response.status_code}. Тело: {response.text}"
            expected_error = "Недостаточно данных для входа"
            assert expected_error in response.text, \
                f"Ожидалось сообщение '{expected_error}', получено: {response.text}"

    @allure.title('Негативный сценарий: авторизация при пустых обязательных полях')
    @allure.description('Проверка входа, при пустых обязательных полях (login, password)')
    @pytest.mark.negative
    @pytest.mark.parametrize('payload', [
        {"login": "", "password": "password123"},
        {"login": "my_login", "password": ""},
        {"login": "", "password": ""}
    ], ids=[
        "Проверка входа с пустым полем логина",
        "Проверка входа с пустым полем пароля",
        "Пустые поля логина и пароля"
    ])
    def test_login_courier_empty_fields_fail(self, courier_api, payload):
        with allure.step('Отправка запроса с неполным payload'):
            response = courier_api.login(payload)
        with allure.step('Проверка ошибки валидации'):
            assert response.status_code == 400, \
                f"Ожидался статус 400, получен {response.status_code}. Тело: {response.text}"
            expected_error = "Недостаточно данных для входа"
            assert expected_error in response.text, \
                f"Ожидалось сообщение '{expected_error}', получено: {response.text}"

    @allure.title('Негативный сценарий: авторизация при неверном логине')
    @allure.description('Передан несуществующий login при валидном пароле')
    @pytest.mark.negative
    def test_login_courier_wrong_login_fail(self, courier_api, create_new_courier_lifecycle):
        payload = {
            "login": "non_existent_user_9999",
            "password": create_new_courier_lifecycle['password']
        }
        with allure.step('Отправка запроса с несуществующим логином'):
            response = courier_api.login(payload)
        with allure.step('Проверка ошибки (404 Not Found)'):
            assert response.status_code == 404, \
                f"Ожидался статус 404, получен {response.status_code}. Тело: {response.text}"
            expected_error = "Учетная запись не найдена"
            assert expected_error in response.text, \
                f"Ожидалось сообщение '{expected_error}', получено: {response.text}"

    @allure.title('Негативный сценарий: авторизация при неверном пароле')
    @allure.description('Передан существующий login, но неправильный password')
    @pytest.mark.negative
    def test_login_courier_wrong_password_fail(self, courier_api, create_new_courier_lifecycle):
        payload = {
            "login": create_new_courier_lifecycle['login'],
            "password": "wrong_password_6666"
        }
        with allure.step('Отправка запроса с неверным паролем'):
            response = courier_api.login(payload)
        with allure.step('Проверка ошибки (404 Not Found)'):
            assert response.status_code == 404, \
                f"Ожидался статус 404, получен {response.status_code}. Тело: {response.text}"
            expected_error = "Учетная запись не найдена"
            assert expected_error in response.text, \
                f"Ожидалось сообщение '{expected_error}', получено: {response.text}"

    @allure.title('Негативный сценарий: авторизация под несуществующим пользователем')
    @allure.description('Оба поля входа заполнены несуществующими данными')
    @pytest.mark.negative
    def test_login_courier_non_existent_user_fail(self, courier_api, new_courier_data_lifecycle):
        with allure.step('Отправка запроса с полностью случайными данными'):
            response = courier_api.login(new_courier_data_lifecycle)
        with allure.step('Проверка ошибки (404 Not Found)'):
            assert response.status_code == 404, \
                f"Ожидался статус 404, получен {response.status_code}. Тело: {response.text}"
            expected_error = "Учетная запись не найдена"
            assert expected_error in response.text, \
                f"Ожидалось сообщение '{expected_error}', получено: {response.text}"
            