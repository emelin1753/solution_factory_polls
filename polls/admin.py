from django.contrib import admin

# Register your models here.
from .models import Choice, Question

class ChoiceInline(admin.TabularInline):
	model = Choice
	extra = 1


class QuestionAdmin(admin.ModelAdmin):
	
	fieldsets = [
	(None,	
		{'fields': ['question_text', 'question_type']}),
		('Date information', {'fields': ['pub_date', 'fin_date'], 'classes': ['collapse']}),
		]
	
	#readonly_fields = ('pub_date',)
	inlines = [ChoiceInline]
	list_display = ('question_text', 'pub_date', 'fin_date')

	def get_readonly_fields(self, request, obj = None):
		
		if obj is not None and obj.pub_date is not None:
			return ('pub_date')
		return ()

admin.site.register(Question, QuestionAdmin)