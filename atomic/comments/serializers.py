from rest_framework import serializers

from revisions.models import Revision
from revisions.serializers import RevisionSerializer
from users.models import User
from users.serializers import UserSerializer
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField(read_only=True)
    user = UserSerializer(read_only=True)
    revision = RevisionSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['uuid', 'text', 'image_s3_key', 'audio_s3_key', 'user', 'reply_to', 'revision', 'replies',
                  'created_at', 'x', 'y']
        read_only_fields = ['user']

    def get_replies(self, obj):
        replies = Comment.objects.filter(reply_to=obj)
        if obj.replies.exists():
            return CommentSerializer(replies, many=True).data
        return []

    def create(self, validated_data):
        user = self.context['user']
        revision = self.context['revision']
        return Comment.objects.create(user=user, revision=revision, **validated_data)
