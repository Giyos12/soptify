from django.urls import path, include
from .views import RegisterView, LoginView, LogoutView, ExampleView, TeacherPage, StudentPage, AuthViewSet
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('accounts', AuthViewSet, basename='auth')

urlpatterns = [
                  path('register/', RegisterView.as_view(), name='register'),
                  path('login/', LoginView.as_view(), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path('teacher/', TeacherPage.as_view(), name='teacher'),
                  path('student_page/', StudentPage.as_view(), name='student_page'),
                  path('', ExampleView.as_view(), name='example'),
              ] + router.urls
