from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from ..logic import Board
from ..models.custom_user import CustomUser
from ..models.statistic import Statistic

class InitGameTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.statistic = Statistic.objects.create(
            game_win = 0,
            game_loose = 0,
            game_ranked_win = 0,
            game_ranked_loose = 0,
        )
        self.sample_user = get_user_model().objects.create_user(
            username='testuser',
            email='testemail@sezamail.net',
            password='testpassword123',
            stat=self.statistic
        )
        self.client.login(username='testuser', password='testpass')
        self.response = self.client.post('/create_game/', {
            'game-name': 'Test Game',
            'game-desc': 'Description for the test game',
            'game-private': False,
            'map-size': '9x9',
            'game-rules': 'japanese',
            'byo_yomi':30,
            'clock-type': 'Byo-yomi',
            'time-clock':3600,
            'komi':6.5
        })

    # Test de la creation de partie
    def test_create_game(self):
        # On verifie si l'utilisateur est redirige vers la bonne page
        self.assertEqual(self.response.status_code, 302)
        self.assertTrue(self.response.url.startswith('/game?id='))
        # On verifie que l'objet Game est cree correctement
        created_game = Game.objects.get(name='Test Game')
        self.assertEqual(created_game.description, 'Description for the test game')
        self.assertEqual(created_game.done, False)

    # Test de l'initialisation correcte du terrain
    def test_initialisation(self):
        expected_board = [[None for _ in range(9)] for _ in range(9)]

        actual_board = Board(9)
        with open(game.move_list.path, 'r') as f:
            actual_board.load(json.load(f))
        # Verification de la taille du plateau
        self.assertEqual(Vector2(9, 9), actual_board.size())
        # Verification que le plateau est vide
        self.assertEqual(expected_board, actual_board.raw())

    def test_handicap(self):
        pass
