from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['uuid', 'text', 'image', 'audio', 'user', 'reply_to', 'revision', 'replies']
        read_only_fields = ['user']

    def get_replies(self, obj):
        replies = Comment.objects.filter(reply_to=obj)
        if obj.replies.exists():
            return CommentSerializer(replies, many=True).data
        return None
