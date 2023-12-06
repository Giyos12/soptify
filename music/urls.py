from django.urls import path, include
from .views import SongViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('song', SongViewSet, basename='song')

urlpatterns = [
    # path('', SongAPIView.as_view()),
    # path('<int:pk>/', SongAPIView.as_view()),
    path('', include(router.urls)),
]
