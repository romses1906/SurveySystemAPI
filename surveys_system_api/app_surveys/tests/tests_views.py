import json
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase, Client
from django.urls import reverse
from app_surveys.models import Survey, Question, Choice, Answer
from app_surveys.serializers import SurveySerializer, ChoiceSerializer, QuestionSerializer, AnswerSerializer

client = Client()


class SurveysAPITest(TestCase):  # переименовать
    """ Test module for GET all surveys API """

    def setUp(self):
        self.survey_1 = Survey.objects.create(
            title='Тестовый опрос 1',
            date_end='2022-04-23 23:15:12',
            description='Тестовое описание 1'
        )
        self.survey_2 = Survey.objects.create(
            title='Тестовый опрос 2',
            date_end='2022-04-23 23:15:12',
            description='Тестовое описание 2'
        )
        self.survey_3 = Survey.objects.create(
            title='Тестовый опрос 3',
            date_end='2022-04-23 23:15:12',
            description='Тестовое описание 3'
        )

        self.valid_payload = {
            'title': 'Тестовый опрос для добавления',
            'date_end': '2022-04-23 23:15:12',
            'description': 'Тестовое описание 1'
        }

        self.invalid_payload = {
            'title': 'Тестовый опрос для добавления невалидный',
            'date_end': '2022-04-23 23:15:12',
            'description': ''
        }
        self.count = Survey.objects.all().count()

        # self.superuser = get_user_model().objects.create_superuser(username='admin', email='email', password='admin')

        # Создаем неавторизованный клиент
        # self.guest_client = Client()
        # Создаем пользователя
        self.superuser = get_user_model().objects.create_superuser(username='admin', email='email', password='admin')
        self.user = get_user_model().objects.create_user(username='test_user', email='email', password='test_password')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.superuser)

    def test_get_all_surveys(self):
        response = client.get(reverse('survey-list'))
        surveys = Survey.objects.all()
        serializer = SurveySerializer(surveys, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_survey(self):
        response = client.get(
            reverse('survey-detail', kwargs={'pk': self.survey_1.pk}))
        survey = Survey.objects.get(pk=self.survey_1.pk)
        serializer = SurveySerializer(survey)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_survey(self):
        response = client.get(
            reverse('survey-detail', kwargs={'pk': 200}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_survey(self):
        response = self.authorized_client.post(
            reverse('survey-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Survey.objects.all().count(), self.count + 1)

    def test_create_invalid_survey(self):
        response = self.authorized_client.post(
            reverse('survey-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Survey.objects.all().count(), self.count)

    def test_not_superuser_not_can_create_survey(self):
        self.authorized_client.force_login(self.user)
        response = self.authorized_client.post(
            reverse('survey-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Survey.objects.all().count(), self.count)

    def test_valid_update_survey(self):
        response = self.authorized_client.put(
            reverse('survey-detail', kwargs={'pk': self.survey_1.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # в примере 204

    def test_invalid_update_survey(self):
        response = self.authorized_client.put(
            reverse('survey-detail', kwargs={'pk': self.survey_1.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_superuser_not_can_update_survey(self):
        self.authorized_client.force_login(self.user)
        response = self.authorized_client.put(
            reverse('survey-detail', kwargs={'pk': self.survey_1.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_delete_survey(self):
        response = self.authorized_client.delete(
            reverse('survey-detail', kwargs={'pk': self.survey_1.pk}),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Survey.objects.all().count(), self.count - 1)

    def test_invalid_delete_survey(self):
        response = self.authorized_client.delete(
            reverse('survey-detail', kwargs={'pk': 200}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Survey.objects.all().count(), self.count)

    def test_not_superuser_not_can_delete_survey(self):
        self.authorized_client.force_login(self.user)
        response = self.authorized_client.delete(
            reverse('survey-detail', kwargs={'pk': self.survey_1.pk}),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class QuestionsAPITest(TestCase):  # переименовать

    def setUp(self):
        super().setUp()
        self.survey_1 = Survey.objects.create(
            title='Тестовый опрос 1',
            date_end='2022-04-23 23:15:12',
            description='Тестовое описание 1'
        )
        self.survey_2 = Survey.objects.create(
            title='Тестовый опрос 2',
            date_end='2022-04-23 23:15:12',
            description='Тестовое описание 2'
        )
        # self.survey_3 = Survey.objects.create(
        #     title='Тестовый опрос 3',
        #     date_end='2022-04-23 23:15:12',
        #     description='Тестовое описание 3'
        # )
        self.question_1 = Question.objects.create(
            question_text='Тестовый вопрос 1',
            question_type='text',
            survey=self.survey_1
        )

        self.valid_payload = {
            'question_text': 'Тестовый вопрос',
            'question_type': 'text',
            'survey_id': self.survey_1.id
        }

        self.invalid_payload = {
            'question_text': 'Тестовый вопрос',
            'question_type': '',
            'survey': self.survey_1.id
        }
        self.count = Question.objects.all().count()

        # self.superuser = get_user_model().objects.create_superuser(username='admin', email='email', password='admin')

        # Создаем неавторизованный клиент
        # self.guest_client = Client()
        # Создаем пользователя
        self.superuser = get_user_model().objects.create_superuser(username='admin', email='email', password='admin')
        self.user = get_user_model().objects.create_user(username='test_user', email='email', password='test_password')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.superuser)

    def test_get_all_questions(self):
        response = client.get(reverse('question-list'))
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_question(self):
        response = client.get(
            reverse('question-detail', kwargs={'pk': self.question_1.pk}))
        question = Question.objects.get(pk=self.question_1.pk)
        serializer = QuestionSerializer(question)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_question(self):
        response = client.get(
            reverse('question-detail', kwargs={'pk': 200}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_question(self):
        response = self.authorized_client.post(
            reverse('question-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.all().count(), self.count + 1)

    def test_create_invalid_question(self):
        response = self.authorized_client.post(
            reverse('question-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Question.objects.all().count(), self.count)

    def test_not_superuser_not_can_create_question(self):
        self.authorized_client.force_login(self.user)
        response = self.authorized_client.post(
            reverse('question-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Question.objects.all().count(), self.count)

    def test_valid_update_question(self):
        response = self.authorized_client.put(
            reverse('question-detail', kwargs={'pk': self.question_1.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # в примере 204

    def test_invalid_update_question(self):
        response = self.authorized_client.put(
            reverse('question-detail', kwargs={'pk': self.question_1.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_superuser_not_can_update_question(self):
        self.authorized_client.force_login(self.user)
        response = self.authorized_client.put(
            reverse('survey-detail', kwargs={'pk': self.question_1.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_delete_question(self):
        response = self.authorized_client.delete(
            reverse('question-detail', kwargs={'pk': self.question_1.pk}),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Question.objects.all().count(), self.count - 1)

    def test_invalid_delete_question(self):
        response = self.authorized_client.delete(
            reverse('question-detail', kwargs={'pk': 200}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Question.objects.all().count(), self.count)

    def test_not_superuser_not_can_delete_question(self):
        self.authorized_client.force_login(self.user)
        response = self.authorized_client.delete(
            reverse('question-detail', kwargs={'pk': self.question_1.pk}),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AnswersAPITest(TestCase):  # переименовать

    def setUp(self):
        super().setUp()
        self.survey_1 = Survey.objects.create(
            title='Тестовый опрос 1',
            date_end='2022-04-23 23:15:12',
            description='Тестовое описание 1'
        )

        self.question = Question.objects.create(
            question_text='Тестовый вопрос 1',
            question_type='text',
            survey=self.survey_1
        )

        self.choice = Choice.objects.create(
            choice_text='Тестовый выбор',
            question=self.question
        )
        self.user_1 = get_user_model().objects.create_user(
            username='test_user_1',
            email='email',
            password='test_password')

        self.user_2 = get_user_model().objects.create_user(
            username='test_user_2',
            email='email',
            password='test_password')

        self.answer_1 = Answer.objects.create(
            choice=self.choice,
            question=self.question,
            user=self.user_1
        )
        self.answer_2 = Answer.objects.create(
            choice=self.choice,
            question=self.question,
            user=self.user_2
        )

        self.valid_payload = {
            'choice_text': 'Валидный тестовый выбор',
            'question_id': self.question.id
        }

        self.invalid_payload = {
            'choice_text': 'Невалидный тестовый выбор',
            'question_id': ''
        }
        # self.count = Choice.objects.all().count()

        # self.superuser = get_user_model().objects.create_superuser(username='admin', email='email', password='admin')

        # Создаем неавторизованный клиент
        # self.guest_client = Client()
        # # Создаем пользователя
        # # self.superuser = get_user_model().objects.create_superuser(username='admin', email='email', password='admin')
        # # Создаем второй клиент
        # self.authorized_client = Client()
        # # Авторизуем пользователя
        # self.authorized_client.force_login(self.user_1)
        # self.authorized_client.force_login(self.user_2)

    def test_get_user_answers(self):
        # self.client = APIClient()
        # self.client.force_authenticate(self.user_1)
        response = client.get(reverse('answer-list'))
        answers = Answer.objects.filter(user=self.user_1)

        serializer = AnswerSerializer(answers, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_get_valid_single_choice(self):
#         response = client.get(
#             reverse('choice-detail', kwargs={'pk': self.choice.pk}))
#         choice = Choice.objects.get(pk=self.choice.pk)
#         serializer = ChoiceSerializer(choice)
#         self.assertEqual(response.data, serializer.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_get_invalid_single_choice(self):
#         response = client.get(
#             reverse('choice-detail', kwargs={'pk': 200}))
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#
#     def test_create_valid_choice(self):
#         response = self.authorized_client.post(
#             reverse('choice-list'),
#             data=json.dumps(self.valid_payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Choice.objects.all().count(), self.count + 1)
#
#     def test_create_invalid_choice(self):
#         response = self.authorized_client.post(
#             reverse('choice-list'),
#             data=json.dumps(self.invalid_payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(Choice.objects.all().count(), self.count)
#
#     def test_not_superuser_not_can_create_choice(self):
#         self.authorized_client.force_login(self.user)
#         response = self.authorized_client.post(
#             reverse('choice-list'),
#             data=json.dumps(self.valid_payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.assertEqual(Choice.objects.all().count(), self.count)
#
#     def test_valid_update_choice(self):
#         response = self.authorized_client.put(
#             reverse('choice-detail', kwargs={'pk': self.choice.pk}),
#             data=json.dumps(self.valid_payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_invalid_update_choice(self):
#         response = self.authorized_client.put(
#             reverse('choice-detail', kwargs={'pk': self.choice.pk}),
#             data=json.dumps(self.invalid_payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#
#     def test_not_superuser_not_can_update_choice(self):
#         self.authorized_client.force_login(self.user)
#         response = self.authorized_client.put(
#             reverse('choice-detail', kwargs={'pk': self.choice.pk}),
#             data=json.dumps(self.valid_payload),
#             content_type='application/json'
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_valid_delete_choice(self):
#         response = self.authorized_client.delete(
#             reverse('choice-detail', kwargs={'pk': self.choice.pk}),
#         )
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(Choice.objects.all().count(), self.count - 1)
#
#     def test_invalid_delete_choice(self):
#         response = self.authorized_client.delete(
#             reverse('choice-detail', kwargs={'pk': 200}),
#         )
#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
#         self.assertEqual(Choice.objects.all().count(), self.count)
#
#     def test_not_superuser_not_can_delete_choice(self):
#         self.authorized_client.force_login(self.user)
#         response = self.authorized_client.delete(
#             reverse('choice-detail', kwargs={'pk': self.choice.pk}),
#         )
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ChoicesAPITest(TestCase):  # переименовать

    def setUp(self):
        super().setUp()
        self.survey_1 = Survey.objects.create(
            title='Тестовый опрос 1',
            date_end='2022-04-23 23:15:12',
            description='Тестовое описание 1'
        )

        self.question = Question.objects.create(
            question_text='Тестовый вопрос 1',
            question_type='text',
            survey=self.survey_1
        )

        self.choice = Choice.objects.create(
            choice_text='Тестовый выбор',
            question=self.question
        )

        self.valid_payload = {
            'choice_text': 'Валидный тестовый выбор',
            'question_id': self.question.id
        }

        self.invalid_payload = {
            'choice_text': 'Невалидный тестовый выбор',
            'question_id': ''
        }
        self.count = Choice.objects.all().count()

        # self.superuser = get_user_model().objects.create_superuser(username='admin', email='email', password='admin')

        # Создаем неавторизованный клиент
        # self.guest_client = Client()
        # Создаем пользователя
        self.superuser = get_user_model().objects.create_superuser(username='admin', email='email', password='admin')
        self.user = get_user_model().objects.create_user(username='test_user', email='email', password='test_password')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.superuser)

    def test_get_all_choices(self):
        response = client.get(reverse('choice-list'))
        choices = Choice.objects.all()
        serializer = ChoiceSerializer(choices, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_choice(self):
        response = client.get(
            reverse('choice-detail', kwargs={'pk': self.choice.pk}))
        choice = Choice.objects.get(pk=self.choice.pk)
        serializer = ChoiceSerializer(choice)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_choice(self):
        response = client.get(
            reverse('choice-detail', kwargs={'pk': 200}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_valid_choice(self):
        response = self.authorized_client.post(
            reverse('choice-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Choice.objects.all().count(), self.count + 1)

    def test_create_invalid_choice(self):
        response = self.authorized_client.post(
            reverse('choice-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Choice.objects.all().count(), self.count)

    def test_not_superuser_not_can_create_choice(self):
        self.authorized_client.force_login(self.user)
        response = self.authorized_client.post(
            reverse('choice-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Choice.objects.all().count(), self.count)

    def test_valid_update_choice(self):
        response = self.authorized_client.put(
            reverse('choice-detail', kwargs={'pk': self.choice.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_choice(self):
        response = self.authorized_client.put(
            reverse('choice-detail', kwargs={'pk': self.choice.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_superuser_not_can_update_choice(self):
        self.authorized_client.force_login(self.user)
        response = self.authorized_client.put(
            reverse('choice-detail', kwargs={'pk': self.choice.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_valid_delete_choice(self):
        response = self.authorized_client.delete(
            reverse('choice-detail', kwargs={'pk': self.choice.pk}),
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Choice.objects.all().count(), self.count - 1)

    def test_invalid_delete_choice(self):
        response = self.authorized_client.delete(
            reverse('choice-detail', kwargs={'pk': 200}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Choice.objects.all().count(), self.count)

    def test_not_superuser_not_can_delete_choice(self):
        self.authorized_client.force_login(self.user)
        response = self.authorized_client.delete(
            reverse('choice-detail', kwargs={'pk': self.choice.pk}),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
