class Url:
    URL = 'https://qa-scooter.praktikum-services.ru'

class Endpoint:
    # Курьеры
    CREATE_COURIER = '/api/v1/courier' #POST
    LOGIN_COURIER = '/api/v1/courier/login' #POST
    DELETE_COURIER = "/api/v1/courier/{}" #DELETE

    # Заказы
    CREATE_ORDER = '/api/v1/orders' #POST
    GET_ORDERS = '/api/v1/orders' #GET
