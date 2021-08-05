from django.urls import reverse
from rest_framework.test import APITestCase

from .models import CustomUser


class TestSetUp(APITestCase):

    def setUp(self):
        self.get_token_url = reverse('get_token')
        self.refresh_token_url = reverse('refresh_token')
        self.user_activity_url = reverse('activity')
        self.user_data = {
            'username': 'lukadoncic',
            'password': 'mavericks123',
            'email': 'slovenianboy@dallas.com'
        }
        return super().setUp()

    def tearDown(self):
        return super().tearDown()


class TestUserViews(TestSetUp):

    def test_user_can_get_token(self):
        self.client.post('/api/users/', self.user_data, format='json')
        res = self.client.post(
            self.get_token_url, self.user_data, format='json')
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.data['access'], msg='Check access key')
        self.assertTrue(res.data['refresh'], msg='Check refresh key')

    def test_user_can_refresh_token(self):
        self.client.post('/api/users/', self.user_data, format='json')
        res = self.client.post(
            self.get_token_url, self.user_data, format='json')
        first_token = res.data['access']
        refresh_token = res.data['refresh']
        refresh_res = self.client.post(
            self.refresh_token_url, {'refresh': refresh_token}, format='json')
        second_token = refresh_res.data['access']
        check_second_token = self.client.get('/users/me')
        self.assertTrue(check_second_token.status_code, 200)
        self.assertEqual(refresh_res.status_code, 200)
        self.assertNotEqual(first_token, second_token)

    def test_user_activity(self):
        res = self.client.post('/api/users/', self.user_data, format='json')
        email = res.data['email']
        user = CustomUser.objects.get(email=email)
        user.is_superuser = True
        user.save()
        get_token = self.client.post(
            self.get_token_url, self.user_data, format='json')
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + get_token.data['access'])
        activity_res = self.client.get(self.user_activity_url)
        self.assertEqual(activity_res.status_code, 200)
        self.assertTrue(activity_res.data['last_login'])
        self.assertTrue(activity_res.data['last_made_request'])
