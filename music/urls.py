from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SongViewSet

router = DefaultRouter()
router.register('song', SongViewSet, basename='song')


urlpatterns = [
    # path('', SongAPIView.as_view()),
    # path('<int:pk>/', SongAPIView.as_view()),
    path('', include(router.urls)),
]
