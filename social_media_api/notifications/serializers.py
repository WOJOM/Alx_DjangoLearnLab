from rest_framework import serializers
from .models import Notification
from django.contrib.contenttypes.models import ContentType

class NotificationSerializer(serializers.ModelSerializer):
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    recipient_username = serializers.CharField(source='recipient.username', read_only=True)
    target_repr = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'recipient_username', 'actor', 'actor_username',
            'verb', 'timestamp', 'unread', 'target_repr'
        ]
        read_only_fields = fields

    def get_target_repr(self, obj):
        if obj.target is None:
            return None
        return str(obj.target)
