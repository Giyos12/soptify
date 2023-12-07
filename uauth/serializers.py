from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    Choice = (
        ('student', 'student'),
        ('teacher', 'teacher'),
    )
    role = serializers.ChoiceField(choices=Choice, default='student', write_only=True)
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
        g = Group.objects.get(name=validated_data['role'])
        user.groups.add(g)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    role = serializers.SerializerMethodField(read_only=True)

    def get_role(self, obj):
        try:
            role = obj.groups.all()[0].name
        except:
            role = 'student'
        return role

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


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    def get_role(self, obj):
        try:
            role = obj.groups.all()[0].name
        except:
            role = None
        return role

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'role')


class LoginSessionSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Incorrect username or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')
        login(self.context['request'], user)
        return data


class RegisterSessionSerializer(serializers.ModelSerializer):
    Choice = (
        ('student', 'student'),
        ('teacher', 'teacher'),
    )
    role = serializers.ChoiceField(choices=Choice, default='student', write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'role')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        g = Group.objects.get(name=validated_data['role'])
        user.groups.add(g)
        return user
