from django.contrib.auth import logout
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response

from .authentication import CsrfExemptSessionAuthentication
from .serializers import RegisterSerializer, LoginSerializer, RegisterSessionSerializer, LoginSessionSerializer
from .permissions import IsTeacher, IsStudent
from rest_framework.viewsets import GenericViewSet


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


class TeacherPage(APIView):
    permission_classes = (IsTeacher,)

    def get(self, request):
        return Response(data={'msg': 'I am teacher'}, status=200)


class StudentPage(APIView):
    permission_classes = (IsStudent,)

    def get(self, request):
        return Response(data={'msg': 'I am student'}, status=200)


class AuthViewSet(GenericViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    serializer_class = RegisterSessionSerializer

    def get_serializer_class(self):
        if self.action == 'login':
            return LoginSessionSerializer
        return RegisterSessionSerializer

    @action(methods=['GET'], detail=False)
    def session(self, request):
        if request.user.is_authenticated:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=200)
        return Response(data={'msg': 'not login'}, status=400)

    @action(methods=['POST'], detail=False)
    def login(self, request):
        serializer = LoginSessionSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=200)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

    @action(methods=['GET'], detail=False)
    def logout(self, request):
        if request.user.is_authenticated:
            logout(request)
            return Response(data={'msg': 'logout'}, status=204)
        return Response(data={'msg': 'not login'}, status=400)
