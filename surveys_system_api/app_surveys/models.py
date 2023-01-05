from django.contrib.auth.models import User
from django.db import models


class Survey(models.Model):
    """Модель опроса."""
    title = models.CharField(max_length=200, verbose_name='название')
    date_start = models.DateTimeField(auto_now_add=True, verbose_name='дата старта')
    date_end = models.DateTimeField(verbose_name='дата окончания')
    description = models.CharField(max_length=200, verbose_name='описание')

    def __str__(self):
        return self.title


class Question(models.Model):
    """Модель вопроса."""
    CHOICES = (
        ('text', 'Ответ текстом'),
        ('one_option', 'Ответ с выбором одного варианта ответа'),
        ('many_options', 'Ответ с выбором нескольких вариантов ответа'),
    )
    question_text = models.CharField(max_length=200, verbose_name='текст вопроса')
    question_type = models.CharField(max_length=200, choices=CHOICES, verbose_name='тип вопроса')
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE, verbose_name='опрос')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    """
    Модель выбора варианта ответа.
    """
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE, verbose_name='вопрос')
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text


class Answer(models.Model):
    """
    Модель ответа.
    """
    user = models.ForeignKey(User, related_name='answers', on_delete=models.CASCADE, verbose_name='пользователь', blank=True, null=True)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE, verbose_name='вопрос')
    choice = models.ForeignKey(Choice, related_name='answers', on_delete=models.CASCADE, verbose_name='выбор', blank=True, null=True)
    answer_text = models.CharField(max_length=200, verbose_name='текст ответа', blank=True, null=True)

    def __str__(self):
        if self.answer_text:
            return self.answer_text
        return self.choice.choice_text
