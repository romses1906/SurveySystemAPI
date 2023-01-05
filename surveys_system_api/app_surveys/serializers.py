from rest_framework import serializers
from app_surveys.models import Survey, Question, Choice, Answer


class ChoiceSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Выбор"""

    question = serializers.CharField(source='question.question_text', read_only=True)
    question_id = serializers.IntegerField()

    class Meta:
        model = Choice
        fields = ['id', 'question', 'question_id', 'choice_text']


class QuestionSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Вопрос"""

    survey = serializers.CharField(source='survey.title', read_only=True)
    survey_id = serializers.IntegerField()
    question_type_display = serializers.ChoiceField(source='get_question_type_display', choices=Question.CHOICES,
                                                    read_only=True)
    question_type = serializers.ChoiceField(choices=Question.CHOICES, write_only=True)
    choices = serializers.SlugRelatedField(many=True, read_only=True, slug_field='choice_text')

    # survey = serializers.StringRelatedField()
    # survey = serializers.ChoiceField(source='survey.title', choices=Survey.objects.all())
    # question_type = serializers.CharField(source='get_question_type_display')
    # question_type = serializers.ChoiceField(choices=Question.CHOICES, default='text')
    # choices = ChoiceSerializer(many=True, read_only=True)
    # choice = serializers.CharField(source='question__choices.choice_text')
    # choices = ChoiceSerializer(source='question__choices.choice_text')

    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'question_type_display', 'survey', 'survey_id', 'choices']

    def validate(self, attrs):
        survey_id = attrs['survey_id']
        if survey_id in Survey.objects.all():
            return attrs
        raise serializers.ValidationError(f'В базе данных отсутствует опрос с id = {survey_id}')


class SurveySerializer(serializers.ModelSerializer):
    """Сериалайзер модели Опрос"""

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = ['id', 'title', 'date_start', 'date_end', 'description', 'questions']


# class ChoiceTwoSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Choice
#         fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    """Сериалайзер модели Ответ"""

    user = serializers.ReadOnlyField(source='user.username')
    question = serializers.CharField(source='question.question_text', read_only=True)
    question_id = serializers.IntegerField()
    choice = serializers.CharField(source='choice.choice_text', allow_null=True, required=False, read_only=True)
    choice_id = serializers.IntegerField(required=False)
    # choice = ChoiceTwoSerializer(required=False)
    # choice = serializers.SlugRelatedField(queryset=Choice.objects.all(), slug_field='choice_text', allow_null=True, required=False)
    answer_text = serializers.CharField(max_length=200, allow_null=True, required=False)
    survey = serializers.ReadOnlyField(source='question.survey.title')


    class Meta:
        model = Answer
        fields = ['id', 'user', 'survey', 'question', 'question_id', 'choice', 'choice_id', 'answer_text']

    def validate(self, attrs):
        question_type = Question.objects.get(id=attrs['question_id']).question_type
        try:
            if question_type == "one_option" or question_type == "text":
                obj = Answer.objects.get(question=attrs['question_id'])
            elif question_type == "many_options":
                obj = Answer.objects.get(question=attrs['question_id'],
                                         choice=attrs['choice_id'])
        except Answer.DoesNotExist:
            return attrs
        else:
            raise serializers.ValidationError('Вы уже отвечали на этот вопрос.')



