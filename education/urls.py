from django.urls import path
from rest_framework.routers import DefaultRouter

from education.apps import EducationConfig
from education.views import CourseViewSet, LessonCreateAPIView, \
    LessonRetrieveAPIView, LessonListAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView

app_name = EducationConfig.name

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='comments')


urlpatterns = [
    path('lesson_create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson_detail/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_retrieve'),
    path('lesson_list/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson_update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson_delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
] + router.urls
