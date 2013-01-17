from django.test import TestCase

class HomePageViewTest(TestCase):
	
	def test_root_url_shows_questions(self):
		"""
		Test the home page view
		"""
		q1 = Question(text="What are some good ways to get started testing?",
					  date_asked=)
		
		response = self.client.get('/')
		self.assertEquals(response.status_code, 200)
		
		self.assertTemplateUsed(response, 'home.html')