from django.test import TestCase, Client
from ...models.custom_user import CustomUser

class SignUpTestCase(TestCase):
	def setUp(self):
		self.sample_data = {
			'username': 'testuser',
			'email': 'testemail@sezamail.net',
			'password1': 'testpassword123',
			'password2': 'testpassword123',
		}

	def test_successful(self):
		response = self.client.post('/register', self.sample_data)
		self.assertEqual(response.status_code, 302)

	def test_failed(self):
		invalid_sample = {
			'username':'testuser2',
			'email':'testemail@sezamail.net',
			'password1': 'testpassword123',
			'password2': 'error',
		}
		response = self.client.post('/register',invalid_sample)
		self.assertEqual(response.status_code, 400)