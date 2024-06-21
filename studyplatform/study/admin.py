from django.contrib import admin

from .models import (Course, ClassRoom, LessonDays, ClassTime, Group, Lesson,
                     LessonVideo, Homework, LessonComment, LessonLike)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']


@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description']
    list_display_links = ['name']


@admin.register(LessonDays)
class LessonDaysAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']


@admin.register(ClassTime)
class ClassTimeAdmin(admin.ModelAdmin):
    list_display = ['id', 'start_time', 'end_time']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'class_room', 'class_time']
    list_display_links = ['name']


class LessonVideInline(admin.TabularInline):
    """ This class provides tabular view to lesson and video models."""
    model = LessonVideo
    extra = 1


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['id', 'group', 'lesson_name', 'topic']
    list_display_links = ['lesson_name']
    inlines = [
        LessonVideInline
    ]


@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['id', 'lesson', 'deadline']
    list_display_links = ['id']


@admin.register(LessonComment)
class LessonCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'lesson', 'content']
    list_display_links = ['id']


@admin.register(LessonLike)
class LessonLikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'student', 'lesson']
    list_display_links = ['id']
