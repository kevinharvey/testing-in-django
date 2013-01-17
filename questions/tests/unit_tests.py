from django.test import TestCase

class HomePageViewTest(TestCase):
	
	def test_root_url_shows_questions(self):
		"""
		Test the home page view
		"""
		response = self.client.get('/')
		self.assertEquals(response.status_code, 200)
		
		self.assertTemplateUsed(response, 'home.html')