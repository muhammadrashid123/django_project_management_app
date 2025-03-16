from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser


class AccountsAuthTestCase(APITestCase):

    def setUp(self):
        self.register_url = reverse('auth_register')
        self.login_url = reverse('token_obtain_pair')
        self.logout_url = reverse('auth_logout')

        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'strongpassword123',
            'username': 'testuser'
        }
        self.user = CustomUser.objects.create_user(
            email=self.user_data['email'],
            password=self.user_data['password'],
            username=self.user_data['username']
        )

    # Test user registration
    def test_user_registration_success(self):
        data = {
            'email': 'newuser@example.com',
            'password': 'newpassword123',
            'username': 'newuser'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'User registered successfully.')
        self.assertIn('id', response.data['data'])
        self.assertEqual(response.data['data']['email'], data['email'])
        self.assertEqual(response.data['data']['username'], data['username'])

    # Test user login to get token
    def test_user_login_success(self):
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_user_login_wrong_password(self):
        data = {
            'email': self.user_data['email'],
            'password': 'wrongpassword',
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



