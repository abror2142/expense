from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.contrib.postgres.search import SearchVector

from .models import (Course, ClassRoom, LessonDays, ClassTime, Group, Lesson,
                     LessonVideo, Homework, LessonComment, LessonLike)
from .serializers import (CourseSerializer, ClassRoomSerializer, LessonDaysSerializer,
                          ClassTimeSerializer, GroupSerializer, LessonSerializer,
                          LessonVideoSerializer, HomeworkSerializer, LessonCommentSerializer,
                          LessonLikeSerializer)
from accounts.models import Student, Teacher


class CourseAPIView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]


class ClassRoomAPIView(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer


class LessonDaysAPIView(viewsets.ModelViewSet):
    queryset = LessonDays.objects.all()
    serializer_class = LessonDaysSerializer


class ClassTimeAPIView(viewsets.ModelViewSet):
    queryset = ClassTime.objects.all()
    serializer_class = ClassTimeSerializer


class GroupAPIView(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class LessonAPIView(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonVideoAPIView(viewsets.ModelViewSet):
    queryset = LessonVideo.objects.all()
    serializer_class = LessonVideoSerializer


class HomeworkAPIView(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer


class LessonCommentAPIView(APIView):
    def post(self, request, lesson_id):
        content = request.data.get('content', '')
        try:
            lesson = Lesson.objects.get(pk=lesson_id)
        except Lesson.DoesNotExist:
            return Response({"message": "Unable to get the lesson."})
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({"message": "Unable to get the student."})

        data = {
            "content": content,
            "lesson": lesson.pk,
            "student": student.pk
        }

        serializer = LessonCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data})
        return Response({"message": "Unable to create a comment!"})

    def get(self, request, lesson_id):
        try:
            lesson = Lesson.objects.get(pk=lesson_id)
        except Lesson.DoesNotExist:
            return Response({"message": "Unable to get the lesson."})
        comments = LessonComment.objects.filter(lesson=lesson)
        serializer = LessonCommentSerializer(comments, many=True)
        return Response({"data": serializer.data})


class LessonLikeAPIView(APIView):
    def get(self, request, lesson_id):
        try:
            lesson = Lesson.objects.get(pk=lesson_id)
        except Lesson.DoesNotExist:
            return Response({"message": "Unable to get the lesson."})
        try:
            student = Student.objects.get(user=request.user)
        except Student.DoesNotExist:
            return Response({"message": "Unable to get the student."})
        try:
            like = LessonLike.objects.get(lesson=lesson, student=student)
        except LessonLike.DoesNotExist:
            like = None
        # if already liked remove it
        if like:
            like.delete()
            return Response({'message': 'Like Deleted.'})
        # if not liked yet, create a like object for user and the lesson
        data = {
            "student": student.pk,
            "lesson": lesson.pk
        }

        serializer = LessonLikeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': serializer.data})
        return Response({'message': 'Not created!'})


@api_view(['GET', 'POST'])
def send_notification(request):
    subject = request.data.get('subject', '')
    message = request.data.get('message', '')
    if request.user.is_authenticated and request.user.is_superuser:
        students = Student.objects.all()
        for student in students:
            # by looping I am sending individual emails not listed emails.
            send_mail(subject, message, 'abror2142@gmail.com', [student.email])
        return Response({"message": 'Message sent!'})
    return Response({"message": "You have to be a superuser to use email-notification feature!"})


@api_view(['GET'])
def search_view(request, keyword):
    # postgres has suopport for search paramater and we can use annotate and SearchVector to search in many fields.
    lessons = (Lesson.objects.
               annotate(search=SearchVector("topic") + SearchVector("description")).
               filter(search=keyword))
    serializer = LessonSerializer(lessons, many=True)
    return Response({"data": serializer.data})