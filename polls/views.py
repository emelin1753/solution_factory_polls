from django.shortcuts import get_object_or_404, render
from .models import Choice, Question, QuestionResults
from django.contrib.auth import authenticate, login
from django.utils import timezone

def get_latest_question_list(filter_date):
	'''функция возвращает доступный на дату (filter_date) список тестов'''
	latest_question_list = Question.objects.filter(pub_date__lte=filter_date, fin_date__gte=filter_date)
	return {'latest_question_list': latest_question_list,}


def get_user(request):
	'''функция возвращает текущего пользователя
	если пользователь не авторизован (anonymous), то возвращается ключ сессии'''
	user = request.user
	if not user.is_authenticated:
		user = request.session.session_key
	return user


def get_question_input_type(question):
	'''функция возвращает настройку для input в разметке выбора варианта ответа,
	в зависимости от от типа вопроса 
	text - подразумевается текстовый ответ
	radio - выбор только одного варианта
	checkbox - выбор нескольких вариантов
	'''
	input_type = 'text'
	if question is not None:
		if question.question_type == 'OC':
			input_type = 'radio'
		elif question.question_type == 'SC':
			input_type = 'checkbox'

	return input_type


def index(request):
	'''функция обрабатывает вывод разметки index.html с выводом доступных тестов'''
	# проверим текущего юзера, и залогинимся для теста
	# этот кусок кода нужно заменить после подключения авторизации пользователей
	#user = authenticate(request, username = 'John', password = 'Johnpassword')
	user = request.user
	if user.is_authenticated:
		login(request, user)
	#______________________________________________________
	return render(request, 'polls/index.html', get_latest_question_list(timezone.now()))


def detail(request, question_id):
	'''функция обрабатывает вывод разметки detail.html с выводом вариантов ответов (choice) по вопросу (question_id)'''
	question = get_object_or_404(Question, pk=question_id)
	return render(request, 'polls/detail.html', {'question': question, 'input_type': get_question_input_type(question),})

def results(request):
	'''функция обрабатывает вывод разметки results.html с результатов ответов (result_votes) для пользователя (user)'''
	user = get_user(request)
	result_votes = QuestionResults.objects.filter(user=user)
	return render(request, 'polls/results.html', {'result_votes':result_votes, 'user':user})


def vote(request, question_id):
	'''функция обрабатывает и записывает в модель БД (QuestionResults) вариант выбора ответа (votes_text)
	для вопроса (question_id) и пользователя (user)
	если не выбран ни один вариант (votes_text == [] or votes_text == [''])
	то предлагается повторный выбор'''
	question = get_object_or_404(Question, pk=question_id)
	votes_text = [value for key, value in request.POST.items() if 'choice' in key]

	if votes_text == [] or votes_text == ['']:
		return render(request, 'polls/detail.html', {'question': question,
			'error_message': "You didn't select a choice.",'input_type': get_question_input_type(question),})

	user = get_user(request)
	vote_result = QuestionResults(question=question, user=user, votes_text=votes_text)
	vote_result.save()
	return render(request, 'polls/index.html', get_latest_question_list(timezone.now()))

