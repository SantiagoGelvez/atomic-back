from rest_framework import serializers

from .models import Revision
from projects.serializers import ProjectSerializer
from users.serializers import UserSerializer


class RevisionSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Revision
        fields = ['uuid', 'attempt', 'file_extension', 'file_s3_key', 'created_at', 'project', 'user']
