from django.contrib.admin import register, ModelAdmin
from .models import Advertising, Feedback


@register(Advertising)
class AdvertisingAdmin(ModelAdmin):
    list_display = ['id', 'title']


@register(Feedback)
class FeedbackAdmin(ModelAdmin):
    list_display = ['id', 'user_type', 'reason']

