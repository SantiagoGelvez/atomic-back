from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex_verbose', read_only=True, required=False)

    class Meta:
        model = User
        fields = ['uuid', 'first_name', 'last_name', 'username', 'email', 'password', 'user_type', 'company']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

