from rest_framework import serializers
from django.contrib.auth import authenticate
from app.models import User
from app.serializers.position import PositionSerializer


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'position']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'position']

    extra_kwargs = {
        'username': {'required': False},
    }

class UserSerializer(serializers.ModelSerializer):
    position = PositionSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'position', 'date_created', 'date_terminated']



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('Неверные учетные данные.')

        attrs['user'] = user
        return attrs