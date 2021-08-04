import pytest
import requests
import random
import string

from lib.base_case import BaseCase
from lib.assertions import Assertions

from datetime import datetime

class TestUserRegister(BaseCase):
    ex_params = [{'password'}, {'username'}, {'firstName'}, {'lastName'}, {'email'} ]

    def setup(self):
        basepart = 'learnqa'
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{basepart}{random_part}@{domain}"

    def test_create_user_succesfully(self):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': self.email
        }

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@example.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"User with email '{email}' already exists", f"Unexpected response content {response.content}"

    def test_user_register_with_incorrect_email(self):
        email = 'vinkotovexample.com'
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", f"Unexpected response content {response.content}"

    def test_user_register_with_short_name(self):
        email = 'test@example.com'
        data = {
            'password': '123',
            'username': 'a',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': email
        }

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too short", f"Unexpected response content {response.content}"

    def test_user_register_with_long_nameO(self):
        name = '4kjDFbC0wAHydZjhU4prwqnMf8mkMtNyqOe7NVReUbliCKPlcSDGVaPTaiifjZ1ZmD3xMLvMi18zkLAqXx7ddadddadadN6gU6tIXpD8BWssrXjos4PAkh00lEqkZ3yXGEYaWAA9Ei96aJPddyD9tiyQRnelQl8GDBeBu8rf3hRvoJHqxP4Io8sEKmzECQcZhGKWaIxcp5gpjmX6sJm8DlmeAeZqI1q8I9ufPdvnaYDkwEQWhBuj5jywhnzL4uhTIGH6'
        data = {
            'password': '123',
            'username': name,
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'test@example.com'
        }

        response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too long", f"Unexpected response content {response.content}"

    @pytest.mark.parametrize('conditions', ex_params)
    def test_user_without_required_field(self, conditions):
        data = {
            'password': '123',
            'username': 'learnqa',
            'firstName': 'learnqa',
            'lastName': 'learnqa',
            'email': 'test@example.com'
        }

        for condition in conditions:
           del data[condition]

           response = requests.post('https://playground.learnqa.ru/api/user/', data=data)

           print(response.content)
           Assertions.assert_code_status(response, 400)
           assert response.content.decode("utf-8") == f"The following required params are missed: {condition}", f"Unexpected response content {response.content}"


