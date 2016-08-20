from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic

from .models import Question, Choice

# non-generic inefficient use of views

#def index(request):
#	latest_question_list = Question.objects.order_by('-pub_date')[:5]
#	context = {
#		'latest_question_list':latest_question_list,
#	}
#	return render(request, 'polls/index.html', context)
#
#def detail(request, question_id):
#	question = get_object_or_404(Question, pk=question_id)
#	context = {
#		'question':question,	
#	}
#	return render(request, 'polls/detail.html', context)
#
#def results(request, question_id):
#	question = get_object_or_404(Question, pk=question_id)
#	context = { 
#		'question': question,
#	}
#	return render(request, 'polls/results.html', context)
#

class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'
	
	def get_queryset(self):
		"""return the last five published questions."""
		return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except(KeyError, Choice.DoesNotExist):
		# redisplay the question voting form
		context = {
			'question': question,
			'error_message': "You didn't select an option",
		}
		return render(request, 'polls/detail.html', context)
	else:
		selected_choice.votes += 1
		selected_choice.save()	
		# always retrun a httpresponserediect after sucessfully dealing with POST data.
		# this will prevent data from being posted twice if a user hits the back button.
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

