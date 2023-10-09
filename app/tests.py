from django.test import TestCase

# Create your tests here.
class TestIndex(TestCase):
    def test_index(self) -> None:
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login')
        self.assertTemplateNotUsed(response, 'index.html')
        self.assertTemplateNotUsed(response, 'login.html')
