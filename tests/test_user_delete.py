import requests

from lib.base_case import BaseCase
from lib.assertions import Assertions

class TestUserDelete(BaseCase):

    def test_delete_super_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)

        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")
        auth_sid = self.get_cookie(response1, "auth_sid")

        response2 = requests.delete(f"https://playground.learnqa.ru/api/user/{user_id_from_auth_method['user_id']}")

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == "Auth token not supplied", f"Unexpected response content"

    def test_user_delete_on_registered_user(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = requests.post('https://playground.learnqa.ru/api/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # Login
        login_data = {
            'email': email,
            'password': password
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        token = self.get_header(response2, "x-csrf-token")
        auth_sid = self.get_cookie(response2, "auth_sid")

        # EDIT
        new_name = "Changed name"

        response3 = requests.delete(f"https://playground.learnqa.ru/api/user/{user_id['id']}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response3, 200)

        # GET

        response4 = requests.get(f"https://playground.learnqa.ru/api/user/{user_id['id']}",
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid}
                                 )

        Assertions.assert_code_status(response4, 404)

    def test_delete_user_under_other_user(self):
        # Register
        register_data = self.prepare_registration_data()
        response1 = requests.post('https://playground.learnqa.ru/api/user/', data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, 'id')

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # Login
        login_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response2 = requests.post("https://playground.learnqa.ru/api/user/login", data=login_data)

        token = self.get_header(response2, "x-csrf-token")
        auth_sid = self.get_cookie(response2, "auth_sid")

        # EDIT
        new_name = "Changed name"

        response3 = requests.delete(f"https://playground.learnqa.ru/api/user/{user_id['id']}",
                                    headers={"x-csrf-token": token},
                                    cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response3, 400)