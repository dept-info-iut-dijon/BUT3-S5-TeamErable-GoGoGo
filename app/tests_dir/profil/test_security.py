from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ...models import Statistic
from ...forms import ResetPasswordForm

class SecurityTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.statistic = Statistic.objects.create(
            game_win=0,
            game_loose=0,
            game_ranked_win=0,
            game_ranked_loose=0,
        )
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass',
            email='testuser@example.com',
            stat=self.statistic
        )
        self.client.login(username='testuser', password='testpass')

    def test_change_pwd_correct(self):
        response = self.client.post('/change-pwd', {'old-pwd': 'testpass', 'new-pwd': 'Newpassword1+', 'new-pwd-confirm': 'Newpassword1+'})
        self.assertEqual(response.status_code, 200)
        # Add assertions to check if the password is actually changed

    def test_change_pwd_incorrect(self):
        response = self.client.post('/change-pwd', {'old-pwd': 'wrongpass', 'new-pwd': 'Newpassword1+', 'new-pwd-confirm': 'Newpassword1+'})
        error_message = 'L\'ancien mot de passe est incorrect.'
        self.assertIn(error_message, response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 400)

    def test_change_pwd_not_match(self):
        response = self.client.post('/change-pwd', {'old-pwd': 'testpass', 'new-pwd': 'Newpassword1+', 'new-pwd-confirm': 'password'})
        error_message = 'Les mots de passe ne correspondent pas.'
        self.assertIn(error_message, response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 400)

    def test_delete_account_correct_password(self):
        response = self.client.post('/delete-account', {'password': 'testpass'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Votre compte a bien été supprimé.')

    def test_delete_account_incorrect_password(self):
        response = self.client.post('/delete-account', {'password': 'wrongpass'})
        error_message = 'Le mot de passe est incorrect.'
        self.assertIn(error_message, response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 400)