import pytest
import allure
from utils.special_request import UserRequests, generate_random_string

randoms_string = generate_random_string(10)


@allure.feature('Создание Пользователя')
class TestCreateCourier:

    @allure.title('Можно создать Пользователя со случайным логином')
    @pytest.mark.parametrize('login_v, password_v, firstname_v',
                             [
                                 (randoms_string, randoms_string, randoms_string),
                             ])
    def test_all_the_fields_are_required(self, login_v, password_v, firstname_v):
        payload = {
            "login": login_v,
            "password": password_v,
            "firstName": firstname_v
        }

        response = UserRequests().post_create_user(data=payload)
        assert response['ok']

    @allure.title('Нельзя создать двух Пользователей с одинаковыми логинами')
    def test_cant_create_courier_dupes(self, courier_with_payload):
        response_dupe = courier_with_payload.post_create_user(
            data=courier_with_payload.payload)  # отправляем данные повторно
        assert response_dupe["message"] == "User already exists"

    @pytest.mark.parametrize('login_v, password_v, firstname_v',
                             [
                                 (None, randoms_string, randoms_string),
                                 (None, randoms_string, None),
                                 (randoms_string, None, None),
                                 (None, None, randoms_string),

                             ])
    @allure.title('Для создания Пользователя необходимо задать все обязательные поля (логин, пароль)')
    def test_all_the_fields_are_required(self, login_v, password_v, firstname_v):
        payload = {
            "login": login_v,
            "password": password_v,
            "firstName": firstname_v
        }

        response = UserRequests().post_create_user(data=payload)
        assert response["message"] == "Email, password and name are required fields"
