from django.urls import path, include
from .views import RegisterView, LoginView, LogoutView, ExampleView, TeacherPage, StudentPage, AuthViewSet
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register('accounts', AuthViewSet, basename='auth')

urlpatterns = [
                  path('', include('djoser.urls')),
                  path('', include('djoser.urls.authtoken')),
                  path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
                  path('register/', RegisterView.as_view(), name='register'),
                  path('login/', LoginView.as_view(), name='login'),
                  path('logout/', LogoutView.as_view(), name='logout'),
                  path('teacher/', TeacherPage.as_view(), name='teacher'),
                  path('student_page/', StudentPage.as_view(), name='student_page'),
                  path('', ExampleView.as_view(), name='example'),
              ] + router.urls
