from django.shortcuts import render

from questions.models import Question

def home(request):
	current_questions = Question.objects.all()
	return render(request, 'home.html', {'current_questions': current_questions})