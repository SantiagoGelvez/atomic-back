from rest_framework import serializers

from atomic.modules import get_user_from_jwt_token
from .models import Project
from users.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)

    class Meta:
        model = Project
        fields = ['uuid', 'name', 'description', 'created_at', 'creator']

    def create(self, validated_data):
        user = get_user_from_jwt_token(self.context['request'].COOKIES.get('jwt'))
        return Project.objects.create(creator=user, **validated_data)
