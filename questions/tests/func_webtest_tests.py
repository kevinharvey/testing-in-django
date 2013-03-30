from django_webtest import WebTest
from bs4 import BeautifulSoup

class WebTestQuestionsTest(WebTest):
	
	fixtures = ['questions', 'admin_users']

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_can_read_vote_and_ask_a_question(self):
		# Isabel opens her web browser and visits Torquemada
		response = self.app.get('/')

		# She knows it's Torquemada because she sees the name
		# in the heading
		# Note that it seems you need to prepend the opening html tag
		soup = BeautifulSoup('<html>%s' % response.html)
		heading = soup.find('h1', id='trq-heading')
		self.assertEqual(heading.text, "Torquemada")

		# She browses through the existing questions
		question_1 = soup.select('div#trq-question-1 h4')[0]
		self.assertEqual(question_1.text, "How can my team get started with testing?")
		question_2 = soup.select('div#trq-question-2 h4')[0]
		self.assertEqual(question_2.text, "Does Selenium only work in Firefox?")
				
		# She sees a question that she'd like to have answered, and votes it up
		response = response.click(href='/vote/2/up/').follow()
		soup = BeautifulSoup('<html>%s' % response.html)
		vote_tally = soup.select('div#trq-question-2 .trq-vote-count')[0]
		self.assertEqual(vote_tally.text, "Votes: 1")

		# Her voted up question is now at the top of the list
		all_questions = soup.select("div.trq-question")
		self.assertEqual(all_questions[0]['id'], "trq-question-2")

		# She sees a silly question and votes it down. No time for that type of stuff
		# in a Django talk
		question_3 = soup.select("div#trq-question-3 h4")[0]
		self.assertEqual(question_3.text, "Why didn't you build this in Wordpress?")
		response = response.click(href='/vote/3/down/').follow()
		soup = BeautifulSoup('<html>%s' % response.html)
		vote_tally_3 = soup.select('div#trq-question-3 .trq-vote-count')[0]
		self.assertEqual(vote_tally_3.text, "Votes: -1")
		
		# She then asks a question of her own.
		form = response.form
		form['text'] = "Why aren't using reverse() for your URLs in views?"
		response = form.submit().follow()
		soup = BeautifulSoup('<html>%s' % response.html)
		question_4 = soup.select('div#trq-question-4 h4')[0]
		self.assertEqual(question_4.text,
						 "Why aren't using reverse() for your URLs in views?")

	def test_admin_can_manage_questions(self):
		# Peter goes to the admin site and sees the familiar "Django Administration" heading
		response = self.app.get('/admin/')
		# Note the mustcontain will raise an error if the string is not found
		# And will also let you know what was on the page
		self.assertIsNone(response.mustcontain('Django administration'))

		# Reassured, he logs in
		form = response.form
		form['username'] = "peter"
		form['password'] = "password"
		response = form.submit().follow()
		soup = BeautifulSoup('<html>%s' % response.html)

    # He navigates to the admin list of questions
		response = response.click(href='/admin/questions/', index=1)

    # He selects one for deleting
		form = response.form
		form.set('action', 'delete_selected')
		form.set('_selected_action', True, 0)
		response = form.submit()

		# And confirms that he does indeed want to delete it
		form = response.form
		form.set('action', 'delete_selected')
		form.set('_selected_action', '3')
		form.set('post', 'yes')
		form.submit()

		# He goes to the homepage and confirms that the question is no longer visible
		response = self.app.get('/')
		soup = BeautifulSoup('<html>%s' % response.html)
		body = soup.body
		self.assertNotIn("Why didn't you build this in Wordpress?", body.text)
		# although the other 2 questions do exist
		all_questions = soup.select("div.trq-question")
		self.assertEqual(len(all_questions), 2)