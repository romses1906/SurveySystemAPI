from django.shortcuts import render
from rest_framework import viewsets, generics
from app_surveys.serializers import SurveySerializer, QuestionSerializer, AnswerSerializer, ChoiceSerializer
from app_surveys.models import Survey, Question, Answer, Choice
from rest_framework.authtoken.admin import User
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.pagination import PageNumberPagination

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from app_surveys.permissions import IsAdminOrReadOnly
from datetime import datetime


class SurveysViewSet(viewsets.ModelViewSet):
    """
    Представление для отображения списка опросов, списка активных опросов, создания опроса, его редактирования
    и удаления.
    """
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        queryset = Survey.objects.all()
        active = self.request.query_params.get('active')
        if active:
            queryset = queryset.filter(date_end__gte=datetime.now(), date_start__lte=datetime.now())
        return queryset


class QuestionsViewSet(viewsets.ModelViewSet):
    """
    Представление для отображения списка вопросов, создания вопроса, его редактирования и удаления.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminOrReadOnly,)


class AnswersViewSet(viewsets.ModelViewSet):
    """
    Представление для отображения списка ответов конкретного пользователя, создания ответа,
    его редактирования и удаления.
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Answer.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChoicesViewSet(viewsets.ModelViewSet):
    """
    Представление для отображения списка вариантов ответов на вопросы, создания варианта, его редактирования и удаления.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = (IsAdminOrReadOnly,)
