import pytest
import allure
from conftest import fake
from utils.special_request import OrderRequests, generate_random_string

randoms_string = generate_random_string(10)
email = fake.email()


@allure.feature('Создание и выгрузка заказов')
class TestOrder:
    @allure.title('Можно создать заказ без авторизации')
    def test_create_order_successful(self, create_order_payload):
        payload = create_order_payload
        response = OrderRequests().post_create_order_no_auth(data=payload)
        assert response["success"]

    @allure.title('Можно создать заказ с токеном пользователя и ингредиентами')
    def test_create_order_for_authorized_user_zzz(self, courier_with_payload, create_order_payload):
        response = OrderRequests().post_create_order_auth(data=create_order_payload,
                                                          token=courier_with_payload.access_token)
        assert response["success"]

    @allure.title('Заказ не может не содержать ингредиентов')
    def test_create_order_without_ingredients(self):
        payload = {}
        response = OrderRequests().post_create_order_no_auth(data=payload)
        print(response)
        assert response["message"] == 'Ingredient ids must be provided'

    @allure.title('Нельзя создать заказ с неверным id ингредиента')
    def test_create_order_wrong_ingredients_id(self, create_order_payload):
        payload = create_order_payload
        payload["ingredients"][0] = randoms_string
        response = OrderRequests().post_create_order_no_auth(data=payload)
        assert 'Internal Server Error' in response

    @allure.title('Нельзя создать заказ авторизованным пользователем без ингредиентов')
    def test_create_order_without_payload_with_auth(self, courier_with_payload):
        payload = {}
        response = OrderRequests().post_create_order_auth(data=payload,
                                                          token=courier_with_payload.access_token)
        assert response['message'] == 'Ingredient ids must be provided'
