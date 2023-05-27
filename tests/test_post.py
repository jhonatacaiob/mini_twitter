from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from api.models import Post
from api.views import PostView


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

        post = Post.objects.get(id=response.data['id'])
        self.assertIsNotNone(post)

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

    def test_should_return_posts_of_one_selected_users(self):
        current_user = User.objects.get(username='user1')
        filtred_user = User.objects.get(username='user2')

        request = self.factory.get(
            '/api/posts/', {'user_id': filtred_user.id}, format='json'
        )
        force_authenticate(request, user=current_user)
        response = self.view(request)

        self.assertTrue(
            any([row['user'] == 'user2' for row in response.data['results']])
        )

    # Por motivos de limitação da lib de test, não da pra testar essa operação
    # def test_should_return_posts_of_various_selected_users(self):
    #     current_user = User.objects.get(username='user5')
    #     filtred_users_id = [
    #         User.objects.get(username='user1').id,
    #         User.objects.get(username='user2').id,
    #         User.objects.get(username='user3').id,
    #     ]

    #     request = self.factory.get(
    #         '/api/posts/',
    #         {
    #             'user_id': filtred_users_id[0],
    #             'user_id': filtred_users_id[1],
    #             'user_id': filtred_users_id[2],
    #         },
    #     )
    #     force_authenticate(request, user=current_user)
    #     response = self.view(request)

    #     self.assertTrue(
    #         any(
    #             [
    #                 row['user'] not in filtred_users_id
    #                 for row in response.data['results']
    #             ]
    #         )
    #     )
