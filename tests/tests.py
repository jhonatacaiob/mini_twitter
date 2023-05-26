from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from api.models import Post
from api.views import CreateUserView, PostView


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
    
        user = User.objects.get(username='user1')

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


class PostsTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PostView.as_view()
        users = [
            User(username='user1', password=make_password('pass1')),
            User(username='user2', password=make_password('pass2')),
            User(username='user3', password=make_password('pass3')),
            User(username='user4', password=make_password('pass4')),
            User(username='user5', password=make_password('pass5')),
            User(username='user6', password=make_password('pass6')),
        ]
        User.objects.bulk_create(users)

        posts = [
            Post(user=users[0], content='Post-1-1'),
            Post(user=users[1], content='Post-1-2'),
            Post(user=users[2], content='Post-1-3'),
            Post(user=users[3], content='Post-1-4'),
            Post(user=users[4], content='Post-1-5'),
            Post(user=users[5], content='Post-1-6'),
            Post(user=users[0], content='Post-2-1'),
            Post(user=users[1], content='Post-2-2'),
            Post(user=users[2], content='Post-2-3'),
            Post(user=users[3], content='Post-2-4'),
            Post(user=users[4], content='Post-2-5'),
            Post(user=users[5], content='Post-2-6'),
            Post(user=users[0], content='Post1-3-1'),
            Post(user=users[1], content='Post2-3-2'),
            Post(user=users[2], content='Post3-3-3'),
            Post(user=users[3], content='Post4-3-4'),
            Post(user=users[4], content='Post5-3-5'),
            Post(user=users[5], content='Post6-3-6'),
        ]
        Post.objects.bulk_create(posts)

    def test_user_should_post(self):
        user = User.objects.get(username='user1')

        expected_response = {
            'content': 'some post content',
            'user': 'user1',
        }

        request = self.factory.post(
            '/api/posts/', {'content': 'some post content'}
        )
        force_authenticate(request, user=user)
        response = self.view(request)

        self.assertDictContainsSubset(expected_response, response.data)

    def test_should_return_list_of_posts_paginated(self):
        user = User.objects.get(username='user1')

        request = self.factory.get('/api/posts/')
        force_authenticate(request, user=user)
        response = self.view(request)

        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.data['results'], list)
        self.assertEqual(10, len(response.data['results']))

    def test_shouldnt_return_posts_of_current_user(self):
        user = User.objects.get(username='user1')

        request = self.factory.get('/api/posts/')
        force_authenticate(request, user=user)
        response = self.view(request)

        self.assertTrue(
            any([row['user'] != 'user1' for row in response.data['results']])
        )

    def test_should_return_posts_of_selected_users(self):
        user = User.objects.get(username='user1')

        request = self.factory.get('/api/posts/', {'user_id': '2'})
        force_authenticate(request, user=user)
        response = self.view(request)
        # self.assertTrue(
        #     any([row['user'] != 'user1' for row in response.data['results']])
        # )
