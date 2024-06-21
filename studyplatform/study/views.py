from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from django.contrib.postgres.search import SearchVector
from django.conf import settings

from .models import (Course, ClassRoom, LessonDays, ClassTime, Group, Lesson,
                     LessonVideo, Homework, LessonComment, LessonLike)
from .serializers import (CourseSerializer, ClassRoomSerializer, LessonDaysSerializer,
                          ClassTimeSerializer, GroupSerializer, LessonSerializer,
                          LessonVideoSerializer, HomeworkSerializer, LessonCommentSerializer,
                          LessonLikeSerializer)
from accounts.models import Student, Teacher



class CourseAPIView(viewsets.ModelViewSet):
    """
        This viewset is used for creating/get/retrieving/updating/deleting courses.
        The user must be authenticated to proceed unsafe methods.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ClassRoomAPIView(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer
    permission_classes = [IsAdminUser]


class LessonDaysAPIView(viewsets.ModelViewSet):
    queryset = LessonDays.objects.all()
    serializer_class = LessonDaysSerializer
    permission_classes = [IsAdminUser]


class ClassTimeAPIView(viewsets.ModelViewSet):
    queryset = ClassTime.objects.all()
    serializer_class = ClassTimeSerializer
    permission_classes = [IsAdminUser]


class GroupAPIView(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]


class LessonAPIView(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAdminUser]


class LessonVideoAPIView(viewsets.ModelViewSet):
    queryset = LessonVideo.objects.all()
    serializer_class = LessonVideoSerializer
    permission_classes = [IsAuthenticated]


class HomeworkAPIView(viewsets.ModelViewSet):
    queryset = Homework.objects.all()
    serializer_class = HomeworkSerializer
    permission_classes = [IsAuthenticated]


class LessonCommentAPIView(APIView):
    """
        This class gets POST and GET requests and creates/sends comments
        When a comment is posted, user is authenticated by token it sends and
        he/she will be a comment owner by getting identity from request.user.
    """
    # User must be authenticated to be able to use this feature
    permission_classes = [IsAuthenticated]

    def post(self, request, lesson_id):
        # Used to create a comment for the authenticated user
        content = request.data.get('content', '')
        try:
            lesson = Lesson.objects.get(pk=lesson_id)
        except Lesson.DoesNotExist:
            return Response({"message": "Unable to get the lesson."})

        data = {
            "content": content,
            "lesson": lesson.pk,
            "user": request.user.pk
        }

        serializer = LessonCommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data})
        return Response({"message": "Unable to create a comment!"})

    def get(self, request, lesson_id):
        # This function lists all comments by the given lesson id
        try:
            lesson = Lesson.objects.get(pk=lesson_id)
        except Lesson.DoesNotExist:
            return Response({"message": "Unable to get the lesson."})
        comments = LessonComment.objects.filter(lesson=lesson)
        serializer = LessonCommentSerializer(comments, many=True)
        return Response({"data": serializer.data})


class LessonLikeAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, lesson_id, like):
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


@permission_classes([IsAdminUser])
@api_view(['GET', 'POST'])
def send_notification(request, target):
    """
        This function is used to send emails to different groups. The user must be a superuser.
        Allowed target groups are:
            all -- teachers / students
            students -- only students
            teachers -- only teachers
        Subject and Message comes from the user as a post.
        The sender is the email address in settings.py
    """
    subject = request.data.get('subject', '')
    message = request.data.get('message', '')
    from_user = settings.EMAIL_HOST_USER
    if request.user.is_superuser:
        students = Student.objects.all()
        teachers = Teacher.objects.all()
        if target == 'all':
            for student in students:
                send_mail(subject, message, from_user, [student.email])
            for teacher in teachers:
                send_mail(subject, message, from_user, [teacher.email])
            return Response({"message": 'Message sent to all users!'})
        elif target == 'students':
            for student in students:
                send_mail(subject, message, from_user, [student.email])
            return Response({"message": 'Message sent to students!'})
        elif target == 'teachers':
            for teacher in teachers:
                send_mail(subject, message, from_user, [teacher.email])
            return Response({"message": 'Message sent to teachers!'})
        else:
            return Response({"message": "Wrong target!"})
    return Response({"message": "You have to be a superuser to use email-notification feature!"})


@api_view(['GET'])
def search_view(request, keyword):
    """
        This view is used to search a keyword from lessons.
        Postgres has support for search parameter, and we can
        use annotate and SearchVector to search in many fields.
    """
    lessons = (Lesson.objects.
               annotate(search=SearchVector("topic") + SearchVector("description")).
               filter(search=keyword))
    serializer = LessonSerializer(lessons, many=True)
    return Response({"data": serializer.data})
