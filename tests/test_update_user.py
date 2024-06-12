import pytest
import allure
from utils.special_request import UserRequests, generate_random_string
from conftest import fake

from conftest import fake
from utils.special_request import UserRequests, generate_random_string
from faker import Faker

randoms_string = generate_random_string(10)
email = fake.email()


@allure.feature('Проверка обновления данных юзера')
class TestUserDataUpdate:
    # @pytest.mark.parametrize("key_to_be_changed",
    #                          ["email",
    #                           "password",
    #                           "name"]
    #                          )
    # @allure.title('Изменение данных пользователя без авторизации')
    # def test_can_patch_unauthorized_user(self, create_user_payload, make_user, key_to_be_changed, make_random_value):
    #     payload = create_user_payload(email='rand', password='1234', name='rand')
    #     user = make_user(data=payload)
    #     payload[key_to_be_changed] = make_random_value
    #     patched_user = UserRequests().patch_user(data=payload, token=user["text"]['accessToken'])
    #     updated_user = UserRequests().get_user_data(token=user["text"]['accessToken'])
    #     assert (patched_user["text"]["user"]["name"] == updated_user["text"]["user"]["name"] and
    #             patched_user["text"]["user"]["email"] == updated_user["text"]["user"]["email"])
    #
    #     @pytest.mark.parametrize("change_value",
    #                              ["login",
    #                               "password"]
    #                              )
    #     @allure.title('Система вернёт ошибку, если неправильно указать логин или пароль')
    #     def test_courier_cannot_login_due_wrong_input(self, change_value, create_payload):
    #         CourierRequests().post_create_courier(data=create_payload)
    #         create_payload[change_value] = randoms_string
    #         response = CourierRequests().post_login_courier(data=create_payload)
    #         assert response['message'] == 'Учетная запись не найдена'
    #
    # @pytest.mark.parametrize("change_value",
    #                          ["login",
    #                           "password"]
    #                          )
    # @allure.title('Пользователь с отсутствующим логином не может залогиниться')
    # def test_courier_cannot_name(self, change_value, create_payload):
    #     CourierRequests().post_create_courier(data=create_payload)
    #     courier_with_payload.payload[change_value] = None
    # CourierRequests().post_create_courier(data=create_payload)
    # create_payload[change_value] = randoms_string
    # response = CourierRequests().post_login_courier(data=create_payload)
    # @pytest.mark.parametrize("change_value",
    #                          ["name",
    #                           "password"]
    #                         )
    # def test_all_the_fields(self, change_value, create_payload):
    @allure.title('Изменение данных пользователя с авторизацией')
    def test_update_auth(self, create_payload):
        new_user = UserRequests().post_create_user(data=create_payload)
        payload = {

            "name": randoms_string,
            "password": randoms_string,
            "email": email
        }
        access_token = new_user.get('accessToken')
        patched_user = UserRequests().patch_user(data=payload, token=access_token)
        rewrite_user = UserRequests().get_user_data(token=access_token)
        assert (patched_user['text']['user']['email'] == rewrite_user['text']['user']['email'] and
                patched_user['text']['user']['name'] == rewrite_user['text']['user']['name'])

    @allure.title('Данные пользователя - невозможно получить или изменить без авторизации')
    def test_update_no_auth(self, create_payload):
        new_user = UserRequests().post_create_user(data=create_payload)
        payload_new = {

            "name": randoms_string,
            "password": randoms_string,
            "email": fake.email()
        }

        refreshment = new_user['refreshToken']
        logout_user = UserRequests().post_logout(token=refreshment)  # выход из системы
        rewrite_user = UserRequests().get_user_data(token=refreshment)
        patched_user = UserRequests().patch_user(data=payload_new, token=refreshment)
        assert (patched_user['text']['message'] == "You should be authorised" and
                logout_user['message'] == "Successful logout" and
                rewrite_user['text']['message'] == "You should be authorised")
