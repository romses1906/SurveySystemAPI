from django.contrib import admin
from app_surveys.models import Survey, Question, Choice, Answer


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_start', 'date_end')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'question_type', 'survey')


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice_text')


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'choice', 'answer_text')


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Answer, AnswerAdmin)

