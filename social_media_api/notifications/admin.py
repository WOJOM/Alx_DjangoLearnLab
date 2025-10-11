
# Register your models here.
from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient','actor','verb','timestamp','unread')
    list_filter = ('unread','timestamp')
    search_fields = ('recipient__username','actor__username','verb')
