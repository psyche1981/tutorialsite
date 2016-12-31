from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question
from django.core.urlresolvers import reverse



# helpers

def create_question(q_text, days):
	'''
	creates a question with the question_text=q_text and the 
	pub_date offset by days
	'''
	time = timezone.now() + datetime.timedelta(days=days)
	return Question.objects.create(question_text=q_text, pub_date=time)

# tests

class QuestionMethodTests(TestCase):

	def test_was_pub_recently_future_question(self):
		'''
		was_published_recently() should return False for a question 
		with a pub_date in the future
		'''
		time = timezone.now() + datetime.timedelta(days=1)
		fut_q = Question(pub_date=time)
		self.assertEqual(fut_q.was_published_recently(), False)

	def test_was_pub_recently_old_question(self):
		'''
		was_published_recently() should return false if the question 
		has a pub_date older than 1 day
		'''
		time = timezone.now() - datetime.timedelta(days=2)
		old_q = Question(pub_date=time)
		self.assertEqual(old_q.was_published_recently(), False)

	def test_was_pub_recently_recent_question(self):
		'''
		was_published_recently() should return true if the question
		has a pub_date within 1 day of now
		'''
		time = timezone.now() - datetime.timedelta(hours=1)
		new_q = Question(pub_date=time)
		self.assertEqual(new_q.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
	
	def test_index_no_questions(self):
		'''
		no questions, appropriate message
		'''
		response = self.client.get(reverse('polls:index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])
	
	def test_index_with_past_question(self):
		'''
		questions with a pub_adte in the past should be displayed
		on the index page
		'''
		create_question('Past question.', -30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

	def test_index_with_future_question(self):
		'''
		questions with a pub_date in the future should not be shown on the index page
		'''	
		create_question('Future Question', 30)
		response = self.client.get(reverse('polls:index'))
		self.assertContains(response, "No polls are available")
		self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_future_and_past_question(self):
		'''
		only past questions should be displayed
		'''
		create_question('Future Question', 30)
		create_question('Past Question', -30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past Question>'])

	def test_index_multiple_past_questions(self):
		'''
		page should be able to display multile questions
		'''
		create_question('Past Question 1', -4)
		create_question('Past Question 2', -30)
		response = self.client.get(reverse('polls:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past Question 1>', '<Question: Past Question 2>'])
	
		
class QuestionDetailViewTests(TestCase):
	def test_detail_future_question(self):
		'''
		detail view should return 404 if a question with future pub_date
		'''
		fut_q = create_question('Future', 10)
		url = reverse('polls:detail', args=(fut_q.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)

	def test_detail_past_question(self):
		'''
		detail view should display the question text for a 
		question with a pub_date in the past
		'''
		past_q = create_question('Past', -10)
		url = reverse('polls:detail', args=(past_q.id,))
		response = self.client.get(url)
		self.assertContains(response, past_q.question_text)
		

