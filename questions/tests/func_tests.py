from django.test import LiveServerTestCase
from django.core.urlresolvers import reverse
from selenium import webdriver

import time

class QuestionsTest(LiveServerTestCase):
	
	fixtures = ['questions', 'admin_users']

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def test_can_vote_only_once_per_question(self):
		# Bruce opens his web browser and visits Torquemada
		self.browser.get(self.live_server_url + '/')

		# He knows it's Torquemada because he sees the name
		# in the heading
		heading = self.browser.find_element_by_css_selector("h1#trq-heading")
		self.assertEqual(heading.text, "Torquemada")
				
		# He sees a question that he'd like to have answered, and votes it up
		vote_for_1 = self.browser.find_element_by_css_selector("div#trq-question-1 a.trq-vote-up").click()
		vote_tally = self.browser.find_element_by_css_selector("div#trq-question-1 .trq-vote-count")
		self.assertEqual(vote_tally.text, "Votes: 1")

		# He is of a dubious character and tries to vote up the same question by URL
		# He must do by URL because we remove upvote link after successful vote
		# However, you may only vote on a question a single time
		self.browser.get(self.live_server_url + reverse('vote', args=[1, "up"]))
		vote_tally = self.browser.find_element_by_css_selector("div#trq-question-1 .trq-vote-count")
		self.assertEqual(vote_tally.text, "Votes: 1")

		# He changes his mind and votes down the question
		down_vote_for_1 = self.browser.find_element_by_css_selector("div#trq-question-1 a.trq-vote-down").click()
		vote_tally = self.browser.find_element_by_css_selector("div#trq-question-1 .trq-vote-count")
		self.assertEqual(vote_tally.text, "Votes: -1")

	def test_can_read_vote_and_ask_a_question(self):
		# Isabel opens her web browser and visits Torquemada
		self.browser.get(self.live_server_url + '/')

		# She knows it's Torquemada because she sees the name
		# in the heading
		heading = self.browser.find_element_by_css_selector("h1#trq-heading")
		self.assertEqual(heading.text, "Torquemada")

		# She browses through the existing questions
		question_1 = self.browser.find_element_by_css_selector("div#trq-question-1 h4")
		self.assertEqual(question_1.text, "How can my team get started with testing?")
		question_2 = self.browser.find_element_by_css_selector("div#trq-question-2 h4")
		self.assertEqual(question_2.text, "Does Selenium only work in Firefox?")
				
		# She sees a question that she'd like to have answered, and votes it up
		vote_for_2 = self.browser.find_element_by_css_selector("div#trq-question-2 a.trq-vote-up").click()
		vote_tally = self.browser.find_element_by_css_selector("div#trq-question-2 .trq-vote-count")
		self.assertEqual(vote_tally.text, "Votes: 1")
		
		# Her voted up question is now at the top of the list
		all_questions = self.browser.find_elements_by_css_selector("div.trq-question")
		self.assertEqual(all_questions[0].get_attribute("id"), "trq-question-2")
		
		# She sees a silly question and votes it down. No time for that type of stuff 
		# in a Django talk
		question_3 = self.browser.find_element_by_css_selector("div#trq-question-3 h4")
		self.assertEqual(question_3.text, "Why didn't you build this in Wordpress?")
		vote_down_3 = self.browser.find_element_by_css_selector("div#trq-question-3 a.trq-vote-down").click()
		vote_tally_3 = self.browser.find_element_by_css_selector("div#trq-question-3 .trq-vote-count")
		self.assertEqual(vote_tally_3.text, "Votes: -1")
		
		# She then asks a question of her own.
		text_field = self.browser.find_element_by_css_selector("input#id_text")
		text_field.clear()
		text_field.send_keys("Why aren't using reverse() for your URLs in views?")
		self.browser.find_element_by_css_selector("input#trq-submit-question").click()
		
		self.assertEqual(self.browser.find_element_by_css_selector("div#trq-question-4 h4").text,
						 "Why aren't using reverse() for your URLs in views?")
						
	def test_admin_can_manage_questions(self):
		# Peter goes to the admin site and sees the familiar "Django Administration" heading
		self.browser.get(self.live_server_url + '/admin/')
		body = self.browser.find_element_by_tag_name('body')
		self.assertIn('Django administration', body.text)
		
		# Reassured, he logs in
		username = self.browser.find_element_by_css_selector("input#id_username")
		username.clear()
		username.send_keys("peter")
		password = self.browser.find_element_by_css_selector("input#id_password")
		password.clear()
		password.send_keys("password")
		self.browser.find_element_by_css_selector("input[type='submit']").click()
		
		# He navigates to the admin list of questions
		self.browser.find_elements_by_link_text("Questions")[1].click()
		
		# He selects one and archives it
		self.browser.find_element_by_link_text("Why didn't you build this in Wordpress?").click()
		status_select = self.browser.find_element_by_css_selector("#id_status")
		for option in status_select.find_elements_by_tag_name('option'):
			if option.text == 'archived':
				option.click()
		self.browser.find_element_by_css_selector("input[type='submit']").click()
		
		# He goes to the homepage and confirms that the question is no longer visible
		self.browser.get(self.live_server_url + '/')
		body = self.browser.find_element_by_tag_name('body')
		self.assertNotIn("Why didn't you build this in Wordpress?", body.text)
