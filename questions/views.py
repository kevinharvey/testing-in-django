from django.shortcuts import render
from django.http import HttpResponseRedirect

from questions.models import Question

def home(request):
	current_questions = Question.objects.all().order_by('-votes')
	return render(request, 'home.html', {'current_questions': current_questions})
	
def vote(request, pk, verb):
	q = Question.objects.get(id=pk)
	if verb == "up":
		q.increment_votes(1)
	elif verb == "down":
		q.increment_votes(-1)
	return HttpResponseRedirect('/')
	
def ask(request):
	if request.method == "POST":
		new_question = Question(request.POST)
		new_question.save()
	return HttpResponseRedirect('/')
