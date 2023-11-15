from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from ...models.custom_user import CustomUser
from ...models.statistic import Statistic
import os
from django.conf import settings

class FriendsTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Creation d'un utilisateur test
        self.statistic = Statistic.objects.create(
            game_win = 0,
            game_loose = 0,
            game_ranked_win = 0,
            game_ranked_loose = 0,
            
        )
        with open(os.path.join(settings.BASE_DIR, 'static/test', 'test.png'), 'rb') as new_pfp:
            self.user = CustomUser.objects.create_user(
                username='testuser',
                password='testpass',
                email='testuser@example.com',
                stat=self.statistic,
                profile_picture=SimpleUploadedFile("test.png", new_pfp.read(), content_type="image/png")
            )
            self.friend = CustomUser.objects.create_user(
                username='friend',
                password='testpass',
                email='friend@example.com',
                stat=self.statistic,
                profile_picture=SimpleUploadedFile("test2.png", new_pfp.read(), content_type="image/png")
            )
        
        self.user.friends.add(self.friend)
        # Connexion de l'utilisateur
        self.client.login(username='testuser', password='testpass')

    # Test du listage des amis
    def test_list_friends(self):
        response = self.client.get('/friend-list')
        self.assertEqual(response.status_code, 200)

    # Test de la recherche de nouveau amis
    def test_search_not_friend(self):
        random_user = CustomUser.objects.create_user(
            username='user1',
            password='userpass',
            email='user1@example.com',
            stat=self.statistic
        )
        response = self.client.post('/search-notfriend-user', {'username': 'user1'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'reusable/search_user.html')
        users_in_context = [user for user in response.context['users']]
        self.assertIn(random_user, users_in_context)

    # Test de l'ajout d'ami
    def test_add_friend(self):
        friend = CustomUser.objects.create_user(
            username='newfriend',
            password='friendpass',
            email='newfriend@example.com',
            stat=self.statistic
        )
        response = self.client.get('/add-friend', {'id': friend.id})
        # Verification code status
        self.assertEqual(response.status_code, 200)
        # Verification du message de reponse
        self.assertContains(response, f'{friend.username} a été ajouté à vos amis.')
        # Verification de la modification de donnee
        self.assertTrue(self.user.friends.filter(id=friend.id).exists())

    # Test de la suppresion d'ami
    def test_remove_friend(self):
        response = self.client.get('/delete-friend', {'id': self.friend.id})
        # Verification code status
        self.assertEqual(response.status_code, 200)
        # Verification du message de reponse
        self.assertContains(response, f'{self.friend.username} a été supprimé de vos amis.')
        # Verification de la modification de donnee
        self.assertFalse(self.user.friends.filter(id=self.friend.id).exists())