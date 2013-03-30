from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.conf import settings

from questions.models import Question
from questions.forms import QuestionForm

def home(request):
	current_questions = Question.objects.exclude(status="archived").order_by('-votes')
	form = QuestionForm()
	return render(request, 'home.html', {'current_questions': current_questions,
										 'form': form,
										 'request': request,})
	
def vote(request, pk, verb):
	q = Question.objects.get(id=pk)
	question_vote_key = '%s%s' % (settings.TORQUEMADA_SESSION_VOTES_PREFIX, pk)
	current_vote = request.session.get(question_vote_key, 0)
	if verb == "up" and current_vote != 1:
		q.increment_votes(1 - current_vote)
		request.session[question_vote_key] = 1
	elif verb == "down" and current_vote != -1:
		q.increment_votes(-1 - current_vote)
		request.session[question_vote_key] = -1
	return HttpResponseRedirect('/')
	
def cancel_vote(request, pk):
	q = Question.objects.get(id=pk)
	question_vote_key = '%s%s' % (settings.TORQUEMADA_SESSION_VOTES_PREFIX, pk)
	current_vote = request.session.get(question_vote_key, 0)
	q.increment_votes(-1 * current_vote)
	del request.session[question_vote_key]
	return HttpResponseRedirect('/')
	
def ask(request):
	if request.method == "POST":
		question_form = QuestionForm(request.POST)
		question_form.save()
	return HttpResponseRedirect('/')
