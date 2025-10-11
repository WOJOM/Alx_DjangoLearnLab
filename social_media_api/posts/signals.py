from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from notifications.models import Notification

@receiver(post_save, sender=Comment)
def comment_created_notification(sender, instance, created, **kwargs):
    if not created:
        return
    post = instance.post
    commenter = instance.author
    if post.author != commenter:
        Notification.objects.create(
            recipient=post.author,
            actor=commenter,
            verb='commented on your post',
            target_content_type=ContentType.objects.get_for_model(post),
            target_object_id=str(post.id)
        )
