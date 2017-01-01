from django.shortcuts import render

def index(request):
	context = {
		'title': 'The New Boston Tutorial',
	}
	return render(request, 'tnb/index.html', context) 
