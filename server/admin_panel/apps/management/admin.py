from django.contrib.admin import register, ModelAdmin
from .models import Admin, Instructor, Student


class UserAdmin(ModelAdmin):
    list_display = ['id', 'telegram_id', 'name', 'phone_number', 'lang']
    list_filter = ['phone_number']


@register(Admin)
class AdminAdmin(UserAdmin):
    list_display = ['id', 'telegram_id', 'name', 'phone_number', 'lang', 'type']


@register(Instructor)
class InstructorAdmin(UserAdmin):
    list_display = ['id', 'telegram_id', 'name', 'phone_number', 'lang', 'subject']


@register(Student)
class StudentAdmin(UserAdmin):
    pass
