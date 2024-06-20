from rest_framework import serializers

from .models import (Course, ClassRoom, LessonDays, ClassTime, Group, Lesson,
                     LessonVideo, Homework, LessonComment, LessonLike)


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class ClassRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoom
        fields = '__all__'


class LessonDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonDays
        fields = '__all__'


class ClassTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassTime
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonVideo
        fields = '__all__'


class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'


class LessonCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonComment
        fields = '__all__'


class LessonLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonLike
        fields = '__all__'


