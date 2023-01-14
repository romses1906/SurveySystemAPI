from rest_framework import serializers
from app_surveys.models import Survey, Question, Choice, Answer
from datetime import datetime


class ChoiceSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Выбор"""

    question_text = serializers.CharField(source='question.question_text', read_only=True)
    question = serializers.SlugRelatedField(
        queryset=Question.objects.all(),
        slug_field='id')

    class Meta:
        model = Choice
        fields = ['id', 'question', 'question_text', 'choice_text']


class QuestionSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Вопрос"""

    survey = serializers.CharField(source='survey.title', read_only=True)
    survey_id = serializers.IntegerField()
    question_type_display = serializers.ChoiceField(source='get_question_type_display', choices=Question.CHOICES,
                                                    read_only=True)
    question_type = serializers.ChoiceField(choices=Question.CHOICES, write_only=True)
    choices = serializers.SlugRelatedField(many=True, read_only=True, slug_field='choice_text')

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'question_type_display', 'survey', 'survey_id', 'choices']

    def validate(self, attrs):
        survey_id = attrs['survey_id']
        list_id = Survey.objects.values_list('id', flat=True)
        if survey_id in list_id:
            return attrs
        raise serializers.ValidationError(f'В базе данных отсутствует опрос с id = {survey_id}')


class SurveySerializer(serializers.ModelSerializer):
    """Сериалайзер модели Опрос"""

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = ['id', 'title', 'date_start', 'date_end', 'description', 'questions']


class AnswerSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Ответ"""

    user = serializers.ReadOnlyField(source='user.username')
    question_text = serializers.CharField(source='question.question_text', read_only=True)
    question = serializers.SlugRelatedField(queryset=Question.objects.all(), slug_field='id')
    choice = serializers.SlugRelatedField(queryset=Choice.objects.all(), slug_field='id', allow_null=True,
                                          required=False)
    choice_text = serializers.CharField(source='choice.choice_text', allow_null=True, required=False, read_only=True)

    answer_text = serializers.CharField(max_length=200, allow_null=True, required=False)
    survey = serializers.ReadOnlyField(source='question.survey.title')

    class Meta:
        model = Answer
        fields = ['id', 'user', 'survey', 'question', 'question_text', 'choice', 'choice_text', 'answer_text']

    def validate(self, attrs):
        question_type = Question.objects.get(id=attrs['question'].id).question_type
        try:
            if question_type == "one_option" or question_type == "text":
                obj = Answer.objects.get(question=attrs['question'].id)
            elif question_type == "many_options":
                obj = Answer.objects.get(question=attrs['question'].id,
                                         choice=attrs['choice'].id)
        except Answer.DoesNotExist:
            return attrs
        else:
            raise serializers.ValidationError('Вы уже отвечали на этот вопрос.')

    def validate_question(self, value):
        survey_id = value.survey.id
        active_surveys = Survey.objects.filter(date_end__gte=datetime.now(), date_start__lte=datetime.now())
        active_surveys_ids = active_surveys.values_list('id', flat=True)
        if survey_id in active_surveys_ids:
            return value
        raise serializers.ValidationError(f'Опрос, содержащий данный вопрос, завершен.')
