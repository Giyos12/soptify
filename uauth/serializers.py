from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.CharField(default='student', write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'role', 'token')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')


        if username and password:
            user = User.objects.filter(username=username).first()

            if not user:
                msg = 'Foydalanuvchi nomi'
                raise ValidationError(msg, code='authorization')
            if not user.check_password(password):
                msg = 'paroli xato'
                raise ValidationError(msg, code='authorization')
        else:
            msg = 'Foydalanuvchi nomi va parolni kiriting'
            raise ValidationError(msg, code='authorization')
        token, created = Token.objects.get_or_create(user=user)
        data['token'] = token.key
        return data
