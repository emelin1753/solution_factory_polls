from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):

	question_types = (
		('TC', 'text choice'),
		('OC', 'one choice'),
		('SC', 'several choice'),
		)

	question_text = models.CharField(max_length=200)
	question_type = models.CharField(max_length=2, choices = question_types, default=question_types[0])
	pub_date = models.DateTimeField('date published')
	fin_date = models.DateTimeField('date finished')

	def __str__(self):
		return self.question_text


class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)

	def __str__(self):
		return self.choice_text


class QuestionResults(models.Model):
	question = models.ForeignKey(Question, on_delete=models.PROTECT)
	user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
	#choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True, blank=True)
	votes_text = models.CharField(max_length=200)

	def __str__(self):
		return self.votes_text