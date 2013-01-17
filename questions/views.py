from django.shortcuts import render
from django.http import HttpResponseRedirect

from questions.models import Question

def home(request):
	current_questions = Question.objects.all()
	return render(request, 'home.html', {'current_questions': current_questions})
	
def voteup(request, pk):
	q = Question.objects.get(id=pk)
	q.increment_votes(1)
	return HttpResponseRedirect('/')