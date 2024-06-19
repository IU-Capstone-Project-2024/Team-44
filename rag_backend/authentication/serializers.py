from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'telegram_id', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            telegram_id=validated_data['telegram_id'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
