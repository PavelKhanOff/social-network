from django.urls import reverse
from rest_framework.test import APITestCase

from .models import CustomUser


class TestSetUp(APITestCase):

    def setUp(self):
        self.get_token_url = reverse('get_token')
        self.user_data = {
            'username': 'lukadoncic',
            'password': 'mavericks123',
            'email': 'slovenianboy@dallas.com'
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class TestApiViews(TestSetUp):

    def test_posts_create(self):
        res = self.client.post('/api/users/', self.user_data, format='json')
        email = res.data['email']
        user = CustomUser.objects.get(email=email)
        user.is_superuser = True
        user.save()
        get_token = self.client.post(
            self.get_token_url, self.user_data, format='json')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + get_token.data['access'])
        post_create_res = self.client.post(
            '/api/posts/', {
                'title': 'title',
                'text': 'text'
            }, format='json')
        self.assertEqual(post_create_res.status_code, 201)
        self.assertEqual(post_create_res.data['title'], 'title')
        self.assertEqual(post_create_res.data['text'], 'text')

    def test_post_get(self):
        user_list_res = self.client.get('/api/posts/')
        self.assertEqual(user_list_res.status_code, 200)

    def test_post_delete(self):
        res = self.client.post('/api/users/', self.user_data, format='json')
        email = res.data['email']
        user = CustomUser.objects.get(email=email)
        user.is_superuser = True
        user.save()
        get_token = self.client.post(
            self.get_token_url, self.user_data, format='json')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + get_token.data['access'])
        post_create_res = self.client.post(
            '/api/posts/', {
                'title': 'title',
                'text': 'text'
            }, format='json')
        post_id = post_create_res.data['id']
        delete_post = self.client.delete(f'/api/posts/{post_id}/')
        self.assertEqual(delete_post.status_code, 204)
        self.assertEqual(delete_post.data, None)

    def test_post_update(self):
        res = self.client.post('/api/users/', self.user_data, format='json')
        email = res.data['email']
        user = CustomUser.objects.get(email=email)
        user.is_superuser = True
        user.save()
        get_token = self.client.post(
            self.get_token_url, self.user_data, format='json')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + get_token.data['access'])
        post_create_res = self.client.post(
            '/api/posts/', {
                'title': 'title',
                'text': 'text'
            }, format='json')
        post_id = post_create_res.data['id']
        update_post = self.client.put(f'/api/posts/{post_id}/', {
                'title': 'changed_title',
                'text': 'changed_text'
            }, format='json')
        self.assertEqual(update_post.status_code, 200)
        self.assertNotEqual(
            update_post.data['title'], post_create_res.data['title'])
        self.assertNotEqual(
            update_post.data['text'], post_create_res.data['text'])

    def test_like_create_delete(self):
        res = self.client.post('/api/users/', self.user_data, format='json')
        email = res.data['email']
        user = CustomUser.objects.get(email=email)
        user.is_superuser = True
        user.save()
        get_token = self.client.post(
            self.get_token_url, self.user_data, format='json')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + get_token.data['access'])
        post_create_res = self.client.post(
            '/api/posts/', {
                'title': 'title',
                'text': 'text'
            }, format='json')
        post_id = post_create_res.data['id']
        like_create_res = self.client.get(f'/api/posts/{post_id}/like/')
        self.assertEqual(like_create_res.status_code, 201)
        self.assertEqual(like_create_res.data, 'Лайк успешно поставлен')
        like_delete_res = self.client.delete(f'/api/posts/{post_id}/like/')
        self.assertEqual(like_delete_res.status_code, 204)
        self.assertEqual(like_delete_res.data, 'Удалено')

    def test_like_analytics(self):
        res = self.client.post('/api/users/', self.user_data, format='json')
        email = res.data['email']
        user = CustomUser.objects.get(email=email)
        user.is_admin = True
        user.save()
        get_token = self.client.post(
            self.get_token_url, self.user_data, format='json')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + get_token.data['access'])
        for post in range(5):
            post_create_res = self.client.post(
                '/api/posts/', {
                    'title': f'{post}title',
                    'text': 'text'
                }, format='json')
            post_id = post_create_res.data['id']
            self.client.get(f'/api/posts/{post_id}/like/')
        analytics_res = self.client.get('/api/like/analytics/')
        self.assertEqual(analytics_res.status_code, 200)
        self.assertEqual(len(analytics_res.data['results']), 5)
