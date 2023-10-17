from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models.custom_user import CustomUser

class LogInTestCase(TestCase):
    def setUp(self):
        self.sample_user = get_user_model().objects.create_user(
            username='testuser',
            email='testemail@sezamail.net',
            password='testpassword123'
        )
        sample_data = {
            "username":'testuser',
            "email":'testemail@sezamail.net',
            "password1":'testpassword123',
            "password2":'testpassword123'
        }
        response = self.client.post('/register', sample_data)
        self.login_data = {
            'username':'testuser',
            'password':'testpassword123'
        }

    def test_successful_login(self):
        response = self.client.post('/login', self.login_data)
        self.assertEqual(response.status_code, 302)