from django.urls import path, include, re_path
from app_surveys.views import SurveysViewSet, QuestionsViewSet, AnswersViewSet, ChoicesViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'surveys', SurveysViewSet)
router.register(r'questions', QuestionsViewSet)
router.register(r'answers', AnswersViewSet)
router.register(r'choices', ChoicesViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    # path('active_surveys/', SurveysActiveAPIList.as_view()),
    # path('auth/', include('djoser.urls')),
    # re_path(r'^auth/', include('djoser.urls.authtoken')),

    # path('surveyslist/', SurveysViewSet.as_view({'get': 'list', 'post': 'create'})),
    # path('surveyslist/<int:pk>/', SurveysViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    # path('books/<int:pk>/', BookDetail.as_view(), name='book_detail'),

]
