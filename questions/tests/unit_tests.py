from django.test import TestCase
import datetime
from django.utils.timezone import utc

from questions.models import Question

class HomePageViewTest(TestCase):
	
	def test_root_url_shows_questions(self):
		"""
		Test the home page view
		"""
		question_1 = Question(text="How can my team get started with testing?",
							  votes=0,
							  created=datetime.datetime.utcnow().replace(tzinfo=utc),
							  status="new")
		question_1.save()
		question_2 = Question(text="Does Selenium only work in Firefox?",
							  votes=0,
							  created=datetime.datetime.utcnow().replace(tzinfo=utc)-datetime.timedelta(seconds=30),
							  status="new")
		question_2.save()
		
		response = self.client.get('/')
		self.assertEquals(response.status_code, 200)
		
		self.assertTemplateUsed(response, 'home.html')
		
		self.assertTrue('current_questions' in response.context)
		
		second_question = response.context['current_questions'][1]
		self.assertEqual(second_question.text, "Does Selenium only work in Firefox?")