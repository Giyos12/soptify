from django.shortcuts import render
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, LoginSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        serializer.data['token'] = user.auth_token.key
        dict = serializer.data
        dict['token'] = user.auth_token.key
        return Response(dict, status=201)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=200)


class LogoutView(APIView):
    def post(self, request):
        print(request.user)
        request.user.auth_token.delete()
        return Response(data={'msg': 'logout'}, status=204)

class ExampleView(APIView):
    def get(self, request):
        print(request.user)
        return Response(data={'msg': 'hello world'}, status=200)