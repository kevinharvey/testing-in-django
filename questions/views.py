from django.shortcuts import render
from django.http import HttpResponseRedirect

from questions.models import Question
from questions.forms import QuestionForm

def home(request):
	current_questions = Question.objects.all().order_by('-votes')
	form = QuestionForm()
	return render(request, 'home.html', {'current_questions': current_questions,
										 'form': form})
	
def vote(request, pk, verb):
	q = Question.objects.get(id=pk)
	if verb == "up":
		q.increment_votes(1)
	elif verb == "down":
		q.increment_votes(-1)
	return HttpResponseRedirect('/')
	
def ask(request):
	if request.method == "POST":
		question_form = QuestionForm(request.POST)
		question_form.save()
	return HttpResponseRedirect('/')
