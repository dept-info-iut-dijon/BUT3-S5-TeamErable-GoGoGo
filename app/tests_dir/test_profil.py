from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from ..models.custom_user import CustomUser
from ..models.statistic import Statistic
import os
from django.conf import settings

class ProfileViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Creation d'un utilisateur test
        self.statistic = Statistic.objects.create(
            game_win = 0,
            game_loose = 0,
            game_ranked_win = 0,
            game_ranked_loose = 0,
            
        )
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpass',
            email='testuser@example.com',
            stat=self.statistic
        )
        # Connexion de l'utilisateur
        self.client.login(username='testuser', password='testpass')

    # Test du chargement de la vue profil
    def test_profile_view(self):
        response = self.client.get('/profile')
        # Verification du code status
        self.assertEqual(response.status_code, 200)
        # Verification du chargement avec la bonne template
        self.assertTemplateUsed(response, 'profile/profile.html')
        # Verification de la validite des donnees
        self.assertEqual(response.context['user'], self.user)

    # Test du changement des informations utilisateur
    def test_change_user_info(self):
        new_username = 'newusername'
        new_email = 'newuser@example.com'

        response = self.client.post('/change-user-info', {
            'username': new_username,
            'email': new_email
        })
        # Verification du code status
        self.assertEqual(response.status_code, 200)
        updated_user = get_user_model().objects.get(id=self.user.id)
        # Verification de la mise a jour des donnees
        self.assertEqual(updated_user.username, new_username)
        self.assertEqual(updated_user.email, new_email)

    # Test du changement de photo de profil
    def test_change_pfp(self):
        self.client.login(username='testuser', password='testpass')
        new_pfp_path = os.path.join(settings.BASE_DIR, 'static/test', 'test.png')

        with open(new_pfp_path, 'rb') as new_pfp:
            response = self.client.post('/change-pfp', {'pfp': new_pfp})
        # Verification du code status
        self.assertEqual(response.status_code, 200)
        # Mise a jour de l'utilisateur
        updated_user = get_user_model().objects.get(id=self.user.id)
        # Verification du chemin de la nouvelle image
        expected_path = os.path.join(settings.BASE_DIR, 'static\profile_pictures', '')
        self.assertTrue(updated_user.profile_picture.path.startswith(expected_path))