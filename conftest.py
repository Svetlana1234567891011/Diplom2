import pytest
import allure
from faker import Faker
from utils.special_request import UserRequests, OrderRequests
import random
import string

fake = Faker()


@pytest.fixture()
@allure.step('Создаем случайное число')
def generate_random_string_fix():
    def _generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string  # Возвращаем сгенерированную строку

    return _generate_random_string


@pytest.fixture()
@allure.step('Создаем случайное число')
def generate_random_string_10(generate_random_string_fix):
    randoms_string = generate_random_string_fix(10)
    return randoms_string


@allure.step('payload для пользователя')
@pytest.fixture(scope='function', autouse=True)
def create_payload(generate_random_string_10):
    name = generate_random_string_10
    password = generate_random_string_10
    email = fake.email()  # генерируем мейл методом генерации имейлов в fake

    payload = {
        "name": name,
        "password": password,
        "email": email
    }

    return payload


@pytest.fixture(scope='function')
@allure.step('payload заказа')
def create_order_payload():
    ingredients_list = OrderRequests().get_ingredients_list()
    ids = [element['_id'] for element in ingredients_list['text']['data']]
    ids_for_payload = random.sample(ids, 3)
    payload = {"ingredients": ids_for_payload}
    return payload


@pytest.fixture(scope='function')
def courier_with_payload(create_payload):
    courier_requests = UserRequests()
    # Создаем Пользователя
    payload = create_payload
    courier_requests.payload = payload  # Добавляем payload в объект
    response_new = courier_requests.post_create_user(data=payload)
    access_token = response_new.get('accessToken')

    if access_token:
        courier_requests.access_token = access_token

    return courier_requests


@pytest.fixture(scope='function', autouse=True)
def cleanup_user():
    response = {}

    yield response
    if 'token' in response:
        UserRequests().delete_user(token=response['token'])
