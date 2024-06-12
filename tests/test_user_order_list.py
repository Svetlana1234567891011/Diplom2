import allure
from conftest import fake
from utils.special_request import OrderRequests, generate_random_string, UserRequests

randoms_string = generate_random_string(10)
email = fake.email()


@allure.feature('Проверка создания заказов')
class TestGetOrderForUser:

    @allure.title('получить список заказов авторизованного пользователя')
    def test_get_user_auth_order_list(self, courier_with_payload, create_order_payload):
        orders = OrderRequests().post_create_order_auth(data=create_order_payload,
                                                        token=courier_with_payload.access_token)
        response_for_order = OrderRequests().get_user_orders(token=courier_with_payload.access_token)
        assert (orders['order']['_id']) == (response_for_order['text']['orders'][0]['_id'])

    @allure.title('Получить список заказов без токена')
    def test_get_user_orders_for_invalid_token(self, courier_with_payload, create_order_payload):
        orders = OrderRequests().post_create_order_auth(data=create_order_payload,
                                                        token=courier_with_payload.access_token)
        response_for_order = OrderRequests().get_user_orders(token=None)
        assert response_for_order['text']['message'] == "You should be authorised"

    @allure.title('получить список заказов разлогиненного пользователя')
    def test_get_user_orders_for_no_auth_token(self, create_payload, create_order_payload):
        response_new = UserRequests().post_create_user(data=create_payload)
        refresh = response_new['refreshToken']
        accesses = response_new['accessToken']
        orders = OrderRequests().post_create_order_auth(data=create_order_payload, token=accesses)
        response_out = UserRequests().post_logout(token=refresh)
        response_for_order = OrderRequests().get_user_orders(token=refresh)
        assert (response_for_order['text']['message'] == "You should be authorised"
                and response_out['message'] == 'Successful logout')
