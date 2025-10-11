
# notifications/models.py
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actor_notifications')
    verb = models.CharField(max_length=255)  # e.g., "liked", "commented", "followed"
    timestamp = models.DateTimeField(auto_now_add=True)
    unread = models.BooleanField(default=True)

    # Generic target (optional)
    target_content_type = models.ForeignKey(ContentType, blank=True, null=True, on_delete=models.CASCADE)
    target_object_id = models.CharField(max_length=255, blank=True, null=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Notification: {self.actor} {self.verb} -> {self.recipient}"
