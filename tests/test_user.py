from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from api.views import CreateUserView


class CreateUserTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = CreateUserView.as_view()

    def test_creating_user(self):
        user_dict = {
            'username': 'user1',
            'password': '123',
        }
        request = self.factory.post(
            '/api/create_user/', user_dict, format='json'
        )
        response = self.view(request)

        self.assertEqual(response.status_code, 201)
        self.assertDictContainsSubset({'username': 'user1'}, response.data)

        user = User.objects.get(id=response.data['id'])

        self.assertIsNotNone(user)

    def test_do_not_create_if_an_argument_is_missing(self):
        values = [
            {'username': 'jhow'},
            {'password': '123'},
        ]

        for value in values:
            with self.subTest(value=value):
                request = self.factory.post(
                    '/api/create_user/', value, format='json'
                )
                response = self.view(request)
                self.assertEqual(response.status_code, 400)

    def test_do_not_create_if_user_already_exists(self):
        user = User(username='user1', password=make_password('password'))
        user.save()

        request = self.factory.post(
            '/api/create_user/',
            {
                'username': user.username,
                'password': user.password,
            },
            format='json',
        )
        response = self.view(request)
        self.assertEqual(response.status_code, 400)

    def test_hashing_password(self):
        password = 'password'
        user = User(username='user1', password=make_password(password))
        user.save()

        self.assertNotEqual(password, user.password)
