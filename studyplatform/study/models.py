from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError

from accounts.models import Teacher, Student


class Course(models.Model):
    """Course Model includes course name, its description, and dates.
    It is mainly used as the parent of lesson class.
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ClassRoom(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class LessonDays(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ClassTime(models.Model):
    days = models.ManyToManyField(LessonDays)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} {self.end_time}"


class Group(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class_time = models.ForeignKey(ClassTime, on_delete=models.SET_NULL, null=True)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=100)
    topic = models.CharField(max_length=255)
    description = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    start = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.lesson_name


def file_size_validator(value):
    limit = 2 * 1024 * 1024 * 1024
    if value.size > limit:
        raise ValidationError("File must be less than 2 GB.")


class LessonVideo(models.Model):
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
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)
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


