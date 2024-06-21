from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from accounts.models import Teacher, Student



class Course(models.Model):
    """
    Course Model includes course name, its description, and dates.
    It is mainly used as the parent of lesson class.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ClassRoom(models.Model):
    """
    ClassRoom defienes name and description of a room in which lesson held
    """
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class LessonDays(models.Model):
    """
    Lesson Days are week days which lesson will be conducted.
    They are written to select multiple days for a class.
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ClassTime(models.Model):
    """
    CLass time includes starting time and end time.
    It also includes days which lessons will be conducted.
    The duration of the lesson can be added here but I think
    it can be calculated by subtracting start time from end time
    """
    days = models.ManyToManyField(LessonDays)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} {self.end_time}"


class Group(models.Model):
    """
        Group model is used to show an individual
        group which has a teacher, a class room and a class time.
        e.g. FN 12 is a group which is based on the course Python.
    """
    name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class_time = models.ForeignKey(ClassTime, on_delete=models.SET_NULL, null=True)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    """
    Lesson will be held in a group. Lesson name will be named by a teacher like 1-dars.
    Lesson has a topic and description.
    """
    lesson_name = models.CharField(max_length=100)
    topic = models.CharField(max_length=255)
    description = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    start = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lesson_name


def file_size_validator(value):
    """ This function is used to limit file size. It can be adjusted by changing numbers"""
    limit = 2 * 1024 * 1024 * 1024
    if value.size > limit:
        raise ValidationError("File must be less than 2 GB.")


class LessonVideo(models.Model):
    """
    Lesson video is one to many relationship with Lesson.
    One Lesson may have many videos.
    """
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    video = models.FileField(
        upload_to='lesson/video',
        validators=[FileExtensionValidator(['mp4', 'avi']), file_size_validator]
    )
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Homework(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField()

    def __str__(self):
        return f"{self.lesson} {self.deadline}"


class LessonComment(models.Model):
    content = models.TextField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} {self.lesson}"


class LessonLike(models.Model):
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} {self.lesson}"


