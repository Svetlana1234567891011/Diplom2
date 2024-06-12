import pytest
from conftest import create_payload, fake
from utils.special_request import UserRequests, generate_random_string
import allure

randoms_string = generate_random_string(10)

email = fake.email()


@allure.feature('Проверка авторизации пользователя, успешный запрос возвращает id')
class TestLogin:
    @allure.title('Пользователь может авторизоваться с существующей учетной записью')
    def test_user_can_login(self, create_payload):
        courier_requests = UserRequests()  # Создаем экземпляр класса CourierRequests
        payload = create_payload
        response_new = courier_requests.post_create_user(data=create_payload)  # Создаем Пользователя

        response_login = courier_requests.post_login_user(data=payload,
                                                          token=response_new['accessToken'])  # Аутентификация
        assert response_login["success"] == True

    @pytest.mark.parametrize("change_value",
                             ["password"
                              ]
                             )
    @allure.title('Пользователь с отсутствующим паролем не может залогиниться')
    def test_user_cannot_login(self, courier_with_payload, change_value):
        courier_with_payload.payload[change_value] = randoms_string  # Меняем пароль
        response = courier_with_payload.post_login_user(data=courier_with_payload.payload,
                                                        token=courier_with_payload.access_token)

        assert response['message'] == 'email or password are incorrect'
        print(f"Response message: {response['message']}")
        print(f"Full response: {response}")

    @allure.title('Пользователь с отсутствующим логином не может залогиниться')
    def test_user_cannot_name(self, courier_with_payload):
        courier_with_payload.payload['email'] = email  # Меняем мейл
        response = courier_with_payload.post_login_user(data=courier_with_payload.payload,
                                                        token=courier_with_payload.access_token)

        assert response['message'] == 'email or password are incorrect'
