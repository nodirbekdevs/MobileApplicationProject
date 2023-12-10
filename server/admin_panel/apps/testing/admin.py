from django.contrib.admin import register, ModelAdmin
from .models import Section, Statistics, Subject, Test


@register(Section)
class SectionAdmin(ModelAdmin):
    list_display = ['id', 'instructor', 'title_uz', 'title_ru', 'total_tests']


@register(Subject)
class SubjectAdmin(ModelAdmin):
    list_display = ['id', 'title_uz', 'title_ru']
    list_filter = ['title_uz', 'title_ru']


@register(Statistics)
class StatisticsAdmin(ModelAdmin):
    list_display = ['id', 'instructor', 'student', 'subject', 'section', 'total_tests', 'right_count', 'wrong_count', 'percentage']
    # list_filter = ['percentage']


@register(Test)
class TestAdmin(ModelAdmin):
    list_display = ['id', 'instructor', 'subject', 'section', 'question_uz', 'question_ru', 'is_testing']
    list_filter = ['is_testing']
