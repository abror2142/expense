from django.urls import path, include
from rest_framework import routers

from .views import (CourseAPIView, ClassRoomAPIView, LessonDaysAPIView,
                    ClassTimeAPIView, GroupAPIView, LessonAPIView,
                    LessonVideoAPIView, HomeworkAPIView, LessonCommentAPIView,
                    LessonLikeAPIView, send_notification, search_view)


router = routers.SimpleRouter()
router.register('course', CourseAPIView)
router.register('classroom', ClassRoomAPIView)
router.register('lesson-days', LessonDaysAPIView)
router.register('class-time', ClassTimeAPIView)
router.register('group', GroupAPIView)
router.register('lesson', LessonAPIView)
router.register('lesson-video', LessonVideoAPIView)
router.register('homework', HomeworkAPIView)


urlpatterns = [
    path('', include(router.urls)),
    path('lesson-comment/<int:lesson_id>/', LessonCommentAPIView.as_view()),
    path('lesson-like/<int:lesson_id>/', LessonLikeAPIView.as_view()),
    path('send-notification/<str:target>/', send_notification, name='send_notification'),
    path('search-lesson/<str:keyword>/', search_view, name='search-lesson'),
]