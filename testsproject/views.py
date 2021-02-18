from django.http import HttpResponse


def home(request):
	return HttpResponse('<h1>This is home page <a href="/polls/">->опросы</a></h1>')
