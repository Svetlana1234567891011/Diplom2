import json
import random
import string

import requests
import allure


def generate_random_string(length):
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))
    return random_string


class MainRequests:
    host = 'https://stellarburgers.nomoreparties.site'



    def post_request_transform_token(self, url, data, token):
        headers = {'authorization': token}
        response = requests.post(url=url, data=data, headers=headers)
        return response.json()


    def post_request_transform(self, url, data):
        response = requests.post(url=url, json=data)
        if response.headers.get('Content-Type') and 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return {"status_code": response.status_code, "text": response.text}

    def delete_request_transform(self, url, token):
        headers = {"Content-Type": "application/json", 'authorization': token}
        response = requests.delete(url=url, headers=headers)

        return {"status_code": response.status_code, "text": response.json()}

    def get_request_transform(self, url):
        response = requests.get(url=url, data={})

        return {"status_code": response.status_code, "text": response.json()}

    def get_request_transform_token(self, url, token):
        headers = {'authorization': token}
        response = requests.get(url=url, data={}, headers=headers)
        return {"status_code": response.status_code, "text": response.json()}

    def put_request_transform_and_check(self, url, data):
        response = requests.put(url=url, data=data)
        if 'application/json' in response.headers['Content-Type']:
            return response.json()
        else:
            return response.text

    def patch_request_transform(self, url, data, token):
        headers = {'authorization': token}
        response = requests.patch(url=url, data=data, headers=headers)
        return {"status_code": response.status_code, "text": response.json()}

    def post_request_transform_and_check_ord_auth(self, url, data, token):  # проверяем код ответа
        headers = {'authorization': token}
        response = requests.post(url=url, data=data, headers=headers)  # кладем код ответа в переменную response
        if 'application/json' in response.headers['Content-Type']:
            return response.json()

        else:

            return response.text

    def post_request_transform_and_check_ord(self, url, data):  # проверяем код ответа
        response = requests.post(url=url, data=data)  # кладем код ответа в переменную response
        if 'application/json' in response.headers['Content-Type']:  # Функция exec_post_request_and_check проверяет
            return response.json()  # если тип содержимого ответа - JSON, возвращает его в формате словаря, иначе возвращает текст ответа.
        else:
            return response.text

    def post_request_transform_token_refresh(self, url, data):
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url=url, json=data)
        return response.json()


class UserRequests(MainRequests):
    def __init__(self):
        self.access_token = None
        self.refresh_token = None

    courier_create = '/api/v1/courier'
    user_handler = '/api/auth/register'
    manipulate_user_handler = '/api/auth/user'
    user_login_handler = '/api/auth/login'
    logout = '/api/auth/logout'

    @allure.step('Создаем Пользовательа, отправив запрос POST')
    def post_create_user(self, data=None):
        url = f"{self.host}{self.user_handler}"
        return self.post_request_transform(url, data=data)

    @allure.step('Логиним Пользовательа, отправив запрос POST')
    def post_login_user(self, token, data=None):
        url = f"{self.host}{self.user_login_handler}"
        return self.post_request_transform_token(url, data=data, token=token)

    @allure.step('Удаляем Пользовательа, отправив запрос DELETE.')
    def delete_user(self, token):
        url = f"{self.host}{self.manipulate_user_handler}"
        return self.delete_request_transform(url, token=token)

    @allure.step('Обновляем данные пользователя, отправив запрос PATCH')
    def patch_user(self, data, token):
        url = f"{self.host}{self.manipulate_user_handler}"
        return self.patch_request_transform(url, data=data, token=token)

    @allure.step('Получаем данные пользователя, отправив запрос GET')
    def get_user_data(self, token):
        url = f"{self.host}{self.manipulate_user_handler}"
        return self.get_request_transform_token(url, token=token)

    def post_logout(self, token):
        url = f"{self.host}{self.logout}"
        data = {"token": token}
        return self.post_request_transform_token_refresh(url, data=data)


class OrderRequests(MainRequests):

    ingredients_handler = '/api/ingredients'
    order_handler = '/api/orders'

    @allure.step('Создаем заказ без токена, отправив запрос POST')
    def post_create_order_no_auth(self, data):
        url = f"{self.host}{self.order_handler}"
        return self.post_request_transform_and_check_ord(url, data=data)

    @allure.step('Создаем заказ, отправив запрос POST')
    def post_create_order_auth(self, data, token):
        url = f"{self.host}{self.order_handler}"
        return self.post_request_transform_and_check_ord_auth(url, data=data, token=token)

    @allure.step('Получаем список ингредиентов, отправив запрос GET')
    def get_ingredients_list(self):
        url = f"{self.host}{self.ingredients_handler}"
        return self.get_request_transform(url)

    @allure.step('Получаем заказы пользователя, отправив запрос GET.')
    def get_user_orders(self, token):
        url = f"{self.host}{self.order_handler}"
        return self.get_request_transform_token(url, token=token)
