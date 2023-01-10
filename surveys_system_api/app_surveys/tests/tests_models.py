from django.contrib.auth import get_user_model
from django.test import TestCase
from app_surveys.models import Survey, Question, Choice, Answer


class SurveyModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.survey = Survey.objects.create(
            title='Тестовый опрос',
            date_end='2022-04-23 23:15:12',
            description='Тестовое описание'
        )

    def test_verbose_name(self):
        survey = SurveyModelTest.survey
        field_verboses = {
            'title': 'название',
            'date_start': 'дата старта',
            'date_end': 'дата окончания',
            'description': 'описание',

        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(survey._meta.get_field(field).verbose_name, expected_value)

    def test_survey_str(self):
        survey = SurveyModelTest.survey
        self.assertEqual(survey.__str__(), 'Тестовый опрос')


class QuestionModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.survey = Survey.objects.create(
            title='Тестовый опрос',
            date_end='2022-05-23 23:15:12',
            description='Тестовое описание'
        )
        cls.question = Question.objects.create(
            question_text='Тестовый вопрос',
            question_type='text',
            survey=cls.survey
        )

    def test_verbose_name(self):
        question = QuestionModelTest.question
        field_verboses = {
            'question_text': 'текст вопроса',
            'question_type': 'тип вопроса',
            'survey': 'опрос',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(question._meta.get_field(field).verbose_name, expected_value)

    def test_question_str(self):
        question = QuestionModelTest.question
        self.assertEqual(question.__str__(), 'Тестовый вопрос')


class ChoiceModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.survey = Survey.objects.create(
            title='Тестовый опрос',
            date_end='2022-05-23 23:15:12',
            description='Тестовое описание'
        )
        cls.question = Question.objects.create(
            question_text='Тестовый вопрос',
            question_type='text',
            survey=cls.survey
        )
        cls.choice = Choice.objects.create(
            question=cls.question,
            choice_text='тестовый выбор',
        )

    def test_verbose_name(self):
        choice = ChoiceModelTest.choice
        field_verboses = {
            'question': 'вопрос',

        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(choice._meta.get_field(field).verbose_name, expected_value)

    def test_choice_str(self):
        choice = ChoiceModelTest.choice
        self.assertEqual(choice.__str__(), 'тестовый выбор')


class AnswerModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.survey = Survey.objects.create(
            title='Тестовый опрос',
            date_end='2022-04-23 23:15:12',
            description='Тестовое описание'
        )
        cls.question = Question.objects.create(
            question_text='Тестовый вопрос',
            question_type='text',
            survey=cls.survey
        )
        cls.user = get_user_model().objects.create_user(username='testuser', email='email', password='secret')
        cls.choice = Choice.objects.create(
            question=cls.question,
            choice_text='тестовый выбор',
        )
        cls.answer_1 = Answer.objects.create(
            user=cls.user,
            question=cls.question,
            choice=cls.choice,
            answer_text='тестовый ответ'
        )
        cls.answer_2 = Answer.objects.create(
            user=cls.user,
            question=cls.question,
            choice=cls.choice,
        )

    def test_verbose_name(self):
        answer_1 = AnswerModelTest.answer_1
        field_verboses = {
            'user': 'пользователь',
            'question': 'вопрос',
            'choice': 'выбор',
            'answer_text': 'текст ответа',

        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(answer_1._meta.get_field(field).verbose_name, expected_value)

    def test_answer_str(self):
        answer_1 = AnswerModelTest.answer_1
        self.assertEqual(answer_1.__str__(), 'тестовый ответ')
        answer_2 = AnswerModelTest.answer_2
        self.assertEqual(answer_2.__str__(), 'тестовый выбор')
